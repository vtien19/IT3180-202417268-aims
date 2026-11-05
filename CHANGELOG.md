# Changelog

Mọi thay đổi đáng chú ý của AIMS-mini được ghi lại trong tệp này.

Định dạng theo [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/),
số phiên bản theo [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]
### Added
- `Cart.sort_by_title()` và `Cart.sort_by_cost()`: sắp xếp đĩa trong giỏ hàng
- `search_by_category()` trong `aims/search.py`: tìm đĩa theo thể loại

## [1.0.0] - 2026-11-05
### Added
- `Cart.print_cart()`: in danh sách đĩa và tổng tiền, báo "The cart is empty" khi giỏ trống
- `search_by_title()` trong `aims/search.py`: tìm đĩa theo tiêu đề
- `Cart.total_cost_with_discount()`: tính tổng tiền sau giảm giá, báo `ValueError` khi phần trăm không hợp lệ
- Bộ unit test trong `tests/` cho giỏ hàng, giảm giá và tìm kiếm
- Mẫu mô tả Pull Request và biểu đồ use case

### Changed
- Gom mã nguồn vào package `aims/`
- Thông báo khi thêm đĩa chuyển sang tiếng Việt
- Chương trình in số phiên bản khi khởi động

### Fixed
- Giỏ hàng nhận đĩa thứ 21 dù giới hạn là 20 (#9)

[Unreleased]: https://github.com/vtien19/it3180-202417268-aims/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/vtien19/it3180-202417268-aims/compare/v0.1.0...v1.0.0
