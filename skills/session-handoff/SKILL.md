---
name: session-handoff
description: >
  Viết bản bàn giao để cắt một phiên Claude Code đang nặng context rồi mở phiên
  mới làm tiếp mà không mất tiến độ — và chia sẵn một việc lớn thành chuỗi
  phiên chuyên biệt (khám phá → lập kế hoạch → thực thi). Dùng khi người dùng
  nói "phiên này sắp đầy", "bàn giao đi", "context gần hết mà chưa xong",
  "chuyển sang phiên mới", "Claude bắt đầu quên rồi", "session handoff", "tách
  việc này ra nhiều phiên"; hoặc khi thấy Claude sửa file mà không đọc trước,
  đề xuất ngược với thứ vừa thống nhất, hỏi lại thứ đã giải thích. KHÔNG dùng
  để rà cấu hình repo cho gọn context — việc đó là `token-audit`.
---

# Bàn giao phiên — cắt context mà không cắt tiến độ

Phiên càng dài, chất lượng càng giảm: model bắt đầu bỏ sót chi tiết, đề xuất
ngược thứ vừa chốt, hỏi lại thứ đã giải thích. Đến lúc đó, cố đi tiếp là vừa đắt
vừa kém — mỗi request nạp lại toàn bộ lịch sử, mà phần lịch sử đó đang khiến
model tệ đi chứ không giúp gì.

Lối thoát không phải `/clear` rồi kể lại từ đầu. Là **viết một bản bàn giao đủ
để phiên mới bắt việc ngay**, rồi `/clear`.

## Khi nào bàn giao, khi nào chỉ cần `/compact` hay `/clear`

Chọn sai thì hoặc mất context cần thiết, hoặc giữ lại đống rác đang làm hỏng
phiên. Ba tình huống khác hẳn nhau:

| Tình huống | Dùng | Vì sao |
|---|---|---|
| Chuyển sang task **không liên quan** | `/clear` | Không có gì đáng mang sang, viết bàn giao chỉ là công thừa |
| Task **vẫn tiếp tục**, context nặng nhưng model còn tỉnh | `/compact <hướng dẫn cụ thể>` | Rẻ hơn, không đứt mạch. Nén kèm chỉ dẫn (`/compact tập trung vào module auth và kết quả test`) giữ được nhiều hơn `/compact` trơn |
| Claude vừa **đi sai hướng** vài lượt | `/rewind` | Xoá luôn mấy lượt thử hỏng. Chúng làm ô nhiễm context — để lại thì model vẫn bị chúng dẫn dắt |
| Task **chưa xong** mà context đã nặng, hoặc thấy dấu hiệu model đang quên | **Skill này** | Cần một bản tóm tắt do người đọc được, không phải bản nén máy đọc |

Khác biệt so với `/compact`: bản nén chỉ nhắm cho Claude đi tiếp **trong cùng
phiên**. Bản bàn giao viết cho **cả người lẫn máy** — bạn đọc để biết đang ở
đâu, phiên mới đọc để làm tiếp, và nó là file trên đĩa nên sống qua cả lúc máy
tắt.

## Cấu trúc bắt buộc — bảy mục, đủ cả bảy

Script kiểm chứng đòi đúng bảy nhãn này, viết `**Nhãn:**` hoặc `## Nhãn` đều
được:

```markdown
# Bàn giao phiên — <chủ đề> — <YYYY-MM-DD>

**Mục tiêu:** một câu — đang cố đạt cái gì, và xong là thế nào.

**Trạng thái:** xong / đang làm / bị chặn — kèm một câu vì sao.

**Quyết định đã chốt:**
- <quyết định> — vì <lý do>
- ...

**File đã sửa:**
- `đường/dẫn/thật.py` — đã đổi cái gì
- ...

**Bước tiếp theo:**
1. <bước cụ thể, làm được ngay>
2. ...

**Câu hỏi còn treo:** ❓ <thứ chưa quyết được, cần người trả lời>

**Mở đầu phiên mới:**
> <câu nguyên văn để dán vào phiên mới>
```

Bốn luật khiến bản bàn giao dùng được thay vì chỉ đọc cho vui:

1. **"Quyết định đã chốt" phải kèm lý do.** Không có lý do thì phiên mới sẽ mở
   lại đúng cuộc tranh luận vừa xong — và lần này không còn dữ kiện để cãi.
   Đây là mục đắt nhất của cả bản bàn giao: nó là thứ duy nhất `git diff` không
   phục hồi được.
2. **"File đã sửa" ghi đường dẫn thật trong backtick**, không phải "vài file
   trong module auth". Phiên mới không có cách nào đoán ra.
3. **Không dán code.** Trỏ `file.py:88` là đủ — phiên mới đọc được file. Dán
   code vào là dựng lại đúng cái context vừa bỏ đi, chỉ khác là bằng tay.
4. **"Mở đầu phiên mới" viết ở ngôi thứ hai, dán là chạy.** Không phải mô tả
   ("phiên sau nên đọc file này"), mà là câu lệnh thật ("Đọc
   `docs/handoff.md`, làm tiếp bước 1, đừng đụng vào `src/legacy/`").

Chỗ nào không chắc thì đánh `❓` và cho vào "Câu hỏi còn treo" — **đừng đoán
hộ**. Một câu đoán bừa nằm trong bản bàn giao sẽ được phiên mới đọc như sự thật
đã chốt, và không có gì báo là nó sai.

## Các bước

### 1. Chọn chỗ lưu

Mặc định `docs/session-handoff.md` trong repo đang làm. Repo không có `docs/`
thì để ở gốc. Nhiều phiên nối nhau thì đánh số theo giai đoạn
(`docs/handoff-01-discovery.md`) chứ đừng ghi đè — bản cũ là thứ duy nhất giải
thích vì sao bước sau lại làm thế.

Nếu file bàn giao **không** nên vào git (chứa ghi chú nháp), thêm nó vào
`.gitignore` rồi nói cho người dùng biết, đừng lặng lẽ tạo file lạ trong repo
của họ.

### 2. Viết, đọc lại phiên chứ đừng viết theo trí nhớ

Rà lại phiên hiện tại để lấy: quyết định nào đã chốt (và lý do), file nào đã
thật sự sửa, test chạy lần cuối ra sao. Đây là chỗ hay sai nhất — viết theo cảm
giác thì dễ ghi cả những thứ mới chỉ **bàn tới** thành đã chốt.

### 3. Kiểm chứng — bắt buộc

```bash
python scripts/verify_handoff.py docs/session-handoff.md [gốc-repo]
```

Báo FAIL cho: thiếu mục, mục để trống, placeholder chưa điền, đường dẫn trong
"File đã sửa" không tồn tại, bản bàn giao dài quá 150 dòng, hay có quá 40 dòng
code block. Thoát mã 1 nếu có vấn đề.

Kiểm đường dẫn **chỉ áp cho mục "File đã sửa"**, không áp cho "Bước tiếp theo"
— bước tiếp theo hoàn toàn có quyền nhắc file sắp tạo. Một script hay báo sai
thì lần sau không ai chạy nữa, nên chỗ này cố ý hẹp.

Sửa tới khi PASS rồi mới báo xong. Đừng tự đọc lướt rồi kết luận "ổn rồi" — mục
để trống và placeholder sót lại là hai lỗi mắt người bỏ qua nhiều nhất, vì lúc
vừa viết xong bạn vẫn còn nhớ nội dung đáng lẽ phải nằm ở đó.

### 4. Bàn giao cho người dùng, đừng tự `/clear`

In đường dẫn file và **khối "Mở đầu phiên mới"** ra thẳng câu trả lời, rồi nói:
gõ `/clear` (hoặc mở phiên mới) và dán khối đó vào. `/clear` là lệnh của người
dùng — Claude không tự gọi được, và cũng không nên: người dùng có thể còn muốn
hỏi thêm gì đó trước khi cắt.

## Chuỗi phiên: chia trước, đừng đợi tới lúc cạn

Việc lớn thì đừng nhét vào một phiên khổng lồ rồi bàn giao khi đã hết chỗ. Chia
từ đầu, mỗi phiên đúng một mục tiêu, output phiên trước là input phiên sau:

| Phiên | Làm gì | Kết thúc bằng |
|---|---|---|
| **Khám phá** | Đọc code, hiểu kiến trúc hiện tại. **Không sửa gì.** | `discovery-notes.md` → `/clear` |
| **Lập kế hoạch** | Nạp `discovery-notes.md`, ra kế hoạch từng bước, đánh dấu chỗ rủi ro | `refactor-plan.md` → `/clear` |
| **Thực thi** | Nạp `refactor-plan.md` (không cần code thô của phiên 1), làm từng bước, tick xong | Cập nhật lại plan |

Cái hay không nằm ở chỗ chia nhỏ, mà ở chỗ **mỗi phiên bắt đầu bằng context
sạch chỉ chứa đúng thứ nó cần**. Phiên thực thi nhận kế hoạch đã lọc, không dính
đống file thô mà phiên khám phá phải đọc để viết ra kế hoạch đó.

Đáng chia khi: việc ước chừng trên 45 phút, hoặc có nhiều giai đoạn khác chất
(nghiên cứu / lập kế hoạch / làm / rà), hoặc phải đọc nhiều file lớn. Việc dưới
~20 lượt trao đổi thì chia chỉ tổ thêm thủ tục.

## Dấu hiệu phải bàn giao mà người dùng chưa nhận ra

Nếu trong phiên hiện tại thấy mấy dấu hiệu này thì **nói ra**, đừng đợi được
hỏi — người dùng thường không thấy chúng vì đang bám theo nội dung công việc:

- Sửa file mà không đọc lại trước.
- Đề xuất thứ ngược với điều đã thống nhất mươi lượt trước.
- Hỏi lại thứ đã được giải thích rồi.
- Câu trả lời ngắn và nông dần đi so với đầu phiên.

Đề nghị bàn giao lúc đó rẻ hơn nhiều so với sửa hậu quả của một quyết định sai
do model đã quên mất ràng buộc.
