#!/usr/bin/env python3
"""
Rà một note đã có khối "## 📑 Mục lục", báo đúng 4 điều:
  1. Heading nào bị "mồ côi" — có trong file nhưng không có mặt trong Mục lục.
  2. Anchor nào trong Mục lục "gãy" — trỏ tới heading không tồn tại.
  3. Thứ tự trong Mục lục có khớp thứ tự heading thật xuất hiện trong file.
  4. Toàn bộ `[[#...]]` trong CẢ FILE (không chỉ khối Mục lục) có gãy không —
     đổi tên một heading thì mọi backlink kiểu "↑ [[#📑 Mục lục|Mục lục]]"
     hay tham chiếu chéo khác đều có nguy cơ gãy theo mà không có gì báo.

Đây là việc lẽ ra phải tự viết lại bằng tay mỗi lần rà một note — cố định
thành script để chạy lại được, không phải suy luận lại logic mỗi lần.

Dùng:   python verify_toc.py <note.md>
Thoát:  0 nếu mọi mục PASS, 1 nếu có FAIL.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts._tocsupport import (  # noqa: E402
    read_lines, extract_headings, extract_wikilinks, find_toc_block,
    line_of_offset, die,
)

HINH_RE = re.compile(r"^Hình\s+\d+")


def order_check(file_order, toc_anchor_order, toc_anchor_set, group_name):
    if any(t not in toc_anchor_set for t in file_order):
        return None, [f"  (bỏ qua — nhóm {group_name} chưa phủ đủ ở mục coverage phía trên)"]
    seen_in_group = [a for a in toc_anchor_order if a in set(file_order)]
    dedup = list(dict.fromkeys(seen_in_group))
    if dedup == file_order:
        return True, []
    return False, [
        f"  - thứ tự trong Mục lục : {dedup}",
        f"  - thứ tự thật trong file: {file_order}",
    ]


def main():
    if len(sys.argv) != 2:
        die("Dùng: python verify_toc.py <note.md>")
    path = sys.argv[1]
    try:
        lines = read_lines(path)
    except OSError as e:
        die(f"Không đọc được {path}: {e}")
    text = "\n".join(lines)

    all_heads = extract_headings(lines)
    all_head_texts = {txt for _, _, txt in all_heads}

    block = find_toc_block(text, lines)
    if block is None:
        print(f'[FAIL] Không tìm thấy heading "## 📑 Mục lục" trong {path}.')
        print("=> Note chưa có mục lục — dùng extract_headings.py để dựng mới, verify chỉ dùng cho note đã có khối này.")
        sys.exit(1)

    start, end = block
    toc_text = "\n".join(lines[start:end])
    toc_links = extract_wikilinks(toc_text)
    toc_anchor_order = [a for a, _l, _o in toc_links]
    toc_anchor_set = set(toc_anchor_order)

    group_a_file = [t for _, lvl, t in all_heads if lvl == 2 and t.strip() != "📑 Mục lục"]
    group_b_file = [t for _, lvl, t in all_heads if lvl == 3 and HINH_RE.match(t.strip())]

    results = []  # (label, True/False/None, [detail lines])

    # 1) coverage — heading mồ côi
    missing_a = [t for t in group_a_file if t not in toc_anchor_set]
    missing_b = [t for t in group_b_file if t not in toc_anchor_set]
    results.append((
        f"Heading Chương (##) phủ đủ trong Mục lục: {len(group_a_file) - len(missing_a)}/{len(group_a_file)}",
        not missing_a,
        [f'  - mồ côi: "{t}"' for t in missing_a],
    ))
    results.append((
        f"Heading Hình (### Hình N) phủ đủ trong Mục lục: {len(group_b_file) - len(missing_b)}/{len(group_b_file)}",
        not missing_b,
        [f'  - mồ côi: "{t}"' for t in missing_b],
    ))

    # 2) anchor gãy trong khối Mục lục
    broken_in_toc = [a for a in toc_anchor_order if a not in all_head_texts]
    results.append((
        f"Anchor trong Mục lục khớp heading thật: {len(toc_anchor_order) - len(broken_in_toc)}/{len(toc_anchor_order)}",
        not broken_in_toc,
        [f"  - gãy: [[#{a}]]" for a in broken_in_toc],
    ))

    # 3) thứ tự
    status_a, detail_a = order_check(group_a_file, toc_anchor_order, toc_anchor_set, "Chương")
    results.append(("Thứ tự Mục lục khớp thứ tự file (Chương)", status_a, detail_a))
    status_b, detail_b = order_check(group_b_file, toc_anchor_order, toc_anchor_set, "Hình")
    results.append(("Thứ tự Mục lục khớp thứ tự file (Hình)", status_b, detail_b))

    # 4) toàn bộ [[#...]] trong file, không chỉ khối Mục lục
    all_links = extract_wikilinks(text)
    broken_whole = [(a, line_of_offset(text, off)) for a, _l, off in all_links if a not in all_head_texts]
    results.append((
        f"Toàn bộ [[#...]] trong file khớp heading thật: {len(all_links) - len(broken_whole)}/{len(all_links)}",
        not broken_whole,
        [f"  - L{ln}: [[#{a}]] không khớp heading nào" for a, ln in broken_whole],
    ))

    print(f"=== VERIFY TOC: {path} ===")
    any_fail = False
    for label, status, detail in results:
        tag = "PASS" if status else ("SKIP" if status is None else "FAIL")
        if status is False:
            any_fail = True
        print(f"[{tag}] {label}")
        for d in detail:
            print(d)

    print()
    if any_fail:
        print("=> CÓ MỤC FAIL — sửa rồi chạy lại script này tới khi sạch PASS.")
    else:
        print("=> TẤT CẢ PASS — mục lục nhất quán với heading thật.")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
