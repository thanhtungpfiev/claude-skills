---
name: token-audit
description: >
  Soi và vá những thứ ngốn token **cố định** của một repo Claude Code —
  CLAUDE.md phình quá 200 dòng, thư mục nặng chưa bị .gitignore chặn,
  .claude/settings.json thiếu ghim model hoặc chép phải key ma, file văn bản
  quá to. Dùng khi người dùng nói "phiên này tốn token quá", "sao hết context
  nhanh vậy", "rà lại context repo này", "tối ưu CLAUDE.md", "giảm chi phí
  Claude Code", "context đầy nhanh quá", hoặc khi vừa clone/khởi tạo một repo
  và muốn set up cho gọn context ngay từ đầu. KHÔNG dùng để bàn giao phiên
  đang dở — việc đó là `session-handoff`.
---

# Soi context repo — cắt phần token trả đi trả lại mỗi request

Mỗi request Claude Code gửi lại **toàn bộ** những gì đang có trong context:
CLAUDE.md, lịch sử hội thoại, nội dung file đã đọc. Nghĩa là một dòng thừa
trong CLAUDE.md không tốn một lần — nó tốn ở **mọi** request còn lại của phiên.
Đó là lý do phần đáng vá trước không phải cách gõ prompt, mà là mấy file cấu
hình nằm im trong repo.

Skill này chỉ lo phần **cố định và đo được** đó. Phần phụ thuộc thói quen của
người dùng (bấm `/clear` lúc nào, có bật plan mode không, ngưỡng 120K token) thì
skill không làm hộ được — xem mục cuối.

## 1. Chạy script trước, đừng tự đọc file để đoán

```bash
python scripts/audit_context.py [đường-dẫn-repo]   # mặc định: thư mục hiện tại
```

In ra `[ OK ] / [WARN] / [FAIL]` cho năm nhóm, kèm bản vá cụ thể ngay dưới mỗi
dòng. Thoát mã 1 nếu có FAIL, 0 nếu không — dùng được trong hook hay CI.

| Nhóm | Script kiểm gì | Ngưỡng |
|---|---|---|
| **CLAUDE.md** | Số dòng và ước lượng token của mọi `CLAUDE.md` / `CLAUDE.local.md` trong repo; có khối luật compaction chưa | > 200 dòng là FAIL (khuyến nghị của Anthropic) |
| **Thư mục nặng** | Hỏi thẳng `git check-ignore` xem `node_modules/`, `dist/`, `.next/`, lock file… **có mặt trong repo** có đang bị chặn không | Còn sót mục nào là FAIL |
| **settings.json** | Có ghim `model` chưa · `env` có `ANTHROPIC_SMALL_FAST_MODEL` / `MAX_THINKING_TOKENS` không · `permissions.deny` đã chặn đọc `.env` chưa | Thiếu là WARN |
| **Key ma** | Bắt các key chép nhầm từ blog: `smallModelOverride`, `claudeignore`, `maxThinkingTokens` | Có là FAIL |
| **File văn bản to** | File tracked > 100 KB kèm ước lượng token khi Read cả file | Có là WARN |

Ba việc trong đây script làm chắc hơn mắt người, đừng thay bằng cách đọc file:

- **`git check-ignore` thay vì grep `.gitignore`.** Có `node_modules/` trong
  `.gitignore` chưa chắc đã chặn — một dòng `!` phía dưới, một `.gitignore` lồng
  trong thư mục con, hay một pattern viết sai chỗ đều lật ngược kết quả mà nhìn
  file thì không thấy. Hỏi git là hỏi đúng thứ Claude Code thật sự theo.
- **Chỉ liệt file văn bản, bỏ ảnh và binary.** Ảnh cũng tốn token nhưng tính
  theo kích thước hiển thị sau resize chứ không theo byte, xếp chung một bảng là
  so hai đơn vị khác nhau và ra con số vô nghĩa.
- **Ước lượng token tách riêng ký tự có dấu.** Công thức `chars/4` quen thuộc
  chỉ đúng cho tiếng Anh; CLAUDE.md viết tiếng Việt tốn hơn hẳn, dùng `chars/4`
  sẽ báo thấp hơn thực tế. Vẫn là ước lượng thô (±20%) — dùng để so trước/sau
  khi rút gọn, đừng trích ra như số liệu chính xác.

## 2. Vá theo thứ tự impact, không vá theo thứ tự script in ra

Script in theo nhóm; vá thì theo tỉ lệ *hiệu quả / công sức*:

1. **`.gitignore`** — 2 phút, hiệu quả ngay lập tức và không có rủi ro nào.
2. **`model` trong `.claude/settings.json`** — 2 phút. Repo toàn việc thường
   (sửa nhỏ, viết test, format, đọc note) thì `"model": "sonnet"`.
3. **Rút gọn `CLAUDE.md`** — 15–20 phút, và là phần duy nhất cần phán đoán.
4. Còn lại là tuỳ chọn.

### Rút gọn CLAUDE.md: luật là "Claude không tự suy ra được"

Bỏ đi: giải thích đây là dự án gì (`package.json` đã nói), copy README, liệt kê
dependency, mô tả cấu trúc thư mục mà `ls` cho thấy trong một giây.

Giữ lại: lệnh không đoán được (`npm run dev` hay `pnpm dev`?), quy ước không có
trong code, và **cạm bẫy** — thứ mà đọc code xong vẫn làm sai.

Workflow dài hơn ~10 dòng thì **chuyển sang skill riêng**, đừng nhét vào
CLAUDE.md. Lý do là cơ chế nạp chứ không phải thẩm mỹ: CLAUDE.md nạp **nguyên
văn ở mọi request**, còn skill lúc khởi động chỉ nạp phần `description` trong
frontmatter (~100 token), thân skill chỉ nạp khi trigger khớp. Mười workflow
trong CLAUDE.md là mười workflow bạn trả tiền mỗi request kể cả khi hôm nay
không đụng tới cái nào.

Cắt xong thì chạy lại script để có con số trước/sau, đừng chỉ nói "đã gọn hơn".

### Khối luật compaction

Auto-compact vẫn sẽ chạy khi context gần đầy dù bạn có làm gì hay không. Khối
này không chặn nó, nó chỉ nói cho việc nén biết phải giữ gì lại:

```markdown
## Compaction Rules

Khi nén context, luôn giữ: mục tiêu task hiện tại và tiêu chí hoàn thành ·
đường dẫn file đã sửa · kết quả test gần nhất · quyết định đã thống nhất
(không mở lại).
```

### `settings.json`: bản đúng, không phải bản chép trên blog

```jsonc
{
  "model": "sonnet",
  "env": {
    "ANTHROPIC_SMALL_FAST_MODEL": "claude-haiku-4-5-20251001",
    "MAX_THINKING_TOKENS": "8000"
  },
  "permissions": {
    "deny": ["Read(.env*)", "Read(**/*.secret)"]
  }
}
```

**`smallModelOverride` không tồn tại** — key này lan truyền qua vài bài hướng
dẫn nhưng grep binary Claude Code ra 0 kết quả. Đặt nó vào `settings.json` thì
không có gì báo lỗi, nó chỉ đơn giản là không có tác dụng, và bạn tưởng mình đã
tối ưu. Knob thật là env `ANTHROPIC_SMALL_FAST_MODEL`.

Tương tự, **không có file `.claudeignore`**. Claude Code theo `.gitignore` (bật
sẵn qua `respectGitignore`). File nào cần chặn *đọc* — không chỉ chặn commit —
thì phải khai trong `permissions.deny`; `.gitignore` chặn commit chứ không chặn
Read, hai chuyện khác nhau.

**Cạm bẫy `MAX_THINKING_TOKENS`:** hạ quá tay cho việc khó thì output kém, bạn
phải bảo làm lại, và một vòng làm lại đắt hơn nhiều lần phần thinking token vừa
tiết kiệm. Đây là "tiết kiệm giả". 8000 là mức hợp cho việc thường; kiến trúc
hay debug nhiều bước thì bỏ hẳn giới hạn.

## 3. Báo cáo bằng số trước/sau

Chạy lại `audit_context.py` sau khi vá và đặt hai bản in cạnh nhau. Con số
trước/sau là thứ duy nhất chứng minh có tiết kiệm thật — "đã tối ưu" không kiểm
chứng được.

Muốn biết chi phí thật thì gõ `/cost` trong phiên hoặc dùng `ccusage` (community
tool, `npm i -g ccusage`); script này cố tình **không** quy ra đô la, vì con số
đó phụ thuộc model và gói cước, đoán bừa thì sai.

## Skill này KHÔNG làm được gì

Đây là phần cần nói thẳng với người dùng chứ đừng hứa hão. Phần tiết kiệm token
lớn nhất nằm ở thói quen của **người dùng**, mà skill nạp vào Claude thì không
bấm phím hộ được:

| Việc | Vì sao skill không làm được |
|---|---|
| Gõ `/clear` giữa hai task khác nhau | Lệnh của người dùng, Claude không tự gọi được |
| `/rewind` khi Claude vừa đi sai hướng | Như trên — và cần người phán đoán "sai hướng" |
| Giữ phiên dưới ~120K token | Kỷ luật, đọc từ status bar |
| Bật plan mode (Shift+Tab) cho việc lớn | Thao tác bàn phím trước khi gửi message |
| Viết prompt có tên file + số dòng | Do người viết prompt |

Gặp người dùng hỏi mấy thứ trên thì trả lời thẳng chứ đừng cố kéo vào script.
Việc duy nhất skill này làm được cho nhóm đó là **nhắc**: thấy trong phiên hiện
tại đã đọc rất nhiều file không liên quan nhau, hoặc đã chuyển hẳn sang task
khác, thì nói ra rằng `/clear` lúc này rẻ hơn là đi tiếp.

Còn khi phiên sắp cạn mà task **chưa xong** — đó là `session-handoff`, không
phải skill này.
