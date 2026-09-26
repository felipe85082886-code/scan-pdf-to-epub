# Scan PDF to EPUB · 扫描书转换质量检查 Skill

An Agent Skill for turning scanned book PDFs into readable EPUBs **without treating a valid EPUB file as proof of correct OCR**. It guides source inspection, a small OCR trial, page-by-page review, image-based fallback, and final reader checks.

这是一个扫描书转 EPUB 的流程与质量检查 skill。它不会替代 OCR 或 EPUB 制作工具；它要求先核对扫描原图，再决定文字能否作为“校订版”交付。无法完成文字核对时，应明确说明，并可提供原页影像版。

## Install

Copy this directory to `~/.codex/skills/scan-pdf-to-epub` and invoke `$scan-pdf-to-epub`, or let Codex select it for a scanned PDF conversion task. The skill works alongside an EPUB format skill or converter.

## Page coverage check

Start from [`assets/page-map-example.csv`](assets/page-map-example.csv). Add one row for **every source PDF page**, including intentionally omitted blank pages. The `rendering` column records whether that page appears as editable text, an image, or is omitted. An omitted page needs a reason; an included page needs an EPUB target and verified review status.

```sh
python3 scripts/check_page_map.py page-map.csv --expected-pages 369 --epub book.epub
```

The checker detects missing or duplicate source pages, unresolved issues, unverified included pages, and EPUB targets absent from the package. It uses only the Python standard library. **It cannot decide whether OCR words are correct or whether a reviewer truly checked a page.** The skill still requires visual comparison with the source images.

## Scope

The skill is a quality gate and workflow, not a one-click conversion engine. It does not include book scans, copyrighted text, OCR models, or online-service credentials. Its first version grew from a real failure: a book's hidden PDF text layer was corrupt, while the resulting EPUB passed format validation.

Related conversion projects include [Books_Converter](https://github.com/Feplus2/Books_Converter), [Claude-Skill-pdf-to-epub](https://github.com/koreyba/Claude-Skill-pdf-to-epub), and [scan-to-ebook](https://github.com/phuc-nt/scan-to-ebook). Their conversion tools can be useful, while this skill sets a separate gate for text accuracy and honest delivery labels.
