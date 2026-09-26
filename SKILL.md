---
name: scan-pdf-to-epub
description: Convert a scanned book PDF into a readable EPUB, preserving original pages when OCR is unreliable. Use for scan-based book conversion, OCR repair, and diagnosing garbled text in a converted EPUB; use the epub skill for ordinary EPUB structure or metadata edits.
---

# Scanned PDF to EPUB

Build an EPUB whose text is actually readable. Ask for the source PDF and the desired reading style only when they are not available from the task or prior context. Respect the user's chosen output and any existing conversion requirements.

## Inspect the source

- Determine whether the PDF has selectable text, page scans, mixed pages, vertical writing, rotated or reverse-ordered pages, illustrations, notes, and a usable contents page.
- Treat any PDF text layer as unverified OCR until it is compared with page images. Check early, middle, and late pages plus every distinct layout before choosing a recognition method. If these checks show pervasive errors, do not use that layer as the main text source.
- Make a page map before building chapter navigation. Classify each source page as text, blank, cover, illustration, contents, or notes; record its reading order and intended EPUB destination. Account explicitly for missing, repeated, and intentionally omitted pages.
- For a CSV page map, start from [the example](assets/page-map-example.csv) and run `python3 scripts/check_page_map.py page-map.csv --expected-pages N --epub book.epub` before delivery. The script catches missing pages, unresolved review flags, and broken EPUB targets; it does not judge OCR accuracy.

## Trial before full conversion

- Run a small trial on representative pages before processing the whole book: ordinary text, the hardest layout, proper names or mixed scripts, illustrations, and notes where present. Compare the candidate OCR output with those source images. Change the method if columns are skipped, the order is wrong, or text is plainly corrupted.
- If recognition uses a paid or remote service, establish its destination, cost, and authorization before sending the book. Save per-page results so failed pages can be retried without reprocessing verified pages.

## Choose the deliverable

- For reflowable text, recognize and correct the content before packaging it. Use OCR suited to the script and page orientation. Flag empty or unusually short text pages, implausible characters, and large disagreements between recognition methods for review. Check terms and names against the source image before using them as context for other pages.
- Review every text-bearing source page against its proposed text, including column order, omissions, proper names, foreign words, punctuation, and paragraph boundaries; resolve uncertain passages from the image. Keep a page-level record of source image, OCR source, review status, and unresolved issues. A few sampled pages, confidence scores, or automated replacement counts do not establish that the whole book is corrected.
- Do not release a reflowable edition as proofread, corrected, or final while any text-bearing page remains unreviewed or known OCR gibberish remains. EPUBCheck and reader screenshots cannot satisfy this text-accuracy gate.
- If the gate cannot be met, offer an image-based EPUB that retains legible original pages and state explicitly that the requested reflowable edition remains unfinished. Only provide raw OCR text when the user explicitly requests an unverified OCR edition; label it visibly as such. Make scans large enough to read in a real reader and place notes in their true reading order.
- Preserve the source file. Do not overwrite a known-good edition with an uncertain one. Withdraw or clearly label a defective edition when repairing it.

## Verify before delivery

- Validate the EPUB container and navigation with EPUBCheck. Treat this as a format check only; it cannot establish OCR accuracy.
- For a reflowable edition, extract text from the finished EPUB and compare it with the reviewed text, not with an untrusted PDF text layer. Reconcile every source page with the page map so packaging cannot silently drop content.
- Open the actual EPUB in a reading app. Inspect cover, contents, opening pages, several middle chapters, the end, notes, and pages likely to stress OCR. Compare visible text to original scans. Confirm every source page is represented once and in the intended order; check navigation and illustrations.
- Report which edition is reflowable, which retains page images, what was checked, and any remaining OCR uncertainty. Never call an edition proofread merely because EPUBCheck passes.

Use the `epub` skill for EPUB format mechanics and validation when available. Keep this skill focused on the scan-to-readable-book decisions and quality gate.
