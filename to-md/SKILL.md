---
name: to-md
description: Convert files and content to Markdown. Trigger this skill whenever the user wants to convert any file format to .md — PDFs, Word documents, Excel spreadsheets, PowerPoint presentations, images, HTML pages, CSVs, YouTube URLs, ZIP archives, and more. Use this skill even if the user just says "turn this into markdown", "convert to md", "make this readable as markdown", "extract text from PDF as markdown", or similar.
---

# To Markdown

Convert files and content to Markdown.

## Supported input formats

PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx), images (PNG/JPG/etc.),
HTML, URLs, YouTube URLs, CSV, JSON, XML, ZIP, EPub.

## Single file or URL

```sh
python3 scripts/convert.py <input> [-o output.md]
```

- Print result to stdout: `python3 scripts/convert.py report.pdf`
- Save to file: `python3 scripts/convert.py report.pdf -o report.md`
- Convert a URL: `python3 scripts/convert.py https://example.com -o page.md`
- Scanned or image-based PDF: `python3 scripts/convert.py scan.pdf --ocr -o scan.md`
- High-accuracy (Azure DI): `python3 scripts/convert.py scan.pdf --azure-endpoint $AZURE_DI_ENDPOINT --azure-key $AZURE_DI_KEY -o scan.md`

## Batch conversion

```sh
python3 scripts/batch_convert.py [directory] [--pattern GLOB] [--recursive]
```

- Specific format: `python3 scripts/batch_convert.py --pattern "*.xlsx"`
- Subdirectory, specific format: `python3 scripts/batch_convert.py ~/Docs --pattern "*.pdf" --recursive`

Each input file gets a matching `.md` alongside it (`report.pdf` → `report.md`).

## Workflow

1. One file or URL → `scripts/convert.py`; multiple files → `scripts/batch_convert.py`.
2. Show the user the output or confirm the saved file path.
3. If the output looks garbled or empty (common with scanned PDFs), rerun with `--ocr`.
