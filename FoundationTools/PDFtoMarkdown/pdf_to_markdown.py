#!/usr/bin/env python3
"""
Simple PDF -> Markdown converter using PyMuPDF (fitz).
- Extracts plain text per page
- Extracts embedded images into an `images/` subfolder
- Produces a markdown file named `<pdf-stem>.md` in the output directory

Usage:
    python pdf_to_markdown.py input.pdf --outdir ./output

"""
import argparse
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except Exception as e:
    print("Missing dependency: PyMuPDF. Install with: pip install PyMuPDF")
    raise


def pdf_to_md(pdf_path: Path, out_dir: Path, images_dir_name: str = "images", overwrite: bool = False) -> Path:
    doc = fitz.open(pdf_path)
    stem = pdf_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)
    images_dir = out_dir / images_dir_name
    images_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"{stem}.md"
    if md_path.exists() and not overwrite:
        raise FileExistsError(f"Markdown file {md_path} already exists; use --overwrite to replace")

    md_lines = [f"# {stem}", ""]
    img_counter = 1

    for pnum in range(doc.page_count):
        page = doc.load_page(pnum)
        text = page.get_text("text")
        md_lines.append(f"### Page {pnum + 1}")
        md_lines.append("")
        if text.strip():
            # Preserve the page text as-is (simple conversion)
            md_lines.append(text.rstrip())
            md_lines.append("")

        # Extract images on this page
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue
            image_bytes = base_image.get("image")
            img_ext = base_image.get("ext", "png")
            img_name = f"{stem}_p{pnum + 1}_img{img_counter}.{img_ext}"
            img_path = images_dir / img_name
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            # Use a relative path from the markdown file to the image directory
            md_lines.append(f"![{img_name}]({images_dir_name}/{img_name})")
            md_lines.append("")
            img_counter += 1

        md_lines.append("---")
        md_lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    return md_path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert PDF to Markdown (text + images)")
    parser.add_argument("pdf", type=Path, help="Input PDF file path")
    parser.add_argument("--outdir", type=Path, default=Path("."), help="Output directory for markdown and images")
    parser.add_argument("--images-dir", type=str, default="images", help="Images subfolder name in the output directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing markdown output file")
    args = parser.parse_args(argv)

    pdf_path = args.pdf
    if not pdf_path.exists():
        print(f"Input PDF not found: {pdf_path}")
        sys.exit(2)

    try:
        md = pdf_to_md(pdf_path, args.outdir, images_dir_name=args.images_dir, overwrite=args.overwrite)
        print(f"Wrote: {md}")
    except FileExistsError as e:
        print(e)
        sys.exit(3)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
