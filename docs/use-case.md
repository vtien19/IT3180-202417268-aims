# Biểu đồ use case – AIMS-mini

Tác nhân: **Khách hàng**, dùng chương trình dòng lệnh để quản lý giỏ hàng DVD.

```mermaid
flowchart LR
    KH(["Khách hàng"])
    subgraph AIMS["AIMS-mini"]
        UC1(["Thêm đĩa vào giỏ hàng"])
        UC2(["Xóa đĩa khỏi giỏ hàng"])
        UC3(["Xem giỏ hàng"])
        UC4(["Xem tổng tiền"])
        UC5(["Tìm đĩa theo tiêu đề"])
    end
    KH --- UC1
    KH --- UC2
    KH --- UC3
    KH --- UC5
    UC3 -. "«include»" .-> UC4
```

| Use case | Hàm thực hiện |
|---|---|
| Thêm đĩa vào giỏ hàng | `Cart.add_dvd()` |
| Xóa đĩa khỏi giỏ hàng | `Cart.remove_dvd()` |
| Xem giỏ hàng | `Cart.print_cart()` |
| Xem tổng tiền | `Cart.total_cost()` |
| Tìm đĩa theo tiêu đề | `search_by_title()` |
