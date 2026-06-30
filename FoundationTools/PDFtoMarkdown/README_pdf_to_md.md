PDF → Markdown Converter

Usage

- Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-pdf-to-md.txt
```

- Convert a PDF:

```powershell
python pdf_to_markdown.py "input.pdf" --outdir ./out
```

This produces `out/<pdf-stem>.md` and an `out/images/` folder containing extracted images.
