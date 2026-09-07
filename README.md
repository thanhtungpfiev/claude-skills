# thanhtungpfiev-skills

Plugin Claude Code gói bảy skill cá nhân dùng chung cho mọi repo.

## Nó làm gì?

| Skill | Nội dung |
|---|---|
| `commit` | Tách thay đổi thành từng commit một ý, viết message theo khung **Problem → Solution → Implications** — ghi lại *vì sao* repo tiến hoá, thứ mà diff không phục hồi được. Kích hoạt khi tạo commit, tách thay đổi, hay sửa message đã viết. |
| `list-formatting` | Chọn hình thức cho một danh sách trong Markdown: nối ngang bằng `·`, xuống bullet list, hay xếp chồng bằng `<br>` trong ô bảng. Luật quyết định dựa trên độ dài mục dài nhất. |
| `diagram-rules` | Luật màu, font và kiểm chứng khi vẽ sơ đồ SVG bằng skill `diagram-design`: bảng màu Dracula **một bản tối**, mã màu **gắn cứng theo vai trò**, cấm Georgia vì thiếu dấu tiếng Việt, và cạm bẫy mask khi đổi font. Kèm sẵn file profile để dựng lại skin trên máy mới. |
| `toc-builder` | Dựng mới hoặc chuẩn hoá khối `## 📑 Mục lục` trong note nhiều chương: bullet list Chương/Hình/Mã màu, mỗi mục là wikilink trỏ heading thật. Kèm hai script kiểm chứng — heading mồ côi, anchor gãy, thứ tự lệch, wikilink gãy toàn file — chạy lại được thay vì tự soi bằng mắt mỗi lần. |
| `raw-to-note` | Chắt lọc một khối dữ liệu thô — chat Teams, tài liệu web/Confluence copy về, transcript Udemy — thành note kiến thức theo khuôn note anh em, rồi **xoá hẳn bản thô**. Vì bản thô không giữ lại, trình tự là luật: chốt định danh nguồn → chọn note đích → viết → kiểm → mới xoá. Phần Claude tự bổ sung nằm trong callout riêng, chỗ nguồn mơ hồ đánh `❓` chứ không đoán hộ. |
| `token-audit` | Soi phần token **cố định** của một repo: CLAUDE.md có vượt 200 dòng không, thư mục nặng có thật sự bị `.gitignore` chặn không (hỏi `git check-ignore` chứ không grep), `settings.json` có ghim model và chặn đọc `.env` chưa. Bắt luôn mấy key ma lan truyền qua blog — `smallModelOverride`, `.claudeignore` — đặt vào thì không báo lỗi mà cũng không có tác dụng. |
| `session-handoff` | Viết bản bàn giao bảy mục để cắt một phiên đang nặng context rồi mở phiên mới làm tiếp mà không mất tiến độ, và chia việc lớn thành chuỗi phiên khám phá → lập kế hoạch → thực thi. Kèm script kiểm: thiếu mục, placeholder sót, đường dẫn ghi sai, bàn giao phình quá dài. |

Cả bảy đều **không dính quy ước riêng của repo nào**. Phần riêng — ngôn ngữ message, dạng
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
/toc-builder
/raw-to-note
/token-audit
/session-handoff
```

## Cài thế nào?

```
/plugin marketplace add thanhtungpfiev/claude-skills
/plugin install thanhtungpfiev-skills@thanhtungpfiev-skills
```

Trên máy dùng để **sửa** skill, trỏ marketplace vào bản clone local thay vì GitHub — khỏi
phải push mới thử được. Đường dẫn tuỳ máy, không phải quy ước cố định — mỗi máy tự
`git clone` repo này vào đâu tuỳ ý, rồi trỏ đúng vào đó:

```
/plugin marketplace add <đường-dẫn-bản-clone-local-trên-máy-này>
```

Lưu ý: kể cả với nguồn local, Claude Code vẫn **copy** file vào
`~/.claude/plugins/cache/`, không đọc thẳng thư mục nguồn. Sửa `SKILL.md` xong phải đẩy
sang cache thì mới có hiệu lực:

```
/plugin marketplace update thanhtungpfiev-skills
```
