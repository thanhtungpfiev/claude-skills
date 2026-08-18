---
name: list-formatting
description: >
  Chọn đúng hình thức cho một danh sách trong Markdown — nối ngang bằng dấu `·`,
  xuống bullet list, hay xếp chồng bằng `<br>` trong ô bảng. Dùng khi viết hoặc
  sửa note/tài liệu Markdown có liệt kê, khi gom nhiều ý vào một dòng, khi thấy
  một dòng dài khó quét mắt, hoặc khi người dùng nói "gom lại", "tách ra",
  "dòng này dài quá", "rà lại format danh sách".
---

# Định dạng danh sách trong Markdown

Một danh sách có hai hình thức: **ngang** (các mục nối trên cùng một dòng) và **dọc**
(mỗi mục một dòng). Chọn sai hình thức là lỗi hay gặp nhất khi viết tài liệu — và nó
luôn nghiêng về một phía: gom quá tay, biến một checklist thành khối chữ liền.

## Luật quyết định

Đo **mục dài nhất** trong danh sách, rồi chọn:

| Mục dài nhất | Hình thức | Ví dụ |
|---|---|---|
| ≤ ~5 từ, không có mệnh đề phụ | **Ngang**, nối bằng ` · ` | `timestamp · tên event · tóm tắt` |
| Dài hơn, hoặc có ngoặc/mệnh đề giải thích riêng | **Dọc**, bullet list | mỗi ý một dòng `- ` |
| Dọc nhưng đang nằm trong ô bảng | Xếp chồng bằng `<br>` | `**Nhãn** — giải thích<br>**Nhãn** — …` |

Đo theo **mục**, không theo cả dòng. Một dòng 300 ký tự mà các mục đều 2–3 từ thì vẫn
đúng; một dòng 120 ký tự gồm hai mệnh đề thì đã sai.

**Vì sao:** `·` là dấu phân cách *ngang hàng, đọc một nhịp* — mắt lướt qua và nhặt được
cả bộ. Khi mỗi mục cần dừng lại để đọc hiểu, việc nối ngang buộc người đọc phải tự tách
danh sách bằng đầu, đúng phần việc mà bullet list làm sẵn. Nó cũng xoá mất khả năng đánh
dấu vị trí: không thể trỏ "ý thứ tư" trong một khối chữ liền.

## Khi nào KHÔNG tách

Đừng máy móc theo số ký tự. Giữ nguyên hình thức ngang cho:

- **Danh sách link** — `[[wikilink]]`, URL, tên repo. Dài về ký tự nhưng render ra là chip
  ngắn; xuống dòng chỉ làm loãng.
- **Tên lệnh, giá trị enum, đường dẫn file** — `allow · deny · ask`, `.claude/settings.json
  · ~/.claude/settings.json`.
- **Câu văn xuôi có kèm một danh sách ngắn ở giữa.** Phần dài thường nằm *sau* dấu `·`
  cuối cùng, không phải là một mục. `(timestamp · tên event · tóm tắt), gồm việc nạp
  customization ban đầu…` — danh sách ở đây hoàn toàn ổn.

## Cùng lỗi, khác dấu

Dấu `·` chỉ là hình thức dễ thấy nhất. Cùng một lỗi gom ngang còn mặc những áo sau, và
chúng thoát khỏi mọi lệnh rà chỉ tìm `·`:

- **Đánh số ngang** — `…2 vấn đề: (1) chat dài dễ tràn context window; (2) các bước fix
  sau bị pollute bởi context của bước trước…`. Đã đánh số tức là tác giả tự thấy đây là
  danh sách; chỉ còn thiếu mỗi việc cho nó xuống dòng.
- **Chuỗi mũi tên** — `paste lệnh → chọn agent đích (…) → chọn scope: … → chọn cách cài
  (…)`. Đây là **quy trình nhiều bước**, mỗi bước lại kèm lựa chọn riêng; để ngang thì
  không đánh dấu được đang làm tới bước nào.
- **Dấu phẩy nối các thành phần có giải thích** — `folder riêng, bắt buộc có skill.md với
  frontmatter name + description (…), có thể kèm scripts/ (…) và references/ (…)`.
- **Gạch chéo cho các lựa chọn** — `yes / yes + remember (khỏi hỏi lại) / no (thoát)`.
  Ca này thường **vẫn ổn** vì mỗi lựa chọn chỉ 1–3 từ; chỉ tách khi phần trong ngoặc dài ra.

Phân biệt với ca **không** phải danh sách: một đoạn văn xuôi dài là chuyện bình thường và
đừng đụng vào. Câu hỏi để phân định không phải "dòng này dài bao nhiêu" mà **"đây có phải
mấy mục ngang hàng bị nhét chung một dòng không"**.

## Cách chuyển

**Trong thân bài / blockquote** — đổi ` · ` thành `- `, mỗi mục một dòng. Nếu đang nằm
trong list đánh số thì thụt vào 4 space cho khớp bề rộng marker:

```markdown
> 4. **Chọn cách build** — sau khi duyệt plan có 3 nút:
>     - **Start Implementation** — default approvals
>     - **Start with Autopilot** — không dừng giữa các bước
```

Phần văn xuôi đi kèm sau danh sách thì tách thành đoạn riêng, cách bằng một dòng `>` rỗng
và thụt cùng mức — nếu viết nối luôn vào mục cuối, nó bị đọc thành một phần của mục đó.

**Trong ô bảng** — Markdown không cho xuống dòng bằng `-`, dùng `<br>`. Nhân dịp đó đổi
`**Nhãn** (giải thích)` thành `**Nhãn** — giải thích`: bỏ được cặp ngoặc mà vẫn rõ ranh
giới, vì mỗi mục đã có dòng riêng.

```markdown
| **Scope** | **This session** — hết phiên chat hiện tại<br>**This workspace** — còn với dự án |
```

**Khi mục cuối có đuôi văn xuôi** — đừng biến đuôi đó thành một mục. Chấm câu trước, đưa
đuôi xuống câu riêng:

```markdown
Dùng khi: thử A · so sánh B · test C.
→ Mạnh dạn thử nghiệm hơn vì luôn rẽ nhánh được.
```

## Rà lại tài liệu đã viết

Đếm số mục dài trong từng dòng, chỉ báo dòng có **từ 2 mục dài trở lên** — ngưỡng này lọc
được phần lớn dương tính giả:

```bash
grep -rn "·" --include="*.md" . | awk -F'·' '{
  cnt=0
  for(i=1;i<=NF;i++){
    s=$i
    if(i==1){ sub(/^.*: /,"",s); sub(/^.*— /,"",s) }   # bỏ phần dẫn trước danh sách
    sub(/\. .*$/,"",s); sub(/\|.*$/,"",s)              # bỏ văn xuôi sau khi hết danh sách
    if(length(s)>50) cnt++
  }
  if(cnt>=2) print
}'
```

**Kết quả là danh sách nghi vấn, không phải danh sách phải sửa.** Luôn đọc từng dòng rồi
mới quyết — heuristic không phân biệt được link dài với mệnh đề dài, và nó tính cả câu văn
xuôi đứng sau dấu `·` cuối cùng. Hạ `cnt>=2` xuống `cnt>=1` để quét rộng hơn, đổi lại
nhiễu tăng đáng kể.

Đánh số ngang thì bắt bằng một lệnh riêng, rẻ và gần như không có nhiễu:

```bash
grep -rn "(1).*(2)" --include="*.md" .
```

**Chuỗi mũi tên và dấu phẩy nối thì không có lệnh nào bắt được** — nhiễu áp đảo tín hiệu.
Chỉ còn cách đọc. Vì vậy khi được giao "rà lại toàn bộ", đừng dừng ở việc chạy grep: grep
xong là mới xong phần dấu `·` và `(1)(2)`, phần còn lại vẫn phải mở từng file ra đọc. Nói
rõ ranh giới đó trong báo cáo thay vì để người đọc tưởng đã quét hết.

Sửa xong thì chạy lại các lệnh trên để xác nhận phần còn sót đều là ca cố ý giữ, và nói rõ
những dòng nào đã chừa lại cùng lý do.

## Dấu phân cách nào

`·` (U+00B7, interpunct) là mặc định: nhẹ hơn dấu phẩy về thị giác nên không lẫn khi bản
thân các mục đã chứa dấu phẩy. Đổi lại nó khó gõ và không phải quy ước Markdown chuẩn.

Khi các mục ngắn tới mức không thể nhầm lẫn, **dấu phẩy thường vẫn tốt hơn** — đừng dùng
`·` chỉ vì nó trông gọn. Trong một tài liệu, chọn một dấu rồi giữ nguyên; trộn `·` với `|`
với `•` khiến người đọc đi tìm ý nghĩa của sự khác biệt vốn không tồn tại.
