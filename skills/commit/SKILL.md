---
name: commit
description: >
  Tách thay đổi thành từng commit một ý và viết message ghi lại VÌ SAO repo tiến hoá
  như vậy, theo khung Problem → Solution → Implications. Dùng mỗi khi tạo git commit,
  stage hoặc tách thay đổi, viết hoặc sửa commit message, hoặc khi người dùng nói
  "commit", "tạo commit", "tách commit", "sửa commit message", "write a commit message".
  Áp dụng cả khi commit chỉ là hệ quả của một việc khác.
---

# Commit message

Commit message là bản ghi lịch sử **vì sao codebase tiến hoá như vậy** — đoạn văn mà người
đọc sau này rơi vào từ `git blame`. Diff đã nói *cái gì* đổi rồi; message phải cung cấp
đúng phần diff không phục hồi được.

## Quy ước riêng của repo

File này là phần dùng chung cho mọi repo. Phần riêng — **ngôn ngữ message, dạng subject,
đặc thù nội dung, tình trạng lịch sử** — nằm ở mục **"Quy ước commit"** trong `CLAUDE.md`
của repo. Đọc mục đó trước khi viết; khi nó lệch với file này thì **nó thắng**.

Repo không có mục đó thì suy ra từ hiện trạng: `git log -5 --format='%s%n%n%b'` cho biết
dạng subject và ngôn ngữ đang dùng.

*(File này viết bằng tiếng Việt vì nó nói với bạn. Ngôn ngữ của chính commit message thì
theo repo — đừng lẫn hai thứ.)*

## Khung: Problem → Solution → Implications

Trả lời ba câu này, theo đúng thứ tự, viết thành văn xuôi:

1. **Problem** — giới hạn, lỗi, hay vướng víu nào buộc phải thay đổi? Trước đó cái gì
   hỏng, chậm, khó hiểu, hoặc không làm được?
2. **Solution** — đã chọn cách nào, và **đã cân nhắc rồi loại bỏ phương án nào, vì sao?**
   Một phương án bị loại thường là dòng giá trị nhất trong cả message: nó ngăn người sau
   mở lại cuộc tranh luận đã khép. Nhưng chỉ ghi phương án **thật sự đã cân nhắc** — bịa
   ra một lựa chọn nghe hợp lý cho đủ khung còn tệ hơn là bỏ trống, vì người đọc sau không
   có cách nào biết nó chưa từng được đặt lên bàn.
3. **Implications** — đánh đổi và hệ quả, **cả tốt lẫn xấu**. Trên hết: điều gì sẽ khiến
   người đọc sau này **bất ngờ**? Ràng buộc mới, giả định đang gánh cả hệ thống, thứ gỡ ra
   là hỏng, migration chỉ chạy một lần, cái giá về hiệu năng đã chấp nhận.

## Bố cục thân bài

Mỗi phần là một đoạn mở đầu bằng dấu gạch ngang và **nhãn tiếng Anh viết rõ**, kể cả khi
thân bài viết bằng tiếng Việt — nhãn là thứ làm `git log` quét được bằng mắt và giữ cho
khung không tan trở lại thành một khối chữ:

```
- Problem: …

- Solution: …

- Implications: …
```

Bỏ hẳn một phần khi nó không có gì để nói (sửa lỗi chính tả thì làm gì có Implications);
đừng bao giờ để nhãn rỗng. Ngắt dòng ở khoảng 76 ký tự, dòng nối thụt vào cho thẳng với
phần chữ chứ không thẳng với dấu gạch.

## Cân theo độ phức tạp

| Thay đổi | Message |
|---|---|
| Sửa chính tả, đổi tên, format | Chỉ một dòng subject |
| Sửa nhỏ tự nó đã rõ | Subject + 1–2 câu (thường chỉ cần Problem) |
| Tính năng hoặc refactor bình thường | Subject + mỗi phần một đoạn, bỏ phần nào rỗng |
| Lỗi tinh vi (thứ tự thực thi, cache, đồng bộ), đổi kiến trúc | Vài đoạn — chính phần lập luận mới là thứ cần giao |

Đừng bao giờ độn thêm cho đủ khung khi thay đổi nhỏ. Cũng đừng nén một thay đổi tinh vi
xuống còn một dòng.

## Những kiểu nên tránh

- **Kể lại diff.** "Thêm `foo.md`, sửa `bar.md`, bỏ mục cũ" — người đọc tự thấy được.
  Xoá đi và nói vì sao phải làm những việc đó.
- **Liệt kê mọi thứ đã đụng thành changelog.** Một danh sách gạch đầu dòng điểm danh từng
  file đọc ra chỉ thấy nhiễu; người đọc cần mạch lập luận, không cần bảng kê.
- **Lấy tên file làm bố cục.** Tổ chức theo *ý*, không theo file.
- **Giấu đánh đổi.** Nếu có thứ gì chậm đi, kém tổng quát đi, hoặc từ nay phụ thuộc vào
  thứ tự, thì phải nói. Chính câu đó là lý do message tồn tại.

## Tổ chức commit: một commit một ý

Trước khi nghĩ tới câu chữ, phải quyết **commit này gồm những gì**. Commit là đơn vị
review và đơn vị revert, nên nó phải là **một thay đổi mạch lạc, tự nó review độc lập
được**. Đừng trộn refactor với tính năng mà nó dọn đường, đừng gộp nhiều chỗ sửa không
liên quan, đừng để một lượt format đi ké theo thay đổi logic.

Đây không phải sạch sẽ cho vui — đây là điều kiện để công cụ còn dùng được:

- **`git blame`** thả người đọc vào đúng một message, và message đó phải giải thích được
  dòng đang nằm dưới con trỏ. Message ôm ba ý thì không giải thích nổi ý nào.
- **`git bisect`** thu hẹp một hồi quy về một commit. Commit đó ôm ba thay đổi thì bisect
  gần như chưa nói được gì, và bạn dò lại bằng tay từ đầu.
- **`git revert`** một commit hỗn hợp sẽ lôi cả phần không liên quan ra theo.

**Đừng quét việc đang sửa dở của người dùng vào commit của mình.** Cấu hình editor, plugin
mới cài, cache tự sinh đang nằm chung trong `git status` thì để **nguyên chưa stage** —
không bao giờ `git add -A`. Báo lại đã để lại những gì khi tường thuật commit.

Mỗi commit cũng nên để cây thư mục ở trạng thái chạy được (test qua, app chạy). Commit chỉ
build được khi có commit kế tiếp thì phá bisect y hệt commit hỗn hợp.

Dấu hiệu nhận ra commit đang ôm quá nhiều: viết subject mà phải nối hai vế bằng "và" cho
hai việc chẳng liên quan, hoặc đoạn Problem phải tả hai vấn đề rời nhau. Đó là lúc tách,
không phải lúc viết dài thêm.

### Tách khi một file chứa hai ý

Thông thường là `git add -p`. **Nhưng harness này không chạy được cờ tương tác** (`add -i`,
`add -p`, `rebase -i` đều fail), nên phải tách không tương tác:

- **File thuộc trọn về một ý** → `git add <file>`.
- **File chứa hunk của hai ý** → lọc hunk rồi stage bằng patch:
  ```bash
  git diff -- <file> > all.patch        # giữ phần header, rồi chọn các hunk @@
  # dựng patch = header gốc + đúng những hunk @@ thuộc về commit này
  git apply --cached --recount kept.patch
  ```
  Chọn hunk bằng **một chuỗi đặc trưng nằm trong nó**, đừng chọn theo số thứ tự — chỉ số
  xê dịch ngay khi một patch được áp.

Rồi kiểm chứng trước khi commit: `git diff --cached` chỉ được chứa đúng ý này, còn
`git diff` trần vẫn phải giữ phần còn lại. Kiểm cả việc một dòng đặc trưng của ý *kia*
**không** có mặt trong diff đã stage — hunk lạc sang nhầm commit thì ngoài cách đó không
có gì báo.

## Các bước

0. **Dựng commit trước** — gom cây thư mục thành từng ý mạch lạc theo mục trên, và chỉ
   stage ý đầu tiên. Một ý có thể là một commit; nhiều ý rời nhau thì không bao giờ là một.
1. **Đọc thay đổi thật** — `git diff --staged` (hoặc `git diff`, `git status`). Đừng bao
   giờ viết message theo trí nhớ về cuộc hội thoại; diff đã stage mới là nguồn sự thật.
2. **Xem subject gần đây** — `git log -5 --format='%s%n%n%b'` — và giữ cho nhất quán. Chỉ
   *dòng subject* được kế thừa theo cách này; thân bài luôn dùng bố cục có nhãn ở trên,
   bất kể commit cũ viết thế nào.
3. **Viết subject**: một dòng, ≤ ~72 ký tự, theo dạng mà `CLAUDE.md` của repo quy định.
4. **Viết thân bài** theo khung, cân theo bảng trên. Ngắt dòng ở ~76 ký tự.
5. **Commit bằng file, không dùng chuỗi inline:**
   ```bash
   git commit -F <đường-dẫn>/msg.txt      # hoặc: git commit --amend -F <đường-dẫn>/msg.txt
   ```
   Chuỗi `-m` nhiều dòng bị shell quoting làm hỏng — cụ thể, here-string của PowerShell
   (`@'…'@`) lọt một ký tự `@` vào message khi chạy qua Bash. Ghi message ra file tạm rồi
   truyền `-F`. Message có tiếng Việt có dấu thì file phải là UTF-8.
6. **Kiểm lại**: `git log -1 --format='%s%n%n%b'`.

## Sửa lại message đã có

Chỉ amend commit **chưa push** — kiểm tra bằng `git status -sb` (`ahead N`) hoặc
`git log @{u}..`. Mặc định là **không amend**: cứ để commit đã publish nguyên đó và áp quy
ước cho commit kế tiếp.

Viết lại message đã push thì phải force-push, nên **chỉ làm khi người dùng yêu cầu rõ**.
Khi đó đừng amend thủ công từng cái:

1. `git branch backup-<lý-do>` làm phao, và `git stash push` phần đang sửa dở —
   `filter-branch` từ chối chạy khi working tree còn thay đổi chưa commit.
2. Ghi mỗi message mới ra một file tên theo sha của commit gốc, rồi:
   ```bash
   git filter-branch -f --msg-filter '
     short=$(echo "$GIT_COMMIT" | cut -c1-7)
     if [ -f "$M/$short.txt" ]; then cat "$M/$short.txt"; else cat; fi
   ' -- main <các-nhánh-khác>
   ```
   `$GIT_COMMIT` là sha **gốc**, nên bảng tra không bị lệch khi sha đổi dần. Nhớ liệt kê
   cả nhánh cũ nằm trong `main`, không thì chúng giữ message cũ sống mãi. Không bao giờ
   dùng `-- --all` — nhánh backup sẽ bị viết lại theo.
3. Repo có **annotated tag** trỏ vào phần lịch sử bị viết lại thì thêm `--tag-name-filter cat`,
   không thì tag ở lại trên đám commit cũ không ai với tới được.
4. **Kiểm chứng bắt buộc**: `git diff <backup> main` phải rỗng — chứng minh chỉ message
   đổi, không byte nội dung nào đụng vào. Diff hai đầu nhánh chỉ so hai đầu, nên soi thêm
   tree sha từng cặp commit. Kiểm luôn `%an %ae %ad` còn nguyên.
5. `git push --force-with-lease` (không dùng `--force` trần), rồi push riêng từng tag đã
   dời với `--force` — tag không đi theo lệnh push nhánh.
6. `git stash pop`, rồi **dọn phao**: xoá nhánh backup (cả bản trên remote nếu đã push) và
   ref `refs/original/` mà `filter-branch` để lại. Giữ chúng lại là cả hai phiên bản của
   mọi message quay về `git log --all` — đúng cái phân mảnh mà lần rewrite này sinh ra để
   dẹp.

Đừng tham chiếu commit khác bằng sha trong message, vì viết lại là sha đổi hết và tham
chiếu thành trỏ vào hư không — gọi bằng dòng subject của nó thì bền qua mọi lần rewrite.

## Ví dụ

Bố cục minh hoạ ở đây bằng tiếng Anh; ngôn ngữ thật thì theo repo.

Chỉ subject, vì thay đổi tự nó đã rõ:

```
Fix broken link to the deployment runbook
```

Một refactor mà phần lập luận mới là thứ đáng giá:

```
Move token refresh out of the request interceptor

- Problem: refreshing inside the interceptor meant every concurrent 401 kicked
  off its own refresh call. With three parallel dashboard requests we regularly
  sent three refreshes, and the last one to land silently invalidated the tokens
  the other two had just stored — users saw a random logout once a session.

- Solution: refresh now lives in a single-flight helper that concurrent callers
  await. Considered a mutex around the interceptor, but that serialises every
  request even when no refresh is needed; considered refreshing on a timer ahead
  of expiry, but clock skew between our servers and the IdP made the safe margin
  large enough to defeat the point.

- Implications: the helper caches the in-flight promise, so a failed refresh now
  rejects every waiting request at once instead of each retrying independently —
  louder, but it surfaces a dead session immediately rather than after three
  timeouts. Callers outside the interceptor must go through the helper too;
  hitting the refresh endpoint directly reintroduces the race.
```
