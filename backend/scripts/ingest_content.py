#!/usr/bin/env python3
"""
Content ingestion script for RAG chatbot.

This script reads MDX files from the Docusaurus docs directory,
chunks them, creates embeddings, and uploads to Qdrant.

Usage:
    python scripts/ingest_content.py --docs-path ../my-project/docs
"""

import os
import re
import hashlib
import argparse
import asyncio
import logging
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

# Add parent to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.services.qdrant_service import QdrantService
from src.services.openai_service import OpenAIService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""
    content: str
    doc_id: str
    chapter: str
    part: str
    section: str
    heading: str
    anchor: str
    source_url: str
    file_path: str
    chunk_index: int
    token_count: int


def estimate_tokens(text: str) -> int:
    """Rough token estimation (4 chars per token average)."""
    return len(text) // 4


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract YAML frontmatter from MDX content."""
    frontmatter = {}
    body = content

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            # Parse simple frontmatter
            fm_lines = parts[1].strip().split("\n")
            for line in fm_lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
            body = parts[2]

    return frontmatter, body


def clean_mdx_content(content: str) -> str:
    """Remove MDX-specific syntax and clean content."""
    # Remove import statements
    content = re.sub(r'^import\s+.*$', '', content, flags=re.MULTILINE)

    # Remove JSX components (keep content between tags if simple)
    content = re.sub(r'<[A-Z][^>]*>', '', content)
    content = re.sub(r'</[A-Z][^>]*>', '', content)

    # Remove code blocks but keep inline code
    content = re.sub(r'```[\s\S]*?```', '[code block]', content)

    # Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)

    # Clean up multiple newlines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def extract_headings(content: str) -> list[tuple[str, str, int]]:
    """Extract headings with their positions."""
    headings = []
    for match in re.finditer(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE):
        level = len(match.group(1))
        text = match.group(2).strip()
        position = match.start()
        headings.append((text, f"h{level}", position))
    return headings


def create_anchor(heading: str) -> str:
    """Create URL anchor from heading text."""
    anchor = heading.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor)
    return anchor


def chunk_content(
    content: str,
    chunk_size: int = 400,
    overlap: int = 50,
) -> list[tuple[str, str]]:
    """
    Split content into chunks with overlap.

    Returns list of (chunk_text, nearest_heading) tuples.
    """
    # Get headings with positions
    headings = extract_headings(content)

    # Split into paragraphs
    paragraphs = re.split(r'\n\n+', content)

    chunks = []
    current_chunk = []
    current_tokens = 0
    current_heading = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # Check if this is a heading
        heading_match = re.match(r'^#{1,6}\s+(.+)$', para)
        if heading_match:
            current_heading = heading_match.group(1)

            # If we have accumulated content, save it as a chunk
            if current_chunk and current_tokens > 50:
                chunks.append(("\n\n".join(current_chunk), current_heading))

                # Keep overlap
                overlap_tokens = 0
                overlap_content = []
                for p in reversed(current_chunk):
                    p_tokens = estimate_tokens(p)
                    if overlap_tokens + p_tokens <= overlap:
                        overlap_content.insert(0, p)
                        overlap_tokens += p_tokens
                    else:
                        break

                current_chunk = overlap_content
                current_tokens = overlap_tokens

            continue

        para_tokens = estimate_tokens(para)

        # If adding this paragraph exceeds chunk size, save current chunk
        if current_tokens + para_tokens > chunk_size and current_chunk:
            chunks.append(("\n\n".join(current_chunk), current_heading))

            # Keep overlap
            overlap_tokens = 0
            overlap_content = []
            for p in reversed(current_chunk):
                p_tokens = estimate_tokens(p)
                if overlap_tokens + p_tokens <= overlap:
                    overlap_content.insert(0, p)
                    overlap_tokens += p_tokens
                else:
                    break

            current_chunk = overlap_content
            current_tokens = overlap_tokens

        current_chunk.append(para)
        current_tokens += para_tokens

    # Don't forget the last chunk
    if current_chunk and current_tokens > 50:
        chunks.append(("\n\n".join(current_chunk), current_heading))

    return chunks


def parse_chapter_info(file_path: Path) -> tuple[str, str]:
    """Extract chapter and part info from file path."""
    parts = file_path.parts

    part = ""
    chapter = ""

    for p in parts:
        if p.startswith("part-"):
            # Convert part-i-foundations to "Part I: Foundations"
            part_match = re.match(r'part-([ivx]+)-(.+)', p)
            if part_match:
                numeral = part_match.group(1).upper()
                name = part_match.group(2).replace("-", " ").title()
                part = f"Part {numeral}: {name}"

    # Get chapter from filename
    filename = file_path.stem
    ch_match = re.match(r'ch(\d+)-(.+)', filename)
    if ch_match:
        ch_num = ch_match.group(1)
        ch_name = ch_match.group(2).replace("-", " ").title()
        chapter = f"Chapter {ch_num}: {ch_name}"
    elif filename == "glossary":
        chapter = "Glossary"

    return part, chapter


def build_source_url(file_path: Path, base_url: str) -> str:
    """Build the published URL for a doc file."""
    # Convert file path to URL path
    # my-project/docs/part-i-foundations/ch01-embodied-intelligence.mdx
    # -> /docs/part-i-foundations/ch01-embodied-intelligence

    relative = str(file_path).split("docs/")[-1]
    url_path = relative.replace(".mdx", "").replace(".md", "")

    return f"{base_url}/docs/{url_path}"


async def process_file(
    file_path: Path,
    base_url: str,
    chunk_size: int,
    overlap: int,
) -> list[Chunk]:
    """Process a single MDX file into chunks."""
    logger.info(f"Processing: {file_path}")

    content = file_path.read_text(encoding="utf-8")

    # Extract frontmatter
    frontmatter, body = extract_frontmatter(content)

    # Clean content
    clean_content = clean_mdx_content(body)

    if not clean_content or len(clean_content) < 100:
        logger.warning(f"Skipping {file_path}: too little content")
        return []

    # Get chapter info
    part, chapter = parse_chapter_info(file_path)

    # Build source URL
    source_url = build_source_url(file_path, base_url)

    # Create doc ID from file path
    doc_id = hashlib.md5(str(file_path).encode()).hexdigest()[:12]

    # Chunk the content
    raw_chunks = chunk_content(clean_content, chunk_size, overlap)

    chunks = []
    for i, (chunk_text, heading) in enumerate(raw_chunks):
        anchor = create_anchor(heading) if heading else ""

        chunks.append(Chunk(
            content=chunk_text,
            doc_id=doc_id,
            chapter=chapter or frontmatter.get("title", file_path.stem),
            part=part,
            section=heading,
            heading=heading,
            anchor=anchor,
            source_url=source_url + (f"#{anchor}" if anchor else ""),
            file_path=str(file_path),
            chunk_index=i,
            token_count=estimate_tokens(chunk_text),
        ))

    logger.info(f"  Created {len(chunks)} chunks")
    return chunks


async def ingest_docs(
    docs_path: Path,
    base_url: str,
    chunk_size: int = 400,
    overlap: int = 50,
    dry_run: bool = False,
):
    """Main ingestion function."""
    logger.info(f"Starting ingestion from: {docs_path}")
    logger.info(f"Base URL: {base_url}")
    logger.info(f"Chunk size: {chunk_size}, Overlap: {overlap}")

    # Find all MDX files
    mdx_files = list(docs_path.rglob("*.mdx"))
    md_files = list(docs_path.rglob("*.md"))
    all_files = mdx_files + md_files

    logger.info(f"Found {len(all_files)} documentation files")

    # Process all files
    all_chunks = []
    for file_path in all_files:
        try:
            chunks = await process_file(file_path, base_url, chunk_size, overlap)
            all_chunks.extend(chunks)
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    logger.info(f"Total chunks created: {len(all_chunks)}")
    total_tokens = sum(c.token_count for c in all_chunks)
    logger.info(f"Total estimated tokens: {total_tokens}")

    if dry_run:
        logger.info("Dry run - not uploading to Qdrant")
        # Print sample chunks
        for chunk in all_chunks[:3]:
            logger.info(f"\nSample chunk:")
            logger.info(f"  Chapter: {chunk.chapter}")
            logger.info(f"  Section: {chunk.section}")
            logger.info(f"  Tokens: {chunk.token_count}")
            logger.info(f"  Content preview: {chunk.content[:200]}...")
        return

    # Initialize services
    qdrant = QdrantService()
    openai = OpenAIService()

    # Create collection if needed
    logger.info("Ensuring Qdrant collection exists...")
    await qdrant.create_collection_if_not_exists()

    # Create embeddings in batches
    logger.info("Creating embeddings...")
    chunk_texts = [c.content for c in all_chunks]
    embeddings = await openai.create_embeddings_batch(chunk_texts)

    logger.info(f"Created {len(embeddings)} embeddings")

    # Prepare chunks for upload
    chunk_dicts = [
        {
            "chunk_id": f"{c.doc_id}_{c.chunk_index}",
            "content": c.content,
            "chapter": c.chapter,
            "part": c.part,
            "section": c.section,
            "heading": c.heading,
            "anchor": c.anchor,
            "source_url": c.source_url,
            "file_path": c.file_path,
            "doc_id": c.doc_id,
        }
        for c in all_chunks
    ]

    # Upload to Qdrant
    logger.info("Uploading to Qdrant...")
    await qdrant.upsert_chunks(chunk_dicts, embeddings)

    logger.info("Ingestion complete!")
    logger.info(f"  Files processed: {len(all_files)}")
    logger.info(f"  Chunks created: {len(all_chunks)}")
    logger.info(f"  Estimated tokens: {total_tokens}")


def main():
    parser = argparse.ArgumentParser(description="Ingest documentation into Qdrant")
    parser.add_argument(
        "--docs-path",
        type=Path,
        default=Path("../my-project/docs"),
        help="Path to docs directory",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default="https://assadsharif.github.io/Physical-AI-Humanoid-Robotics",
        help="Base URL for the published site",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=400,
        help="Target chunk size in tokens",
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=50,
        help="Overlap between chunks in tokens",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Process files without uploading",
    )

    args = parser.parse_args()

    # Validate docs path
    if not args.docs_path.exists():
        logger.error(f"Docs path does not exist: {args.docs_path}")
        sys.exit(1)

    # Run ingestion
    asyncio.run(ingest_docs(
        docs_path=args.docs_path,
        base_url=args.base_url,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        dry_run=args.dry_run,
    ))


if __name__ == "__main__":
    main()
