r"""
Hàm dùng chung cho extract_headings.py và verify_toc.py.

Không có logic quyết định (nối câu, chọn nhãn...) ở đây — chỉ có phần cơ học:
đọc heading thật và đọc wikilink `[[#...]]` từ một file .md, theo đúng quy ước
của vault (frontmatter YAML ở đầu, code fence không tính là heading, `\|` trong
ô bảng là escape chứ không phải phần anchor).
"""
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass  # Python < 3.7, hoặc stdout đã bị thay bằng thứ không có reconfigure


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def frontmatter_end(lines):
    """Số dòng (0-based) kết thúc khối frontmatter YAML, hoặc 0 nếu không có."""
    if not lines or lines[0].strip() != "---":
        return 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return i + 1
    return 0  # '---' đầu không khớp '---' đóng nào → không phải frontmatter thật


def extract_headings(lines):
    """
    Trả về list (line_no 1-based, level int, text str), bỏ qua:
    - frontmatter YAML ở đầu file
    - dòng nằm trong code fence ``` ... ```
    Chỉ nhận heading ATX (`#`..`######`), đúng chuẩn Markdown: có khoảng trắng
    sau dấu #, không tính dòng bắt đầu bằng `#` dính liền chữ (hashtag).
    """
    start = frontmatter_end(lines)
    heads = []
    in_fence = False
    fence_marker = None
    for i in range(start, len(lines)):
        line = lines[i]
        stripped = line.strip()
        fence_match = re.match(r"^(```+|~~~+)", stripped)
        if fence_match:
            marker = fence_match.group(1)[0] * 3
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker[0] == fence_marker[0]:
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            heads.append((i + 1, len(m.group(1)), m.group(2)))
    return heads


def unescape(s):
    """Bỏ escape kiểu Markdown (`\\|` → `|`, `\\\\` → `\\`, ...)."""
    return re.sub(r"\\(.)", r"\1", s)


def extract_wikilinks(text):
    """
    Trả về list (anchor, label_or_None, char_offset) cho mọi `[[#anchor|label]]`
    hoặc `[[#anchor]]` trong `text`.

    Tách tại dấu `|` ĐẦU TIÊN, coi cả `|` trần lẫn `\\|` là cùng một điểm tách.
    Trong ô bảng, `\\|` không phải escape giữ nguyên ký tự `|` bên trong anchor —
    nó là dấu `|` bình thường của cú pháp `[[#anchor|label]]`, chỉ escape để
    khỏi bị trình phân tách cột của bảng Markdown hiểu nhầm thành ranh giới cột.
    Heading trong vault này không chứa `|`, nên coi mọi `|`/`\\|` là điểm tách
    là an toàn — không có ca nào `|` thật sự cần giữ lại bên trong anchor.
    """
    out = []
    for m in re.finditer(r"\[\[#(.*?)\]\]", text):
        inner = m.group(1)
        parts = re.split(r"\\?\|", inner, maxsplit=1)
        anchor = unescape(parts[0])
        label = unescape(parts[1]) if len(parts) > 1 else None
        out.append((anchor, label, m.start()))
    return out


def line_of_offset(text, offset):
    return text.count("\n", 0, offset) + 1


def find_toc_block(text, lines):
    """
    Trả về (start_line, end_line) 1-based (end exclusive) của khối bắt đầu tại
    heading `## 📑 Mục lục`, kết thúc trước dòng `---` đứng riêng kế tiếp (hoặc
    trước heading `##` kế tiếp nếu không có `---`, hoặc hết file).
    Trả về None nếu note chưa có heading đó.
    """
    heads = extract_headings(lines)
    toc_start = None
    for line_no, level, txt in heads:
        if level == 2 and txt.strip() == "📑 Mục lục":
            toc_start = line_no
            break
    if toc_start is None:
        return None
    end = len(lines)
    for i in range(toc_start, len(lines)):  # bắt đầu ngay sau dòng heading
        if lines[i].strip() == "---" or re.match(r"^##\s+", lines[i]):
            end = i  # loại trừ chính dòng '---' hoặc heading '##' kế tiếp
            break
    return (toc_start, end)


def die(msg):
    print(msg, file=sys.stderr)
    sys.exit(2)
