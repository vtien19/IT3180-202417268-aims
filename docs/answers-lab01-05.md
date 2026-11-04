# Trả lời câu hỏi thảo luận – Lab 01 đến Lab 05

- Học phần: IT3180 – Nhập môn Công nghệ phần mềm · Thực hành Git & GitHub (Release Flow)
- Sinh viên: Đỗ Việt Tiến – MSSV 202417268
- Repo: `it3180-202417268-aims`

---

## Lab 01 – Thiết lập môi trường & Refactor flow

### Câu hỏi nhanh: Cấu hình `--global` được lưu ở đâu? Khác gì so với `--local`?

Git có ba mức cấu hình. Mức hẹp hơn ghi đè mức rộng hơn:

| Mức | Tệp lưu | Phạm vi áp dụng |
|---|---|---|
| `--system` | `/etc/gitconfig` (macOS dùng Command Line Tools: `/Library/Developer/CommandLineTools/usr/share/git-core/gitconfig`) | Mọi người dùng trên máy |
| `--global` | `~/.gitconfig` (máy em: `/Users/name/.gitconfig`) | Mọi repo của người dùng hiện tại |
| `--local` | `.git/config` bên trong từng repo | Chỉ repo đó |

Thứ tự ưu tiên: `--local` > `--global` > `--system`. Khi ghi bằng `git config <khóa> <giá trị>` trong một repo mà không chỉ định mức, Git ghi vào mức `--local`.

Ví dụ trên máy em (`git config --list --show-origin`):

```
file:/Library/Developer/CommandLineTools/usr/share/git-core/gitconfig   init.defaultbranch=main
file:/Users/name/.gitconfig                                             init.defaultbranch=master
```

Mức system đặt nhánh mặc định là `main`, nhưng mức global đặt `master` và ghi đè lên, nên `git init` tạo ra nhánh `master`.

`--global` dùng cho thông tin chung của người dùng như `user.name`, `user.email`, `core.editor`. `--local` dùng khi riêng một repo cần khác đi, ví dụ một repo cần email khác: `git config --local user.email ...`. Vì `.git/config` nằm trong thư mục `.git/`, cấu hình local không được commit và không đi theo khi người khác clone repo.

### Câu 1: Vì sao dùng `git mv`?

`git mv dvd.py aims/dvd.py` tương đương ba lệnh `mv dvd.py aims/dvd.py`, `git rm dvd.py` và `git add aims/dvd.py`, nhưng gộp lại trong một bước và đưa cả việc xóa tên cũ lẫn thêm tên mới vào staging. Nếu chỉ dùng `mv` thường, `git status` sẽ thấy một tệp bị xóa và một tệp chưa được theo dõi, rất dễ quên add một trong hai.

Git không lưu thao tác đổi tên. Nó nhận ra đổi tên khi so sánh hai commit: nếu tệp mới đủ giống tệp cũ (mặc định từ 50%) thì được coi là đổi tên. Vì vậy em tách thành hai commit:

1. `refactor: move sources into aims package`: chỉ di chuyển tệp. Nội dung `dvd.py` và `cart.py` giữ nguyên nên giống 100%.
2. `refactor: update imports in main.py`: sửa import ở một commit riêng.

Nhờ vậy:

- `git log --oneline --follow -- aims/cart.py` vẫn hiện commit `a45567d feat: add initial DVD, Cart and demo program`, được tạo khi tệp còn ở thư mục gốc. Lịch sử của tệp không bị đứt.
- Tab *Files changed* của Pull Request hiện `cart.py → aims/cart.py` là *renamed*, nên reviewer không phải đọc lại toàn bộ tệp như một tệp mới.
- `git blame` vẫn chỉ ra đúng commit đã viết từng dòng.

Về mặt SCM, đây là phần định danh cấu hình (Configuration Identification): tệp vẫn là cùng một configuration item, chỉ đổi đường dẫn.

### Câu 2: `release/lab01` có phải baseline không?

Baseline là một phiên bản của các configuration item đã được thống nhất, dùng làm cơ sở cho bước tiếp theo, và chỉ được thay đổi qua quy trình kiểm soát thay đổi.

Theo nghĩa đó, `release/lab01` đóng vai trò baseline của Lab 01: nó được tạo từ `master` sau khi PR refactor đã merge, là đúng phiên bản em nộp, và theo Release Flow thì không commit thẳng lên nó, chỉ được sửa qua nhánh `hotfix/*` và Pull Request.

Tuy nhiên nhánh chưa phải cách định danh baseline chặt chẽ nhất:

- **Nhánh là con trỏ có thể di chuyển.** Khi có hotfix, đầu nhánh `release/lab01` sẽ trỏ sang commit mới. Thứ cố định thật sự là commit SHA ở đầu nhánh lúc nộp (kiểm tra bằng `git rev-parse origin/release/lab01`, trùng với `origin/master` tại thời điểm tạo).
- **Ở Lab 01 nhánh chưa được bảo vệ.** Về mặt kỹ thuật vẫn push thẳng lên được, nên "chỉ đổi qua quy trình" lúc này mới là quy ước. Đến Lab 04, rule cho `release/*` mới chặn push trực tiếp, force push và xóa nhánh.
- **Lab 04 sẽ gắn annotated tag `v0.1.0` vào commit này.** Tag không bao giờ di chuyển nên là định danh chính xác của baseline; còn `release/lab01` là dòng bảo trì của baseline đó.

Kết luận: `release/lab01` là baseline theo nghĩa phiên bản đã thống nhất để nộp. Để chỉ đích danh baseline một cách bất biến thì dùng commit SHA hoặc tag.

### Câu 3: Vì sao không commit thẳng `master` dù làm một mình?

1. **`master` phải luôn chạy được.** Đây là nhánh tích hợp và là nguồn để tạo các nhánh `release/*`. Làm trên nhánh riêng thì trạng thái dở dang (ví dụ đã `git mv` nhưng chưa sửa import, `main.py` báo `ModuleNotFoundError: No module named 'dvd'`) không bao giờ xuất hiện trên `master`. Nếu làm hỏng thì chỉ cần bỏ nhánh.
2. **Pull Request là bản ghi yêu cầu thay đổi.** Tên nhánh nói lên mục đích; mô tả PR ghi lại mục đích, thay đổi và cách kiểm thử. Sau này nhìn lịch sử là biết vì sao có thay đổi, và từ Lab 03 có thể liên kết PR với Issue (`Fixes #N`).
3. **Có một bước kiểm tra trước khi tích hợp.** Tab *Files changed* giúp tự review lần cuối, ví dụ xác nhận tệp hiện *renamed* chứ không phải xóa + thêm, hay không có `__pycache__/` lọt vào.
4. **Dễ hoàn tác.** Một thay đổi vào `master` qua merge commit có thể được revert cả cụm bằng một lệnh (`git revert -m 1 <sha>`), không phải tìm từng commit lẻ.
5. **Quy trình phải nhất quán từ đầu.** Từ Lab 02, branch protection chặn push thẳng vào `master`; ở Lab 05, CI chạy test trên mỗi PR. Các cơ chế này chỉ có tác dụng khi mọi thay đổi đều đi qua PR.

Kinh nghiệm thực tế trong lab: ở Phần C, em lỡ `git commit --amend` một commit đã push, khiến `master` trên máy và `origin/master` bị lệch (diverged) và push bị từ chối. Sai sót xảy ra ngay trên nhánh chính, nơi các bản phát hành được tạo ra. Nếu làm trên nhánh riêng, việc viết lại lịch sử chỉ ảnh hưởng một nhánh ngắn hạn, còn `master` không bị đụng đến.

---

## Lab 02 – Feature/Topic flow & Pull Request

### Câu 1: Vì sao phải đồng bộ `master` trước khi gửi PR?

Nhánh `feature/search-by-title` được tạo từ `master` cũ, khi `master` chưa có `print_cart`. Trong lúc làm, PR `feature/cart-print` đã được merge nên `master` đi trước. Chạy `git merge origin/master` vào nhánh trước khi gửi PR có các lợi ích:

1. **Kiểm thử đúng phiên bản sẽ được tích hợp.** Code mới có thể chạy đúng khi đứng một mình nhưng hỏng khi ghép với `master` mới (ví dụ cả hai nhánh cùng sửa `main.py`). Đồng bộ xong chạy lại `python main.py` và test là kiểm tra được kết quả tích hợp thật. Đúng nguyên tắc "thứ được duyệt = thứ được tích hợp".
2. **Xung đột được giải quyết bởi chính tác giả, trên nhánh của mình.** Người hiểu thay đổi nhất xử lý xung đột, trước khi reviewer đọc. Nếu không, PR báo *This branch has conflicts* và không merge được.
3. **Reviewer duyệt đúng code cuối cùng.** Approval được cấp cho code đã chứa `master` mới nhất. Với tùy chọn *Dismiss stale approvals*, nếu đồng bộ sau khi được duyệt thì phải duyệt lại.
4. **Giữ nhánh sống ngắn, gần `master`.** Đồng bộ thường xuyên thì mỗi lần chỉ có ít thay đổi phải ghép, tránh "merge hell" (quy tắc 1 của Release Flow).

GitHub cũng có tùy chọn *Require branches to be up to date before merging* (đi kèm *Require status checks to pass*) để bắt buộc việc này.

### Câu 2: Khi nào không được rebase?

Rebase viết lại lịch sử: các commit được tạo lại với SHA mới. Vì vậy **không rebase những commit đã chia sẻ mà người khác có thể đang dựa vào** (quy tắc 5 của Release Flow: viết lại lịch sử chỉ trên commit chưa chia sẻ). Cụ thể:

- **Không bao giờ rebase `master` và `release/*`.** Mọi người đều đã pull các nhánh này; các nhánh khác được tạo từ chúng; tag và PR trỏ tới commit trên đó. Rebase rồi force push sẽ làm bản clone của người khác bị lệch, commit bị nhân đôi, và có thể đè mất công việc. Branch protection cũng chặn force push.
- **Không rebase nhánh mà người khác đang làm tiếp trên đó.** Ví dụ Lab 03 Phần B: `bugfix/discount-calculation` được tạo từ `feature/discount`. Nếu rebase `feature/discount`, nhánh bugfix vẫn dựa trên các commit cũ, khi merge sẽ ra commit trùng lặp và xung đột.
- **Hạn chế rebase khi PR đang được review.** Force push làm comment review trỏ vào commit không còn tồn tại, và approval bị gỡ (*Dismiss stale approvals*).

Được phép rebase: commit chỉ có trên máy mình, hoặc nhánh riêng đã push nhưng chỉ mình dùng. Khi đó push lại bằng `git push --force-with-lease`, lệnh này từ chối ghi đè nếu trên remote có commit mình chưa thấy.

### Câu 3: `feature/*` khác `topic/*` ra sao?

Hai loại nhánh đi theo cùng một quy trình: tạo từ `master`, merge vào `master` qua PR, cùng chịu branch protection. Khác nhau ở **mục đích thay đổi**:

| | `feature/*` | `topic/*` |
|---|---|---|
| Nội dung | Tính năng mới của sản phẩm, thay đổi hành vi chương trình | Chủ đề không phải tính năng: tài liệu, cấu hình repo, quy trình, CI, chuẩn bị phát hành |
| Ví dụ trong lab | `feature/cart-print`, `feature/search-by-title`, `feature/sort-cart` | `topic/pr-template`, `topic/use-case-diagram`, `topic/prepare-release-1.0.0`, `topic/ci-unit-tests` |
| Kiểu commit | `feat:` | `docs:`, `chore:`, `ci:` |
| Ảnh hưởng phát hành | Ghi vào mục *Added* của CHANGELOG, thường kéo theo tăng MINOR | Thường không làm thay đổi phiên bản phần mềm |

Đặt tên đúng loại giúp đọc lịch sử, lọc nhánh và quyết định nhanh thay đổi nào cần ghi CHANGELOG. Trong Release Flow gốc của Microsoft, "topic branch" là tên gọi chung cho mọi nhánh ngắn hạn; học phần tách riêng `feature/*` để phân biệt tính năng sản phẩm với các thay đổi còn lại.

---

## Lab 03 – Bugfix flow, xung đột & hoàn tác

### Câu 1: Merge base là gì?

Merge base là **commit tổ tiên chung gần nhất** của hai nhánh, xem bằng `git merge-base A B`. Đó là điểm hai nhánh bắt đầu tách ra.

Git dùng merge base để **merge ba chiều** (base – nhánh của mình – nhánh kia). Với mỗi đoạn mã:

- chỉ một bên thay đổi so với base → Git tự lấy thay đổi đó;
- cả hai bên cùng thay đổi một đoạn theo cách khác nhau → **xung đột**.

Ví dụ Phần C: tại merge base, `cart.py` có `print("The disc has been added")`. Dev 1 sửa dòng này thành tiếng Việt, Dev 2 sửa thành f-string có tên đĩa. Cả hai cùng đổi một dòng so với base nên Git không tự quyết được, phải giải quyết tay.

Merge base còn quyết định nhiều thứ khác:

- Tab *Files changed* của PR hiển thị thay đổi từ merge base đến đầu nhánh (so sánh ba chấm `master...feature`).
- `git rebase` lấy các commit sau merge base đặt lại lên đầu nhánh đích.
- Chọn sai base cho PR thì merge base thay đổi. Ở Phần B, nếu PR của `bugfix/discount-calculation` để base là `master` thay vì `feature/discount`, merge base lùi về điểm cũ hơn nên PR hiện cả các commit của `feature/discount` ("PR bugfix hiện nhiều commit lạ").
- Mỗi lần đồng bộ `master` vào nhánh, merge base được dời lên mới hơn, nên lần merge sau có ít thay đổi phải so hơn.

### Câu 2: Vì sao `master` và `release/*` phải dùng `revert`?

`master` và `release/*` là **lịch sử đã chia sẻ**: đã có trên GitHub, người khác đã pull, các nhánh khác được tạo từ đó, `release/*` là bản đã nộp và được gắn tag.

| | `reset` | `revert` |
|---|---|---|
| Cơ chế | Dời con trỏ nhánh về trước, commit bị loại khỏi nhánh | Tạo commit mới đảo ngược thay đổi |
| Lịch sử | Bị viết lại | Chỉ được nối thêm |
| Đưa lên GitHub | Cần force push (bị branch protection chặn) | Push và PR bình thường |

Dùng `reset` trên nhánh chung sẽ:

- làm bản clone của mọi người bị lệch với remote;
- làm mất dấu vết: commit mà PR, Issue hay tag tham chiếu không còn nằm trên nhánh;
- vi phạm kiểm soát thay đổi vì thay đổi không đi qua PR.

`revert` thì giữ đủ dấu vết: lịch sử ghi rõ thay đổi nào được đưa vào, khi nào bị hủy và vì sao (commit có dòng `This reverts commit ...`). Bản thân việc revert cũng đi qua nhánh `bugfix/revert-...` và PR như mọi thay đổi khác.

Lưu ý khi revert merge commit: phải dùng `-m 1` để chọn nhánh chính làm gốc. Sau khi revert một merge, nếu merge lại đúng nhánh đó thì Git coi các commit cũ là đã merge rồi và không áp dụng lại; muốn đưa vào lại phải revert chính commit revert.

---

## Lab 04 – Release flow & phiên bản phát hành

### Câu hỏi thêm: Vì sao chuẩn bị phát hành trên `master` trước, không sửa trên nhánh release?

Trong Release Flow, `release/*` **không bao giờ merge ngược vào `master`**. Nếu nâng `__version__` và viết CHANGELOG trên `release/lab04`, các thay đổi đó sẽ mãi chỉ nằm trên nhánh release: `master` không có mục `[1.0.0]` trong CHANGELOG và lần phát hành sau (tạo từ `master`) sẽ thiếu lịch sử này.

Chuẩn bị trên `master` qua `topic/prepare-release-1.0.0` và PR thì:

- thay đổi được review như mọi thay đổi khác;
- `release/lab04` được tạo từ một commit đã hoàn chỉnh, nhánh release chỉ là bản đóng băng, không có commit riêng nào;
- kiểm tra được bằng `git log --oneline master..release/lab04`: kết quả rỗng, tức release không có gì mà `master` thiếu.

### Câu 1: Vì sao `release/*` không merge vào `master`? So sánh với GitFlow.

Dòng chảy của Release Flow chỉ có một chiều: `master` → `release/*`. Không merge ngược vì:

- **Nhánh release chứa những thứ chỉ dành cho dòng phiên bản cũ**, như commit nâng phiên bản `1.0.1` hay mục CHANGELOG riêng. Merge vào `master` (đang ở `1.1.0`) sẽ xung đột, thậm chí hạ phiên bản xuống.
- **Có nhiều dòng phát hành song song** (`release/lab04`, `release/lab05`, ...). Merge tất cả ngược về sẽ thành một mạng merge chồng chéo, đúng kiểu "merge hell".
- **Bản sửa lỗi đã có cách lan truyền có chọn lọc**: `git cherry-pick -x` chỉ commit sửa lỗi sang `master` (Lab 05), không kéo theo commit nâng phiên bản.
- **`master` luôn là nguồn duy nhất của mọi phiên bản tương lai**; nhánh release chỉ là ảnh chụp cộng với vài bản vá tối thiểu.

So sánh với GitFlow:

| | Release Flow (học phần) | GitFlow |
|---|---|---|
| Nhánh lâu dài | Chỉ `master` | `main` (bản phát hành) + `develop` (tích hợp) |
| Nhánh tính năng | Tạo từ `master`, merge về `master` | Tạo từ `develop`, merge về `develop` |
| Nhánh release | Tạo từ `master`, **giữ lại** làm dòng bảo trì, không merge ngược | Tạo từ `develop`, khi xong **merge vào cả `main` và `develop`**, rồi xóa |
| Hotfix | Từ `release/*`, merge vào release, cherry-pick sang `master` | Từ `main`, merge vào `main` và `develop` |
| Tag | Trên nhánh `release/*` | Trên `main` |
| Phù hợp | Phát hành thường xuyên, bảo trì nhiều phiên bản song song | Phát hành định kỳ, có giai đoạn ổn định hóa, `main` luôn là bản production |

Release Flow đơn giản hơn (một nhánh tích hợp, không merge ngược) và hợp với CI/CD, nhưng đòi hỏi kỷ luật lan truyền bản sửa bằng cherry-pick; quên là lỗi quay lại (Lab 05 dùng `git cherry` để kiểm toán). GitFlow tự động đưa bản sửa về `develop` nhờ merge ngược, nhưng nhiều nhánh và nhiều lần merge hơn, dễ xung đột giữa `develop` và `main`.

### Câu 2: Vì sao lên `1.0.0` mà không phải `0.4.0`?

Theo Semantic Versioning, `0.y.z` dành cho giai đoạn phát triển ban đầu: API chưa ổn định, mọi thứ có thể thay đổi bất cứ lúc nào. Phiên bản `1.0.0` là lúc **công bố API công khai ổn định**; từ đó, thay đổi phá vỡ tương thích bắt buộc phải tăng MAJOR.

Lab 04 là bản phát hành chính thức đầu tiên: tính năng chính đã đủ (giỏ hàng, `print_cart`, `search_by_title`, giảm giá), lỗi đã biết đã sửa, test đều pass, và lần đầu có đủ quy trình phát hành (CHANGELOG, nhánh release được bảo vệ, annotated tag, GitHub Release). Đó là lúc sản phẩm sẵn sàng cam kết tương thích, nên là `1.0.0`. Các bản nộp Lab 01–03 vẫn là giai đoạn phát triển nên được gắn tag bù `v0.1.0`–`v0.3.0`.

Số phiên bản là một cam kết, không phải bộ đếm số lần nộp. Từ `1.0.0` trở đi, quy tắc SemVer mới có ý nghĩa: sửa lỗi thì lên `1.0.1` (PATCH), thêm tính năng tương thích thì lên `1.1.0` (MINOR), như Lab 05.

---

## Lab 05 – Hotfix flow & bảo trì nhiều phiên bản

### Câu hỏi thêm: Vì sao không merge cả nhánh hotfix vào `master`?

Nhánh `hotfix/search-case-insensitive` có hai commit: commit sửa lỗi và commit nâng phiên bản lên `1.0.1`. `master` đã ở `1.1.0`, nên merge cả nhánh sẽ xung đột ở `__version__` và CHANGELOG (GitHub báo *Can't automatically merge*), và nếu ép merge có thể hạ phiên bản của `master`. Vì vậy commit sửa lỗi được tách riêng ngay từ đầu, và chỉ commit đó (`<FIX_SHA>`) được `cherry-pick -x` sang `master`.

### Câu hỏi thêm: Vì sao ở Phần A chưa gắn tag `v1.1.0`?

Tag đã chia sẻ thì không bao giờ được xóa hay di chuyển, vì nó là định danh bất biến của một baseline. Ở Phần A, `release/lab05` vừa được tạo nhưng chưa được kiểm tra xong, và sau đó phát hiện lỗi `search_by_title` phân biệt hoa thường cũng ảnh hưởng tới dòng này.

Nếu đã gắn `v1.1.0` vào commit chưa có bản sửa, `v1.1.0` sẽ mãi là phiên bản lỗi, và bản sửa phải phát hành thành `v1.1.1`. Chờ tới khi đã cherry-pick bản sửa và test pass mới gắn tag thì `v1.1.0` đúng là phiên bản đã được kiểm chứng. Nhánh release vẫn nhận sửa đổi qua PR được, còn tag thì đóng băng; vì vậy chỉ gắn tag sau khi đã kiểm toán (tag + test).

### Câu 1: Ưu, nhược điểm của *upstream first* so với *release first*?

- **Release first** (cách làm trong Lab 05): tạo hotfix từ nhánh release bị lỗi, sửa và test trên đúng phiên bản người dùng đang chạy, phát hành `v1.0.1`, rồi cherry-pick sang `master` và các dòng release khác.
- **Upstream first** (Release Flow của Microsoft): sửa trên `master` trước qua nhánh và PR, rồi cherry-pick xuống các nhánh `release/*` cần bản sửa.

| | Upstream first | Release first |
|---|---|---|
| Ưu điểm | `master` luôn có mọi bản sửa nên lỗi không quay lại ở phiên bản sau; bản sửa được review và chạy CI trên dòng chính; viết trên code mới nhất | Sửa nhanh cho bản đang chạy thật; test đúng trên baseline bị ảnh hưởng; không phụ thuộc vào việc `master` có đang ổn định hay không |
| Nhược điểm | Chậm hơn khi cần vá gấp vì phải qua `master` trước; nếu `master` đã khác xa bản cũ thì cherry-pick xuống dễ xung đột, và bản sửa chưa được test trên đúng phiên bản cũ | Dễ quên lan truyền về `master`, làm lỗi tái xuất hiện ở bản phát hành tiếp theo (vì release mới tạo từ `master`); bản sửa viết trên code cũ có thể phải chỉnh lại khi cherry-pick lên `master`; càng nhiều dòng phiên bản càng phải kiểm toán kỹ |

Tóm lại: upstream first ưu tiên tính đúng đắn lâu dài của dòng chính, release first ưu tiên tốc độ vá cho bản đang dùng. Dù chọn cách nào cũng cần bước kiểm toán như Phần F để chắc bản sửa có mặt ở mọi dòng phiên bản bị ảnh hưởng.

### Câu 2: Nếu quên lan truyền bản sửa sang `release/lab05`, lệnh nào ở Phần F sẽ phát hiện?

1. **Lệnh tìm theo dấu vết cherry-pick:**
   ```bash
   git log --all --oneline --grep "cherry picked from commit <FIX_SHA>"
   ```
   Bình thường ra 2 commit (trên `master` và `release/lab05`). Nếu quên, chỉ ra 1, chỉ có bản trên `master`.

2. **Vòng lặp kiểm tra hành vi** trên `v1.0.1`, `v1.1.0` và `master`: dòng `v1.1.0` sẽ in `0` thay vì `1`, vì tìm `"lion"` không ra *The Lion King*. Đây là cách phát hiện trực tiếp nhất vì kiểm tra hành vi thật của phần mềm, không chỉ dựa vào lịch sử commit.

3. Lệnh `git cherry` cũng phát hiện được nếu so đúng hai dòng phiên bản:
   ```bash
   git cherry -v origin/release/lab05 origin/release/lab04
   ```
   Commit `fix: make search_by_title case-insensitive` sẽ có dấu `+` (release/lab05 chưa có thay đổi tương đương) thay vì `-`.

Riêng `git tag --contains <FIX_SHA>` không phát hiện được: cherry-pick tạo commit mới với SHA khác, nên lệnh này chỉ trả về `v1.0.1` dù đã lan truyền hay chưa.
