from __future__ import annotations

from pathlib import Path
from typing import Optional

import os

import pymupdf
import pymupdf4llm


def export_markdown(
    doc: pymupdf.Document,
    output_dir: Path,
    base_name: str,
    *,
    write_images: bool = True,
    embed_images: bool = False,
    pages: Optional[list[int]] = None,
) -> Path:
    """
    Render the provided PyMuPDF document into Markdown via pymupdf4llm.

    Args:
        doc: Translated PyMuPDF document to render.
        output_dir: Destination directory for Markdown (and optional images).
        base_name: Base filename (without extension) used for the outputs.
        write_images: Whether to dump extracted images to disk.
        embed_images: Whether to embed images via data URIs instead of files.
        pages: Optional list of 0-based page indices to include.
    """

    if write_images and embed_images:
        raise ValueError("write_images and embed_images cannot both be True")

    output_dir.mkdir(parents=True, exist_ok=True)
    assets_dir: Optional[Path] = None
    image_path = output_dir

    assets_rel = None
    image_dir_token = None
    output_dir_abs = output_dir.resolve()
    assets_dir = None
    if write_images:
        assets_dir = output_dir / f"{base_name}_assets"
        assets_rel = Path(os.path.relpath(assets_dir.resolve(), output_dir_abs))
        image_dir_token = assets_dir.as_posix()
        assets_dir.mkdir(parents=True, exist_ok=True)
        image_path = assets_dir

    safe_pdf_name = f"{base_name.replace(' ', '-')}.pdf"

    markdown_text = pymupdf4llm.to_markdown(
        doc,
        filename=safe_pdf_name,
        write_images=write_images,
        embed_images=embed_images,
        image_path=str(image_path),
        pages=pages,
    )

    if write_images and assets_rel and image_dir_token:
        markdown_text = markdown_text.replace(
            image_dir_token,
            assets_rel.as_posix(),
        )

    md_path = output_dir / f"{base_name}.md"
    md_path.write_text(markdown_text, encoding="utf-8")
    return md_path
