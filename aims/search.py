"""Các hàm tìm kiếm đĩa DVD trong AIMS-mini."""


def search_by_category(items, category):
    """Trả về danh sách đĩa thuộc thể loại category."""
    return [dvd for dvd in items if dvd.category == category]


def search_by_title(items, keyword):
    """Trả về danh sách đĩa có tiêu đề chứa keyword."""
    return [dvd for dvd in items if keyword in dvd.title]
