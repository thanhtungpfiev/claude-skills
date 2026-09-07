#!/usr/bin/env python3
"""Soi những thứ ngốn token cố định của một repo Claude Code.

Chỉ đo cái đo được: số dòng CLAUDE.md, thư mục nặng có thật sự bị git bỏ qua
không, key nào trong settings.json là thật. Không đoán chi phí bằng đô la — con
số đó phụ thuộc model và gói cước, `/cost` và `ccusage` mới trả lời được.

    python audit_context.py [đường-dẫn-repo]     # mặc định: thư mục hiện tại
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

try:  # console Windows mặc định cp1252, in tiếng Việt có dấu là vỡ
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Ngưỡng 200 dòng là khuyến nghị của Anthropic cho CLAUDE.md.
CLAUDE_MD_MAX_LINES = 200

# Thư mục/pattern nặng: có mặt trong repo mà không bị ignore là đang nằm trong
# tầm quét của Claude.
HEAVY_DIRS = [
    "node_modules", ".next", "dist", "build", ".output", "out", "target",
    "vendor", ".venv", "venv", "__pycache__", ".turbo", "coverage", ".cache",
    ".gradle", ".terraform", "Pods",
]
HEAVY_FILES = [
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "bun.lockb",
    "poetry.lock", "Cargo.lock", "composer.lock", "Gemfile.lock",
]

# Key từng bị chép nhầm từ blog/bài hướng dẫn — không có trong Claude Code.
BOGUS_SETTINGS_KEYS = {
    "smallModelOverride": (
        "không tồn tại trong Claude Code; muốn ép model phụ (subagent, việc vặt)"
        ' thì đặt env: {"ANTHROPIC_SMALL_FAST_MODEL": "claude-haiku-4-5-20251001"}'
    ),
    "claudeignore": "Claude Code không đọc .claudeignore; nó theo .gitignore",
    "maxThinkingTokens": (
        "không phải key của settings.json; dùng"
        ' env: {"MAX_THINKING_TOKENS": "8000"}'
    ),
}

SECRET_READ_DENIES = ("Read(.env", "Read(**/.env", "Read(**/*.env")

results: list[tuple[str, str, str]] = []  # (mức, tiêu đề, chi tiết)


def add(level: str, title: str, detail: str = "") -> None:
    results.append((level, title, detail))


def est_tokens(text: str) -> int:
    """Ước lượng token, tách riêng ký tự có dấu.

    Tiếng Việt có dấu tốn token hơn hẳn ASCII nên đếm chars/4 kiểu tiếng Anh sẽ
    ra thấp hơn thực tế nhiều lần. Đây vẫn là ước lượng thô (±20%), dùng để so
    trước/sau khi rút gọn chứ đừng trích ra như số liệu chính xác.
    """
    ascii_n = sum(1 for c in text if ord(c) < 128)
    other_n = len(text) - ascii_n
    return round(ascii_n / 4 + other_n / 1.5)


def check_claude_md(repo: Path) -> None:
    files = sorted(
        p for p in repo.rglob("CLAUDE.md")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )
    files += sorted(
        p for p in repo.rglob("CLAUDE.local.md")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )
    if not files:
        add("WARN", "Không có CLAUDE.md",
            "Repo chưa có CLAUDE.md nào. Không phải lỗi, nhưng nghĩa là mỗi phiên "
            "Claude phải tự dò lại lệnh build/test và quy ước — thường tốn hơn là "
            "20 dòng viết sẵn.")
        return

    total = 0
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.count("\n") + 1
        tok = est_tokens(text)
        total += tok
        rel = f.relative_to(repo)
        level = "FAIL" if lines > CLAUDE_MD_MAX_LINES else "PASS"
        add(level, f"{rel}: {lines} dòng · ~{tok:,} token",
            "" if level == "PASS"
            else f"Vượt ngưỡng {CLAUDE_MD_MAX_LINES} dòng. Phần workflow dài nên "
                 "chuyển sang skill riêng — skill chỉ nạp metadata lúc khởi động, "
                 "CLAUDE.md thì nạp nguyên văn mỗi request.")

    if len(files) > 1:
        add("WARN", f"Có {len(files)} file CLAUDE.md, tổng ~{total:,} token",
            "File CLAUDE.md ở thư mục con được nạp thêm khi Claude đụng vào thư "
            "mục đó. Kiểm xem chúng có nói lại thứ file gốc đã nói không.")

    root = repo / "CLAUDE.md"
    if root.exists():
        body = root.read_text(encoding="utf-8", errors="replace").lower()
        if "compact" not in body:
            add("WARN", "CLAUDE.md chưa có luật compaction",
                "Thêm một khối ngắn liệt kê thứ phải giữ lại khi nén context "
                "(mục tiêu task, file đã sửa, kết quả test, quyết định đã chốt). "
                "Auto-compact vẫn sẽ chạy khi context gần đầy; có khối này thì nó "
                "biết ưu tiên giữ gì.")


def git_ignored(repo: Path, paths: list[str]) -> set[str]:
    """Hỏi thẳng git đường nào đang bị ignore — chắc hơn grep .gitignore."""
    if not paths:
        return set()
    try:
        proc = subprocess.run(
            ["git", "check-ignore", "--stdin"],
            cwd=repo, input="\n".join(paths),
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return set()
    return {line.strip().replace("\\", "/").rstrip("/")
            for line in proc.stdout.splitlines() if line.strip()}


def check_gitignore(repo: Path) -> None:
    if not (repo / ".git").exists():
        add("WARN", "Không phải git repo",
            "Claude Code lọc file theo .gitignore, nên ngoài git repo thì không "
            "có gì chặn nó quét thư mục nặng.")
        return

    present: list[str] = []
    for name in HEAVY_DIRS:
        for hit in repo.rglob(name):
            if hit.is_dir() and ".git" not in hit.parts:
                present.append(str(hit.relative_to(repo)).replace("\\", "/"))
                break
    for name in HEAVY_FILES:
        for hit in repo.rglob(name):
            if ".git" not in hit.parts:
                present.append(str(hit.relative_to(repo)).replace("\\", "/"))
                break

    if not present:
        add("PASS", "Không thấy thư mục/lock file nặng nào trong repo")
        return

    ignored = git_ignored(repo, present)
    leaked = [p for p in present if p.replace("\\", "/").rstrip("/") not in ignored]

    if not leaked:
        add("PASS", f"{len(present)} mục nặng đều đã bị .gitignore chặn")
        return

    add("FAIL", f"{len(leaked)} mục nặng KHÔNG bị ignore",
        "Thêm vào .gitignore:\n    " + "\n    ".join(sorted(leaked)))


def check_settings(repo: Path) -> None:
    path = repo / ".claude" / "settings.json"
    if not path.exists():
        add("WARN", "Chưa có .claude/settings.json",
            "Không có file này thì repo dùng model mặc định của phiên cho mọi "
            "việc, và không có hàng rào nào chặn Claude đọc file bí mật.")
        return

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add("FAIL", ".claude/settings.json không parse được", str(exc))
        return

    for key, why in BOGUS_SETTINGS_KEYS.items():
        if key in data or key in data.get("env", {}):
            add("FAIL", f'Key "{key}" là key ma', why)

    if "model" in data:
        add("PASS", f'model = "{data["model"]}"')
    else:
        add("WARN", "Chưa ghim model cho repo",
            'Repo toàn việc thường (sửa nhỏ, viết test, format) thì đặt '
            '"model": "sonnet" để khỏi phải nhớ /model mỗi phiên.')

    env = data.get("env", {})
    if "ANTHROPIC_SMALL_FAST_MODEL" in env:
        add("PASS", f'ANTHROPIC_SMALL_FAST_MODEL = "{env["ANTHROPIC_SMALL_FAST_MODEL"]}"')
    if "MAX_THINKING_TOKENS" in env:
        add("PASS", f'MAX_THINKING_TOKENS = {env["MAX_THINKING_TOKENS"]}')

    deny = data.get("permissions", {}).get("deny", [])
    if any(d.startswith(SECRET_READ_DENIES) for d in deny):
        add("PASS", "permissions.deny đã chặn đọc file .env")
    else:
        add("WARN", "permissions.deny chưa chặn file bí mật",
            'Thêm "Read(.env*)" và "Read(**/*.secret)". .gitignore chặn commit '
            "chứ không chặn Claude đọc — hai chuyện khác nhau.")


def check_big_files(repo: Path) -> None:
    """File văn bản to nằm trong tầm tay Claude — mỗi lần đọc là một cú nạp lớn.

    Chỉ xét file văn bản. Ảnh và binary cũng tốn token nhưng theo cách khác hẳn
    (ảnh bị resize rồi tính theo kích thước hiển thị, không theo byte), nên gộp
    chung vào một bảng "file to" là so hai đơn vị khác nhau.
    """
    if not (repo / ".git").exists():
        return
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"], cwd=repo,
            capture_output=True, text=True, timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired):
        return

    big: list[tuple[int, int, str]] = []  # (byte, token ước lượng, tên)
    for name in proc.stdout.split("\0"):
        if not name:
            continue
        f = repo / name
        try:
            if not f.is_file() or f.stat().st_size <= 100_000:
                continue
            raw = f.read_bytes()
        except OSError:
            continue
        if b"\0" in raw[:8192]:  # binary — bỏ qua
            continue
        big.append((len(raw),
                    est_tokens(raw.decode("utf-8", errors="replace")),
                    name))

    if not big:
        add("PASS", "Không có file văn bản tracked nào vượt 100 KB")
        return

    big.sort(reverse=True)
    lines = [f"{size / 1024:>6.0f} KB · ~{tok:>7,} token  {name}"
             for size, tok, name in big[:8]]
    add("WARN", f"{len(big)} file văn bản tracked vượt 100 KB",
        "Đọc trọn một file trong đây là nạp chừng đó token vào context:\n    "
        + "\n    ".join(lines)
        + "\n  File .html/.pdf/.docx thì convert sang Markdown trước khi đưa cho "
          "Claude; file .log thì grep lấy dòng cần thay vì đọc cả file; note "
          "Markdown quá dài thì đọc theo đoạn (`sed -n`) chứ đừng Read cả file.")


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not repo.is_dir():
        print(f"Không thấy thư mục: {repo}", file=sys.stderr)
        return 2

    print(f"Soi context repo: {repo}\n")
    check_claude_md(repo)
    check_gitignore(repo)
    check_settings(repo)
    check_big_files(repo)

    icon = {"PASS": "[ OK ]", "WARN": "[WARN]", "FAIL": "[FAIL]"}
    for level, title, detail in results:
        print(f"{icon[level]} {title}")
        if detail:
            for line in detail.splitlines():
                print(f"       {line}")
    n_fail = sum(1 for r in results if r[0] == "FAIL")
    n_warn = sum(1 for r in results if r[0] == "WARN")
    print(f"\n{n_fail} FAIL · {n_warn} WARN · "
          f"{sum(1 for r in results if r[0] == 'PASS')} PASS")
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
