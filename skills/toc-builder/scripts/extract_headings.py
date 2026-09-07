#!/usr/bin/env python3
"""
In ra khung sườn của một note để soạn/rà khối "## 📑 Mục lục":
  1. Mọi heading `##`/`###` thật trong file, đúng thứ tự, kèm số dòng.
  2. Khối Mục lục hiện có (nếu note đã có) — từng wikilink `[[#anchor|nhãn]]`,
     tách theo nhóm "Chương" (mọi heading `##`) và "Hình" (heading `###` khớp
     `Hình N — ...`).

Mục đích: cho model một bản đồ heading đã dò sẵn, khỏi phải tự đọc lại cả file
để tìm heading mỗi lần soạn mục lục. Không tự viết mô tả hay tự đoán nhãn rút
gọn — việc đó vẫn cần đọc nội dung từng chương, script không làm thay được.

Dùng: python extract_headings.py <đường-dẫn-note.md>
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts._tocsupport import (  # noqa: E402
    read_lines, extract_headings, extract_wikilinks, find_toc_block, die,
)

HINH_RE = re.compile(r"^Hình\s+\d+")


def main():
    if len(sys.argv) != 2:
        die("Dùng: python extract_headings.py <note.md>")
    path = sys.argv[1]
    try:
        lines = read_lines(path)
    except OSError as e:
        die(f"Không đọc được {path}: {e}")
    text = "\n".join(lines)

    heads = extract_headings(lines)
    if not heads:
        print("Không tìm thấy heading ##/### nào trong file (ngoài frontmatter/code fence).")
        return

    print(f"=== HEADING theo thứ tự file ({path}) ===")
    for line_no, level, txt in heads:
        mark = "##" if level == 2 else "#" * level
        group = ""
        if level == 2 and txt.strip() != "📑 Mục lục":
            group = "  [Chương]"
        elif level == 3 and HINH_RE.match(txt.strip()):
            group = "  [Hình]"
        print(f"L{line_no:<5} {mark:<3} {txt}{group}")

    block = find_toc_block(text, lines)
    print()
    if block is None:
        print('Note CHƯA có heading "## 📑 Mục lục" — đây là note cần dựng mục lục mới.')
        return

    start, end = block
    print(f"=== Khối Mục lục hiện có: dòng {start}–{end} ===")
    toc_text = "\n".join(lines[start:end])
    links = extract_wikilinks(toc_text)
    if not links:
        print("(khối rỗng hoặc không chứa wikilink nào — có thể đang ở kiểu cũ, vd nối bằng ' · ')")
    for anchor, label, _off in links:
        print(f"  [[#{anchor}{'|' + label if label else ''}]]")


if __name__ == "__main__":
    main()
