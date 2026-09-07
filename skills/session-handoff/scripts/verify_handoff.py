#!/usr/bin/env python3
"""Kiểm một file bàn giao phiên có đủ dùng cho phiên mới không.

Bắt đúng những lỗi mắt thường bỏ sót khi vừa viết xong: thiếu mục, mục để trống,
placeholder chưa điền, đường dẫn file ghi sai (phiên mới đọc sẽ không thấy), và
code block dán nguyên cả file — thứ làm bản bàn giao phình lại đúng bằng cái nó
đang cố tránh.

    python verify_handoff.py <đường-dẫn-handoff.md> [gốc-repo]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

REQUIRED = [
    "Mục tiêu",
    "Trạng thái",
    "Quyết định đã chốt",
    "File đã sửa",
    "Bước tiếp theo",
    "Câu hỏi còn treo",
    "Mở đầu phiên mới",
]

PLACEHOLDERS = re.compile(
    r"\[(what|list|exact|key|unresolved|first message|todo|tbd|\.\.\.)",
    re.IGNORECASE,
)

# Đường dẫn file trong văn bản: có dấu / hoặc \ và một đuôi mở rộng.
PATH_RE = re.compile(r"`([^`\n]*[/\\][^`\n]*\.[A-Za-z0-9]{1,8})`")

# Tổng số dòng nằm trong code fence — bản bàn giao không phải chỗ dán code.
FENCE_RE = re.compile(r"^```", re.MULTILINE)

MAX_FENCED_LINES = 40
MAX_TOTAL_LINES = 150

problems: list[str] = []
notes: list[str] = []


def check_sections(text: str) -> None:
    for name in REQUIRED:
        # Khớp cả "**Mục tiêu:**" lẫn "## Mục tiêu"
        m = re.search(
            rf"^(?:#{{1,6}}\s*|\*\*)\s*{re.escape(name)}[^\n]*?(?:\*\*)?:?\s*(.*)$",
            text, re.MULTILINE | re.IGNORECASE,
        )
        if not m:
            problems.append(f'Thiếu mục "{name}"')
            continue
        # Nội dung: phần còn lại của dòng, hoặc các dòng tới mục kế tiếp.
        rest = text[m.end():]
        body = (m.group(1) or "").strip() + "\n" + rest.split("\n\n")[0].strip()
        if not body.strip(" \n-*"):
            problems.append(f'Mục "{name}" để trống')


def check_placeholders(text: str) -> None:
    for m in PLACEHOLDERS.finditer(text):
        line = text[:m.start()].count("\n") + 1
        problems.append(f"Dòng {line}: còn placeholder chưa điền — {m.group(0)}…")


def files_modified_block(text: str) -> tuple[str, int]:
    """Cắt riêng mục "File đã sửa" và trả kèm số dòng offset.

    Chỉ mục này mới được kiểm đường dẫn tồn tại. "Bước tiếp theo" hoàn toàn có
    quyền nhắc tới file *sắp tạo* — bắt lỗi ở đó là dương tính giả, và một
    script hay báo sai thì lần sau không ai chạy nữa.
    """
    m = re.search(
        r"^(?:#{1,6}\s*|\*\*)?\s*File đã sửa",
        text, re.MULTILINE | re.IGNORECASE,
    )
    if not m:
        return "", 0
    # Cắt từ ngay sau nhãn, không phải sau hết dòng — nội dung hay nằm luôn
    # trên cùng dòng với nhãn (`**File đã sửa:** \`a.py\``).
    rest = text[m.end():]
    nxt = re.search(r"^(?:#{1,6}\s+|\*\*\S)", rest, re.MULTILINE)
    block = rest[: nxt.start()] if nxt else rest
    return block, text[: m.end()].count("\n")


def check_paths(text: str, root: Path) -> None:
    block, offset = files_modified_block(text)
    if not block.strip():
        problems.append('Mục "File đã sửa" không có nội dung để kiểm')
        return

    seen: set[str] = set()
    missing = 0
    for m in PATH_RE.finditer(block):
        raw = m.group(1).strip()
        if raw in seen:
            continue
        seen.add(raw)
        # Bỏ hậu tố kiểu ":42" hay ":42-88"
        clean = re.sub(r":\d+(-\d+)?$", "", raw)
        if (root / clean).exists():
            continue
        missing += 1
        line = offset + block[:m.start()].count("\n") + 1
        problems.append(
            f"Dòng {line}: không thấy file `{clean}` dưới {root} "
            "— phiên mới đọc bản bàn giao này sẽ đi vào ngõ cụt"
        )
    if seen:
        if not missing:
            notes.append(
                f'{len(seen)} đường dẫn trong mục "File đã sửa", đều tồn tại'
            )
    else:
        problems.append(
            'Mục "File đã sửa" không có đường dẫn nào trong `backtick` — phải '
            "ghi đường dẫn thật, không phải mô tả chung chung"
        )


def check_size(text: str) -> None:
    lines = text.splitlines()
    if len(lines) > MAX_TOTAL_LINES:
        problems.append(
            f"Bản bàn giao dài {len(lines)} dòng (> {MAX_TOTAL_LINES}). "
            "Nó sẽ được nạp nguyên văn vào phiên mới — dài quá là tự tay dựng "
            "lại đúng cái context vừa bỏ đi."
        )

    fenced = 0
    inside = False
    for line in lines:
        if line.startswith("```"):
            inside = not inside
            continue
        if inside:
            fenced += 1
    if fenced > MAX_FENCED_LINES:
        problems.append(
            f"{fenced} dòng nằm trong code block (> {MAX_FENCED_LINES}). "
            "Bàn giao nên trỏ tới file:dòng, không dán lại code."
        )


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__, file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    if not path.is_file():
        print(f"Không thấy file: {path}", file=sys.stderr)
        return 2
    root = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else path.parent

    text = path.read_text(encoding="utf-8", errors="replace")
    check_sections(text)
    check_placeholders(text)
    check_paths(text, root)
    check_size(text)

    print(f"Kiểm bản bàn giao: {path}")
    print(f"Gốc repo để đối chiếu đường dẫn: {root}\n")
    for n in notes:
        print(f"[ OK ] {n}")
    for p in problems:
        print(f"[FAIL] {p}")
    if not problems:
        print("[ OK ] Đủ mục, không placeholder, đường dẫn tồn tại, độ dài hợp lý")
        print("\nPASS")
        return 0
    print(f"\nFAIL — {len(problems)} vấn đề")
    return 1


if __name__ == "__main__":
    sys.exit(main())
