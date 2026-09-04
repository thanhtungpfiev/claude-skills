---
name: diagram-rules
description: >
  Luật màu, font và kiểm chứng khi vẽ sơ đồ SVG bằng skill `diagram-design` —
  bảng màu Dracula một bản tối, mã màu gắn cứng theo vai trò, cấm Georgia vì
  thiếu dấu tiếng Việt, và cạm bẫy mask khi đổi font. Dùng khi vẽ hoặc sửa sơ đồ,
  khi chọn màu cho khối/chữ/mũi tên, khi đổi stack font trong SVG, hoặc khi người
  dùng nói "vẽ sơ đồ", "sửa màu sơ đồ", "sơ đồ nhìn đơn điệu".
---

# Luật vẽ sơ đồ

Phần bổ sung cho skill `diagram-design`. Skill đó lo bố cục và luật nối mũi tên;
file này lo **màu, chữ và cách kiểm chứng** — những thứ đã trả giá mới rút ra được.

Luật riêng của từng repo (đặt hình vào đâu, đặt tên ra sao) thì repo tự khai trong
`CLAUDE.md` của nó. Đừng chép luật repo vào đây.

## Một bản tối, không có bản sáng

Sơ đồ chỉ có **một bảng màu tối**. Không dùng `@media (prefers-color-scheme: dark)`.

Lý do: media query bắt theo theme **hệ điều hành**, không phải theme của app đang hiển thị
(Obsidian, VS Code, trình duyệt). Máy nào để OS ở light mode là sơ đồ ra bản sáng chói
trên nền tối của app — và không có gì báo, phải mở ra nhìn mới thấy.

Gỡ khối `@media` của một file cũ thì phải **merge** thuộc tính, đừng thay nguyên khai báo
class: khối tối chỉ ghi đè phần đổi màu, thay thẳng sẽ nuốt mất những thuộc tính nó không
nhắc tới. Hai ca đã gặp thật là `fill: none` của khung ngoài và `fill: transparent` của
tag chip — mất chúng thì nền đen phủ kín cả sơ đồ.

Kiểm bằng cách ép trình duyệt sang light mode rồi render lại: `--blink-settings=preferredColorScheme=1`.

## Bảng màu Dracula

Nền `#282a36` · panel `#44475a` · chữ `#f8f8f2` · viền nhạt `#6272a4`.

Chữ phụ 9px dùng `#bfc7e6`, chữ mờ hơn `#8f9ac4`, mũi tên `#7d88b8` — cố ý **sáng hơn**
`#6272a4` thuần Dracula, vì màu comment gốc quá tối để đọc ở cỡ đó.

Bản đầy đủ nằm ở `profile/dracula.md` cạnh file này. Máy mới thì chép nó vào
`~/.diagram-design/profiles/dracula.md`, rồi mỗi project cắm một file `.diagram-design`
ở gốc chứa đúng một dòng:

```
profile: dracula
```

Marker này là cách `diagram-design` chọn skin cho từng project mà không đụng bản cài
chung — xem `references/profiles.md` của skill đó.

## Màu là thông tin, không phải trang trí

Mỗi màu gắn cứng một vai trò, **giống nhau ở mọi sơ đồ**:

| Vai trò | Màu |
|---|---|
| Chỗ người dùng còn quyền | cyan `#8be9fd` |
| Tác nhân tự động hành động | hồng `#ff79c6` |
| Chạm ra ngoài hệ thống | cam `#ffb86c` |
| Hệ thống tự chạy | tím `#bd93f9` |
| Xong, thành công | lá `#50fa7b` |
| Chặn, cảnh báo | đỏ `#ff5555` |

**Áp cho:** viền khối · nền khối (10–12% opacity) · **tên node** · nhãn tag · mũi tên.

**Giữ trung tính:** chú thích dài trong node · callout in nghiêng · legend. Đó là câu chữ
để **đọc**; tô màu vào chỉ làm chậm mắt mà không thêm thông tin, vì vai trò đã nằm ở tên
node và viền rồi.

Ghi mã màu **một lần** ở đầu tài liệu; legend từng hình chỉ giải thích những màu hình đó
dùng — nhồi cả sáu vai trò vào mỗi legend là biến chú thích thành rác.

Hệ quả phải nói rõ với người dùng: **đổi màu một khối từ nay là đổi nghĩa của nó**, không
còn sửa cho đẹp được nữa. Bù lại, mọi vai trò đều có nhãn chữ đi kèm nên không có thông
tin nào chỉ nằm ở màu — người mù màu vẫn đọc đủ.

Đỏ `#ff5555` trên `#282a36` chỉ đạt **~4.6:1**, thấp nhất trong sáu màu (cam 8.4, hồng
5.9, tím 5.9). Vừa đủ ngưỡng AA — chỉ dùng cho chữ đậm từ 11px trở lên, cần đỏ ở cỡ nhỏ
hơn thì đổi màu chứ đừng thu cỡ chữ.

## Font: cái chạy thật là font dự phòng

SVG nhúng kiểu ảnh (`<img>`, hay `![[x.svg]]` trong Obsidian) **không tải được font
ngoài** — Google Fonts bị chặn. Nên font đầu stack luôn rụng, và **font dự phòng mới là
font thật sự hiển thị**. Thêm bất kỳ font nào vào stack cũng phải render thử mới biết.

- **Không bao giờ để Georgia trong stack.** Nó thiếu dải Latin Extended Additional nên
  `lấy` `quyết` `tầng` bị tách thành chữ cái cộng dấu rời, nhìn hệt lỗi encoding. Đã đo
  15 font bằng headless Chrome: Georgia là font **duy nhất** hỏng. Cambria · Times New
  Roman · Constantia · Palatino Linotype đều đủ dấu; mọi font mono thử qua (Cascadia
  Mono, Consolas, Courier New, Lucida Console) cũng đủ.
- Stack đang dùng: `'CaskaydiaCove NF', 'CaskaydiaCove Nerd Font', 'Cascadia Mono',
  ui-monospace, monospace` cho mọi chữ; callout in nghiêng thì `'Instrument Serif',
  Cambria, 'Times New Roman', serif`.
- Cách kiểm nhanh một font có đủ dấu không: render một SVG probe, mỗi dòng một font, đặt
  fallback là `serif`. Dòng nào hiện ra chữ **có chân** nghĩa là tên font đó không resolve
  được; dòng nào dấu rời ra là font thiếu glyph. Lỗi này không có cảnh báo nào cả.

### Cạm bẫy mask khi đổi font

Nhãn đặt trên viền khung được che bằng một `rect` mask khoét đúng bề rộng chữ. Vì font là
**monospace**, cho chữ đậm (`font-weight: 600`) **không đổi advance width**, nên làm nổi
nhãn mà không phải tính lại mask.

Đổi sang **font tỉ lệ** là chữ đậm rộng ra, tràn khỏi mask và làm hở viền khung — mà
không có gì báo. Ai đụng vào `font-family` của `<svg>` phải render lại soi mắt, đừng tin
diff.

## Chọn kiểu sơ đồ theo nội dung

Chọn theo thứ nội dung **thật sự là**, không theo kiểu nào nhìn đẹp. Ví dụ đã gặp: một
vòng lặp có cửa quyết định và ba đường thoát thì phải vẽ **flowchart**, không vẽ `loop` —
kiểu `loop` của `diagram-design` cấm nhánh rẽ, ép vào là bóp méo nội dung.

Tương tự, đừng xếp một sự kiện "nổ bất kỳ lúc nào" ngang hàng với các sự kiện có thứ tự cố
định trên cùng một timeline: vẽ nó nét đứt và nói rõ, chứ xếp ngang hàng là nói dối về
thời gian.

## Kiểm chứng trước khi báo xong

1. `python <thư-mục-skill-diagram-design>/scripts/self_check.py *.svg`
2. Render soi mắt bằng headless Chrome:
   `--headless --disable-gpu --screenshot=... --window-size=W,H`, thêm
   `--force-device-scale-factor=2` để soi chữ 7–9px. **Diff không cho thấy chữ tràn hộp
   hay hai nhãn đè lên nhau** — chỉ có mắt mới thấy.
3. Muốn chắc sơ đồ trơ với theme OS thì render thêm một lần với
   `--blink-settings=preferredColorScheme=1`.
4. Sơ đồ có mã màu thì kiểm luôn: mọi hình khối có class đều phải có `fill` xác định, và
   legend phải phủ đúng những màu hình đó dùng — không thiếu, không thừa.
