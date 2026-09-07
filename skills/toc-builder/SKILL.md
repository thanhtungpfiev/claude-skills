---
name: toc-builder
description: >
  Dựng mới hoặc chuẩn hoá khối "## 📑 Mục lục" trong một note Obsidian nhiều
  chương (kiểu tóm tắt khóa học, hub tổng hợp) — bullet list dọc theo nhóm
  Chương/Hình/Mã màu, mỗi mục là wikilink `[[#heading|nhãn]]` trỏ thẳng heading
  thật. Dùng khi người dùng nói "mục lục note này không giống mấy note kia",
  "rà lại mục lục", "note này thiếu mục lục", "chuẩn hoá mục lục", "table of
  contents", hoặc khi vừa thêm/xoá/đổi tên một heading `##`/`### Hình N` và cần
  kiểm mục lục còn khớp không. KHÔNG dùng cho note detail 4 phần (Nó làm gì? /
  Tại sao? / Dùng thế nào? / Cài thế nào?) — note đó không cần mục lục.
---

# Dựng & chuẩn hoá mục lục note

Mọi note nhiều chương trong vault (`D:\MyLifeExperience`) — chủ yếu là note tóm
tắt khóa học và note hub tổng hợp lĩnh vực — dùng chung một kiểu mục lục để đọc
lướt được và để wikilink không âm thầm gãy khi note dài ra. Skill này làm hai
việc: **dựng mới** khối đó cho note chưa có, và **rà lại** khối đã có cho khớp
heading thật — đúng việc vừa làm tay với note `Claude Code - The Practical
Guide.md` (đối chiếu nó và `VSC Learn Hub.md` / `VSC Youtube Channel.md` làm ví
dụ tham khảo bất cứ khi nào cần xem một mục lục "chuẩn" trông ra sao).

## Trước tiên: note này có cần mục lục không?

Không phải note dài nào cũng cần. Vault có hai loại note khác hẳn kết cấu:

| Loại note | Kết cấu | Có mục lục không |
|---|---|---|
| **Nhiều chương** — tóm tắt khóa học, hub tổng hợp | Nhiều heading `##` (chương/phần), thường có heading `### Hình N` | **Có** — đây là đối tượng của skill này |
| **Detail 4 phần** — giới thiệu một repo/công cụ | Đúng 4 heading `##`: Nó làm gì? / Tại sao tôi cần quan tâm? / Dùng thế nào? / Cài thế nào? | **Không** — 4 phần ngắn, đọc liền mạch, thêm mục lục chỉ thành thừa |

Chạy `scripts/extract_headings.py` trước (xem bước 1) — nếu ra dưới ~5–6
heading `##` và khớp bố cục 4 phần, dừng lại và nói cho người dùng biết note
này không thuộc diện cần mục lục, đừng tự thêm.

## Kiểu chuẩn — bám đúng, đừng tự sáng tác biến thể

Khối nằm ngay dưới `## 📑 Mục lục`, cách phần trên (callout Tổng quan) và phần
dưới (chương đầu tiên) bằng một dòng trống rồi `---`.

````markdown
## 📑 Mục lục

**Chương**

- [[#⬛ Chương 0 — Chuẩn bị & Terminal|⬛ Ch.0 — Chuẩn bị & Terminal]] — chuẩn bị & chọn terminal
- [[#🟦 Chương 1 — Sử dụng cơ bản|🟦 Ch.1 — Sử dụng cơ bản]] — prompt đầu tiên · tích hợp VS Code
- [[#🔗 Liên quan|🔗 Liên quan]] — các note khác trong vault

**Hình**

- [[#Hình 1 — Thang cấp quyền Claude Code|Hình 1]] — default → accept edits → bypass permissions (Ch.2)

**Mã màu** — dùng chung ở mọi hình: **cyan** người dùng còn quyền · **hồng** Claude tự hành động · **đỏ** rủi ro cao nhất
````

Bốn điểm bắt buộc, đúng thứ tự này không phải tuỳ hứng:

1. **`**Chương**` đứng riêng một dòng, rồi xuống bullet list dọc.** Không nối
   ngang bằng `·` như kiểu cũ (`Ch.0 · Ch.1 · Ch.2 …`) — kiểu đó chỉ ra được
   nhãn rút gọn, không ra mô tả, người đọc phải mở từng chương mới biết trong
   đó có gì. Đây là quyết định của [[list-formatting]] áp cho danh sách có mô
   tả dài kèm theo: xuống bullet.
2. **Mọi heading `##` đều có mặt, kể cả heading không phải "Chương N"** — mục
   dẫn nhập, phụ lục, "🔗 Liên quan" ở cuối. Bỏ sót một heading `##` nào khỏi
   mục lục là để nó thành mồ côi, người đọc không có đường bấm tới.
3. **`**Hình**` là khối riêng**, chỉ liệt các heading `### Hình N — …` — không
   liệt các heading `###` khác (heading con trong chương không có mục lục
   riêng, đọc trong outline pane của Obsidian là đủ).
4. **`**Mã màu**` gọi tên màu bằng chữ** (cyan, hồng, cam, tím, lá, đỏ...),
   **không in mã hex** — mã hex đã gắn cứng theo vai trò trong skill
   `diagram-rules`, lặp lại ở đây là hai chỗ cùng một sự thật, dễ lệch khi một
   nơi đổi mà nơi kia quên.

Nhãn rút gọn trong `[[#heading|nhãn]]` (`⬛ Ch.0 — Chuẩn bị & Terminal`) là tuỳ
chọn — mục đích chỉ để dòng bullet không bị lặp lại y hệt heading đầy đủ khi nó
quá dài; note ngắn hoặc heading đã ngắn thì để nhãn trùng heading cũng được,
như `VSC Learn Hub.md` đang làm.

### Callout "Tổng quan" phía trên: rút gọn nếu đang trùng mục lục

Một số note cũ có callout Tổng quan liệt kê mô tả từng chương (thường dưới tên
"Lộ trình note"). Một khi mục lục đã có mô tả đó, giữ nguyên callout là **hai
chỗ cùng mô tả một thứ** — chắc chắn lệch nhau sau vài lần sửa, đúng lý do
CLAUDE.md của vault cấm việc này giữa note index và note detail. Gặp callout
kiểu đó: rút còn 1–2 câu tóm tắt mạch note (đi từ đâu tới đâu), dời hết mô tả
chi tiết xuống mục lục. Callout đã ngắn sẵn (như `VSC Learn Hub.md`) thì để
nguyên, không việc gì phải đụng vào.

## Các bước

### 1. Lấy khung sườn heading — đừng tự đọc lại cả file để dò

```bash
python scripts/extract_headings.py "<đường dẫn note.md>"
```

In ra mọi heading `##`/`###` thật theo đúng thứ tự file (bỏ qua frontmatter và
nội dung trong code fence), đánh dấu heading nào thuộc nhóm `[Chương]` hay
`[Hình]`, và nếu note đã có `## 📑 Mục lục` thì in luôn wikilink đang có trong
đó. Dùng bản in này làm khung — việc còn lại chỉ là viết mô tả 1 dòng cho từng
mục, không cần tự đọc lại toàn file để tìm heading.

### 2. Soạn mô tả từng chương/hình

Đây là phần duy nhất cần đọc nội dung: mở từng chương, tóm còn 1 dòng — theo
[[list-formatting]], nối các ý con bằng `·` nếu ý ngắn, xuống câu riêng nếu ý
dài. Ưu tiên **tái dùng nguyên văn** mô tả đã có sẵn trong note (callout Tổng
quan, hoặc mục lục cũ đang chuẩn hoá lại) thay vì viết lại từ đầu — vừa nhanh
hơn, vừa giữ đúng cách người viết note đã tự mô tả chương của họ.

### 3. Ráp khối theo đúng kiểu chuẩn, ghi đè khối cũ (nếu có)

Theo cấu trúc ở trên. Nếu note đã có `## 📑 Mục lục` kiểu cũ, thay nguyên khối
— từ dòng `## 📑 Mục lục` tới dòng `---` kế tiếp — chứ đừng chèn thêm khối mới
bên cạnh khối cũ.

### 4. Kiểm chứng — bắt buộc, đừng tự soi lại bằng mắt

```bash
python scripts/verify_toc.py "<đường dẫn note.md>"
```

Báo PASS/FAIL cho đúng 4 điều: heading `##`/`### Hình N` nào mồ côi (thiếu
trong mục lục), anchor nào trong mục lục gãy (trỏ heading không tồn tại), thứ
tự mục lục có khớp thứ tự file, và — quan trọng nhất — **toàn bộ `[[#...]]`
trong CẢ FILE** (không riêng khối mục lục) có còn khớp heading thật không.
Mục cuối bắt được thứ mắt thường bỏ sót: backlink `↑ [[#📑 Mục lục|Mục lục]]`
dưới mỗi hình, hay một tham chiếu chéo `[[#Ch.4]]` nằm tuốt cuối note, gãy
ngay khi một heading bị đổi tên mà không có gì báo hiệu.

Sửa tới khi script này sạch PASS rồi mới báo xong việc — đừng tự kết luận
"mục lục ổn" chỉ vì đọc lướt qua thấy hợp lý.

## Vì sao lại có `_tocsupport.py`, `extract_headings.py`, `verify_toc.py`

Đếm heading, khớp anchor, so thứ tự, dò link gãy toàn file — bốn việc này
100% cơ học, không cần phán đoán ngôn ngữ nào. Việc đáng ra phải tự viết lại
bằng một đoạn script dùng-một-lần mỗi khi rà một note (rất dễ quên một use
case, hoặc quên một chi tiết như `\|` trong ô bảng không phải escape giữ
nguyên ký tự mà là dấu phân cách wikilink bị escape để khỏi vỡ cột bảng — hai
script này đã xử lý đúng, không cần biết chi tiết đó mỗi lần chạy). Cố định
lại thành script nghĩa là mỗi lần gọi đều đúng như lần trước, không tốn công
suy luận lại logic, và không tốn token cho phần việc máy làm chính xác hơn.

## Khi note không nằm trong vault Obsidian này

Hai script trên chỉ hiểu wikilink kiểu `[[#heading]]` / `[[#heading|nhãn]]`
(Obsidian, Foam, Logseq đều dùng cú pháp này) — không tự sinh anchor kiểu
GitHub-flavored Markdown (`[nhãn](#heading-slug)`). Gặp một project markdown
dùng kiểu anchor đó thì báo cho người dùng biết giới hạn này thay vì tự chế ra
slug đoán chừng — sai một slug là sai âm thầm, không có gì báo như mục 4 ở
trên vẫn báo được với wikilink.
