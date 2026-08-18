# thanhtungpfiev-skills

Plugin Claude Code gói hai skill cá nhân dùng chung cho mọi repo.

## Nó làm gì?

| Skill | Nội dung |
|---|---|
| `commit` | Tách thay đổi thành từng commit một ý, viết message theo khung **Problem → Solution → Implications** — ghi lại *vì sao* repo tiến hoá, thứ mà diff không phục hồi được. Kích hoạt khi tạo commit, tách thay đổi, hay sửa message đã viết. |
| `list-formatting` | Chọn hình thức cho một danh sách trong Markdown: nối ngang bằng `·`, xuống bullet list, hay xếp chồng bằng `<br>` trong ô bảng. Luật quyết định dựa trên độ dài mục dài nhất. |

Cả hai đều **không dính quy ước riêng của repo nào**. Phần riêng — ngôn ngữ message, dạng
subject, đặc thù nội dung — mỗi repo tự khai trong `CLAUDE.md` của nó; skill `commit` đọc
phần đó và ghép vào khung chung.

## Tại sao tôi cần quan tâm?

Skill đặt trong `.claude/skills/` chỉ có hiệu lực cho đúng repo đó. Muốn dùng ở mọi
project thì phải symlink sang `~/.claude/skills/` bằng tay, và lặp lại thao tác đó trên
từng máy mới. Đóng thành plugin thì hai lệnh là xong, ở bất kỳ máy nào.

## Dùng thế nào?

Không phải gọi tay — skill tự kích hoạt theo mô tả trong frontmatter. Nói "commit giúp
tôi" thì `commit` được nạp; sửa một note Markdown có liệt kê thì `list-formatting` được nạp.

Muốn gọi thẳng:

```
/commit
/list-formatting
```

## Cài thế nào?

```
/plugin marketplace add thanhtungpfiev/claude-skills
/plugin install thanhtungpfiev-skills@thanhtungpfiev-skills
```

Trên máy dùng để **sửa** skill, trỏ marketplace vào bản clone local thay vì GitHub — sửa
file là có hiệu lực ngay, không phải push rồi update plugin:

```
/plugin marketplace add D:/PrivateDocuments/claude-skills
```
