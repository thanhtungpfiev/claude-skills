---
name: raw-to-note
description: >
  Biến một khối dữ liệu thô — chat Teams dán vào note, tài liệu web/Confluence
  copy về, transcript Udemy/YouTube, hoặc file thô rời (.txt/.srt/.vtt/.md) —
  thành note kiến thức viết lại theo khuôn vault, rồi xoá bản thô. Dùng khi
  người dùng nói "dọn chỗ này", "chắt lọc đoạn này", "tôi vừa dán transcript
  vào", "biến đống này thành note", "làm gọn đoạn paste", "note hoá cái này";
  hoặc khi thấy trong một note có khối còn nguyên timestamp, tên người nói,
  breadcrumb điều hướng, nút "Edit this page", hay câu vỡ kiểu speech-to-text.
---

# Chắt lọc dữ liệu thô thành note

Bản thô **bị xoá hẳn** sau khi chắt lọc — note chỉ giữ lại phần đã viết lại cộng
một dòng nguồn. Điều đó làm mọi thứ bỏ sót thành mất vĩnh viễn, và nó quyết định
toàn bộ trình tự của skill này:

> **chốt nguồn → chọn note đích → viết → kiểm → mới xoá thô**

Đảo thứ tự, hay gộp bước cuối vào bước viết, là cách duy nhất để mất dữ liệu ở
đây. Không có bước nào tốn thời gian, chỉ có bước bị bỏ.

## Ba luật cứng

1. **Chưa chốt được định danh nguồn thì chưa xoá dòng thô nào.** Xem Bước 0.
2. **Chỉ xoá thô sau khi note đích đã ghi xong và đọc lại một lượt.** Không xoá
   "dọn đường" trước cho dễ nhìn.
3. **Không tự sửa thứ nghe/đọc không rõ.** Đánh `❓` và để nguyên chữ như nguồn.
   Xem Bước 4.

## Bước 0 — Nguồn này tra ngược bằng gì?

Trước khi đọc nội dung, trả lời: *sáu tháng nữa muốn xem lại câu gốc thì mở cái
gì?* Định danh tối thiểu theo từng loại:

| Nguồn | Định danh tối thiểu |
|---|---|
| Chat Teams | Link tin nhắn (chuột phải → *Copy link*). Không lấy được thì: tên kênh/nhóm + ngày + người nói |
| Trang web, Confluence/Docupedia | URL đầy đủ **+ ngày truy cập** — trang nội bộ bị sửa liên tục, URL không kèm ngày là nguồn nửa vời |
| Udemy, YouTube | Tên khoá + số và tên bài + mốc phút cho những ý quan trọng |
| File rời | Tên file gốc + nó từ đâu ra (ai gửi, tải ở đâu) |

**Không đủ định danh thì hỏi người dùng, đừng xoá và đừng tự bịa URL.** Một link
đoán chừng còn tệ hơn không có link: nó trông như đã kiểm chứng.

## Bước 1 — Loại nguồn quyết định cái gì là rác

Ba loại hay gặp. Cột thứ ba là phần dễ mất nhất, đọc kỹ trước khi cắt:

| Loại | Rác — cắt sạch | Giữ bằng mọi giá |
|---|---|---|
| **Chat Teams** | Dòng tên + timestamp, "Reacted with 👍", "1 reply", "Edited", chữ ký, phần quote lồng lặp lại nội dung đã có ở trên | **Ai** chốt quyết định — quyết định của người khác là dữ kiện có chủ thể, viết trống chủ ngữ là biến nó thành ý kiến của chính bạn.<br>Mọi lệnh, đường dẫn, tên biến, số hiệu ticket nguyên văn.<br>Câu hỏi chưa được trả lời — ghi lại kèm `❓`, đó là việc còn treo |
| **Transcript Udemy/YouTube** | Timestamp đầu dòng, từ đệm ("okay so", "right"), câu lặp lại y hệt, câu chào/quảng cáo khoá học | Tên API, tên lệnh, tên file hiện trên màn hình — **speech-to-text sai chính những chỗ này** (`flutter pub get` ra "flutter pop get"). Nghi ngờ thì `❓`, tuyệt đối không "sửa cho đúng" theo trí nhớ.<br>Thứ tự các bước trong demo — đó chính là nội dung |
| **Web / Confluence / Docupedia** | Breadcrumb điều hướng, "Edit this page", "Last modified by", menu bên, footer, nút Export | Bảng — copy từ web hay vỡ cột; dựng lại bảng Markdown đủ cột **và** dòng ngăn cách `\|---\|`.<br>Link tương đối (`/display/SET/...`) — nối lại thành URL tuyệt đối, không thì nó gãy ngay khi rời trang gốc |

## Bước 2 — Chọn note đích, và nói ra trước khi ghi

1. Tìm trong vault xem chủ đề này đã có note chưa — grep tên khái niệm chính,
   xem thư mục kiến thức của project đang làm.
2. **Có note rồi** → gộp vào đúng mục của nó, đừng tạo note thứ hai cùng chủ đề.
   Hai note cùng nói một thứ chắc chắn lệch nhau sau vài lần sửa.
3. **Chưa có** → note mới, đặt cùng thư mục với các note cùng loại.
4. **Nói cho người dùng biết đã chọn gì và vì sao, trước khi ghi** — một câu là
   đủ. Đây là quyết định dễ sai nhất và rẻ nhất để sửa nếu sai sớm.

## Bước 3 — Khuôn note lấy từ note anh em, không tự sáng tác

Mở **hai note cùng thư mục** và bám theo: dòng breadcrumb đầu file, kiểu heading
(có emoji hay không), thứ tự các mục, mục `## 🔗 Liên quan` cuối file. Vault đã
có kiểu của nó rồi; một note lạc khuôn đọc như note đi mượn.

- Mọi liệt kê áp skill [[list-formatting]] — nối ngang bằng `·`, xuống bullet,
  hay `<br>` trong ô bảng, theo luật ở đó chứ không theo cảm tính.
- Thuật ngữ viết song ngữ `english (tiếng việt)` ở lần xuất hiện đầu.
- Liên kết ra note đã có bằng `[[wikilink]]`. Link tới note **chưa tồn tại** thì
  được, nhưng phải nói ra ở phần báo cáo — nó là ghi chú "còn phải viết", không
  phải lỗi, nhưng cũng không phải thứ để người dùng tự phát hiện.

## Bước 4 — Lời nguồn và lời mình không được lẫn vào nhau

| Loại nội dung | Viết thế nào |
|---|---|
| Suy ra từ nguồn | Văn thường, không đánh dấu gì |
| Bổ sung ngoài nguồn (giải thích, bối cảnh, định nghĩa nguồn cho là ai cũng biết) | Callout gập sẵn `> [!info]- Ngoài nguồn` — hoặc `*(ngoài nguồn)*` nếu chỉ một cụm ngắn |
| Nguồn nói mơ hồ, nghe không rõ, mâu thuẫn | `❓` ngay tại chỗ, kèm nguyên văn chỗ ngờ |

Được phép bổ sung, nhưng **không được để phần bổ sung trông giống lời nguồn**.
Bản thô đã xoá — sau này không còn cách nào phân biệt ngoài dấu vừa đánh.

## Bước 5 — Kiểm, rồi mới xoá thô

Rà đủ bốn thứ này trước khi động vào khối thô:

- [ ] **Dòng nguồn có mặt** trong note đích, đúng định danh chốt ở Bước 0.
- [ ] **Không còn rác sót**: grep note đích tìm `\d\d:\d\d`, "Reacted", "reply",
      "Edit this page". Sót một timestamp nghĩa là còn sót cả đoạn quanh nó.
- [ ] **Bảng nào cũng có dòng ngăn cách** ngay dưới header, và **không có dòng
      trống giữa hai dòng của cùng một bảng** — Markdown đóng bảng tại dòng
      trống, phần sau đổ ra chữ thô kèm nguyên dấu `|`. Đọc file raw vẫn thấy
      thẳng hàng nên lỗi chỉ lộ khi mở Obsidian.
- [ ] **Đọc lại note đích một lượt như người chưa biết gì** — chỗ nào không hiểu
      thì nguồn còn đó để mở lại, sau khi xoá thì không.

Xong bốn mục mới xoá khối thô. Rồi **báo lại**: viết vào note nào, thêm mục gì,
những `❓` nào còn treo, những `[[wikilink]]` nào trỏ note chưa tồn tại.

## Red flags — dừng lại nếu bắt gặp mình đang nghĩ thế này

| Ý nghĩ | Thực tế |
|---|---|
| "Xoá bớt rác trước cho dễ đọc rồi viết sau" | Đó là xoá trước khi có bản thay thế. Viết xong mới xoá. |
| "Link nguồn chắc là cái URL này" | Chắc là ≠ đúng. Hỏi. |
| "Chỗ này nó nói nhầm, sửa lại cho đúng" | Bạn đang sửa theo trí nhớ của mình, không theo nguồn. `❓`. |
| "Ai nói câu này không quan trọng" | Với một quyết định thì chủ thể *là* nội dung. |
| "Đoạn này chỉ là chào hỏi, cắt cả cụm cho nhanh" | Câu chốt hay nằm lẫn trong đoạn tán gẫu. Đọc hết rồi mới cắt. |
| "Note kia cũng nói về cái này, nhưng tạo note mới gọn hơn" | Hai note cùng chủ đề rồi sẽ lệch nhau. Gộp. |
| "Chủ đề này tôi biết, viết thẳng cho đầy đủ" | Thành ra lời mình đội lốt lời nguồn. Callout *Ngoài nguồn*. |

## Khi kho note không phải vault Obsidian

Phần dùng được ở mọi nơi là Bước 0, 1, 4, 5 — chốt nguồn, biết cái gì là rác,
tách lời nguồn khỏi lời mình, kiểm trước khi xoá. Riêng `[[wikilink]]`, callout
`> [!info]`, và cách chọn note đích theo thư mục là đặc thù Obsidian: gặp repo
markdown thường thì đổi sang link tương đối và blockquote thường, giữ nguyên
phần còn lại.

Quy ước riêng của từng vault — đặt note ở đâu, breadcrumb viết thế nào, ngôn ngữ
note — thuộc về `CLAUDE.md` của repo đó, không thuộc skill này.
