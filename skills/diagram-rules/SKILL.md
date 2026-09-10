---
name: diagram-rules
description: >
  Luật màu, font và kiểm chứng khi vẽ sơ đồ bằng skill `diagram-design` — mã màu
  gắn cứng theo vai trò, bảng màu Dracula, cấm Georgia vì thiếu dấu tiếng Việt,
  cạm bẫy mask khi đổi font, và những luật chỉ đúng khi SVG bị nhúng như ảnh.
  Dùng khi vẽ hoặc sửa sơ đồ, khi chọn màu cho khối/chữ/mũi tên, khi đổi stack
  font, hoặc khi người dùng nói "vẽ sơ đồ", "sửa màu sơ đồ", "sơ đồ nhìn đơn điệu".
---

# Luật vẽ sơ đồ

Phần bổ sung cho skill `diagram-design`. Skill đó lo bố cục và luật nối mũi tên;
file này lo **màu, chữ và cách kiểm chứng** — những thứ đã trả giá mới rút ra được.

Luật riêng của từng repo (đặt hình vào đâu, đặt tên ra sao) thì repo tự khai trong
`CLAUDE.md` của nó. Đừng chép luật repo vào đây.

## Phạm vi — đọc trước khi áp

`diagram-design` mặc định xuất **HTML** (bên trong là SVG inline); `.svg` rời là bước
xuất thêm. Ba ngữ cảnh đó chịu luật khác nhau, **áp nhầm là làm hỏng thứ đang chạy đúng**:

| Nhóm luật | HTML mở bằng trình duyệt | SVG inline trong HTML | `.svg` nhúng như ảnh |
|---|---|---|---|
| Mã màu theo vai trò · bảng màu · chọn kiểu sơ đồ | ✅ | ✅ | ✅ |
| Cạm bẫy mask khi đổi font | — | ✅ | ✅ |
| Font dự phòng mới là font thật chạy | ❌ | ❌ | ✅ |
| Chỉ một bản tối, bỏ `@media` | ❌ | ❌ | ✅ khi nhúng trong app có theme riêng |

"Nhúng như ảnh" nghĩa là `<img src="x.svg">` hoặc `![[x.svg]]` trong Obsidian — lúc đó
SVG là **document biệt lập**, không được phép tải tài nguyên ngoài và không biết gì về
trang chứa nó.

---

# Luật cho mọi output

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

Đỏ `#ff5555` trên nền `#282a36` chỉ đạt **~4.6:1**, thấp nhất trong sáu màu (cam 8.4,
hồng 5.9, tím 5.9). Vừa đủ ngưỡng AA — chỉ dùng cho chữ đậm từ 11px trở lên; cần đỏ ở cỡ
nhỏ hơn thì đổi màu chứ đừng thu cỡ chữ.

Mã màu này **không diễn đạt được bằng profile** của `diagram-design`: schema style-guide
chỉ có đúng một `accent`, còn bảng `series-*` thì chính skill đó dặn "don't backfill to
non-chart types". Nên nó phải sống ở đây, dạng luật chữ.

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
chung — xem `references/profiles.md` của skill đó. **Xoá marker là sơ đồ mới lặng lẽ quay
về skin mặc định**, không có gì báo.

## Chọn kiểu sơ đồ theo nội dung

Chọn theo thứ nội dung **thật sự là**, không theo kiểu nào nhìn đẹp. Ví dụ đã gặp: một
vòng lặp có cửa quyết định và ba đường thoát thì phải vẽ **flowchart**, không vẽ `loop` —
kiểu `loop` của `diagram-design` cấm nhánh rẽ, ép vào là bóp méo nội dung.

Tương tự, đừng xếp một sự kiện "nổ bất kỳ lúc nào" ngang hàng với các sự kiện có thứ tự cố
định trên cùng một timeline: vẽ nó nét đứt và nói rõ, chứ xếp ngang hàng là nói dối về
thời gian.

---

# Luật cho SVG inline (cả HTML lẫn `.svg` rời)

## Cạm bẫy mask khi đổi font

Nhãn đặt trên viền khung được che bằng một `rect` mask khoét đúng bề rộng chữ. Vì font là
**monospace**, cho chữ đậm (`font-weight: 600`) **không đổi advance width**, nên làm nổi
nhãn mà không phải tính lại mask.

Đổi sang **font tỉ lệ** là chữ đậm rộng ra, tràn khỏi mask và làm hở viền khung — mà
không có gì báo. Ai đụng vào `font-family` phải render lại soi mắt, đừng tin diff.

## Georgia: sự thật phổ quát, lý do thì tuỳ ngữ cảnh

**Georgia thiếu dải Latin Extended Additional**, nên `lấy` `quyết` `tầng` bị tách thành
chữ cái cộng dấu rời, nhìn hệt lỗi encoding. Đúng ở mọi ngữ cảnh — hễ Georgia thật sự
được dùng để render thì tiếng Việt vỡ ở đó.

Đã đo 15 font bằng headless Chrome: Georgia là font **duy nhất** hỏng. Cambria · Times New
Roman · Constantia · Palatino Linotype đều đủ dấu; mọi font mono thử qua (Cascadia Mono,
Consolas, Courier New, Lucida Console) cũng đủ.

Cách kiểm nhanh một font có đủ dấu không: render một SVG probe, mỗi dòng một font, đặt
fallback là `serif`. Dòng nào hiện chữ **có chân** nghĩa là tên font đó không resolve
được; dòng nào dấu rời ra là font thiếu glyph. Lỗi này không có cảnh báo nào cả.

---

# Luật chỉ đúng khi SVG bị nhúng như ảnh

Áp khi và chỉ khi file `.svg` được tải qua `<img>` hoặc `![[x.svg]]`. **Với HTML do skill
sinh ra thì bỏ qua cả mục này** — ở đó web font tải được và `prefers-color-scheme` chạy
đúng nghĩa.

## Font dự phòng mới là font thật sự chạy

SVG nhúng kiểu ảnh **không tải được font ngoài** — Google Fonts bị chặn. Nên font đầu
stack luôn rụng, và font hiển thị thật là font dự phòng đầu tiên có sẵn trên máy. Thêm bất
kỳ font nào vào stack cũng phải render thử mới biết chữ ra sao.

Stack đang dùng: `'CaskaydiaCove NF', 'CaskaydiaCove Nerd Font', 'Cascadia Mono',
ui-monospace, monospace` cho mọi chữ; callout in nghiêng thì `'Instrument Serif', Cambria,
'Times New Roman', serif` — **không có Georgia trong đó**.

*(HTML do skill sinh thì nạp font qua `<link href="fonts.googleapis.com/...">`, nên Geist
và Instrument Serif chạy đúng. Đừng bê luật này sang đó.)*

## Một bản tối, không `@media (prefers-color-scheme)`

Chỉ áp khi SVG nằm trong một app có **theme riêng độc lập với theme OS** — Obsidian là ca
điển hình.

Lý do: media query bắt theo theme **hệ điều hành**, còn app thì đang ở theme của nó. Máy
nào để OS sáng mà app để tối là sơ đồ ra bản sáng chói trên nền tối, và không có gì báo.
Với HTML mở thẳng bằng trình duyệt thì ngược lại — trang *chính là* ngữ cảnh của OS, nên
`prefers-color-scheme` là đúng, ép dark-only ở đó là làm hỏng thứ đang chạy đúng.

Gỡ khối `@media` của một file cũ thì phải **merge** thuộc tính, đừng thay nguyên khai báo
class: khối tối chỉ ghi đè phần đổi màu, thay thẳng sẽ nuốt mất những thuộc tính nó không
nhắc tới. Hai ca đã gặp thật là `fill: none` của khung ngoài và `fill: transparent` của
tag chip — mất chúng thì nền đen phủ kín cả sơ đồ.

---

# Kiểm chứng trước khi báo xong

0. **Validate XML trước đã — `self_check.py` KHÔNG bắt được file hỏng cấu trúc.** Đã gặp:
   một lệnh `sed` xoá dòng `<style>@import ...` cũng nuốt luôn thẻ `<defs>` mở nằm cùng
   dòng đó; 16 file mất thẻ mở mà `self_check.py` vẫn báo `OK` từng file một. Trình duyệt
   thì bỏ trắng cả hình, không báo lỗi gì. Rẻ nhất là parse thử:
   `python -c "import xml.etree.ElementTree as E,sys; [E.parse(f) for f in sys.argv[1:]]" *.svg`
   Dấu hiệu nhận ra qua ảnh render: **nhiều file ra đúng cùng một dung lượng byte** —
   đó là các trang trắng cùng kích thước, không phải trùng hợp.
1. `python <thư-mục-skill-diagram-design>/scripts/self_check.py <file>` — chạy được trên
   cả `.html` lẫn `.svg`.
2. Render soi mắt bằng headless Chrome:
   `--headless --disable-gpu --screenshot=... --window-size=W,H`, thêm
   `--force-device-scale-factor=2` để soi chữ 7–9px. **Diff không cho thấy chữ tràn hộp
   hay hai nhãn đè lên nhau** — chỉ có mắt mới thấy.
3. Sơ đồ có mã màu thì kiểm luôn: mọi hình khối có class đều phải có `fill` xác định, và
   legend phải phủ đúng những màu hình đó dùng — không thiếu, không thừa.
4. *Chỉ với `.svg` nhúng ảnh:* render thêm một lần ép light mode
   (`--blink-settings=preferredColorScheme=1`) để chắc sơ đồ trơ với theme OS. Hai lần
   render phải ra **file giống hệt nhau về dung lượng** — lệch byte là còn `@media` đâu đó.
5. **Đổi cỡ chữ hay đổi stack font thì phải quét tràn chữ bằng lệnh, không soi mắt.** Sang
   mono cỡ lớn hơn (12px sans → 14px mono) làm chữ rộng thêm khoảng 35%, đủ để tràn khỏi
   hộp và khỏi mask mà diff không hề lộ. Ước lượng đủ dùng: bề rộng ≈ `len(text) × cỡ chữ ×
   (0.60 + letter-spacing)`, so với hộp nhỏ nhất chứa điểm neo, chừa 4px mỗi bên; chuẩn hoá
   NFC trước khi đếm ký tự nếu không tiếng Việt bị đếm dôi. Chữ tràn **mask** còn tệ hơn
   tràn hộp: nét mũi tên xuyên qua giữa chữ.

## Khi buộc phải hạ cỡ chữ

Ngân sách chữ hết chỗ thì **rút gọn câu chữ trước, hạ cỡ sau**. Riêng chuỗi nội dung dài
(một scenario, một câu ví dụ) thì giữ 12px là chấp nhận được — nó là *nội dung*, không phải
*tên node*. Đừng bao giờ hạ cỡ chữ đỏ `#ff5555` xuống dưới 11px để nhét vừa: đổi màu, hoặc
để màu ở viền và nhãn tag còn chữ thì trung tính.
