MAX_NUMBERS_ORDERED = 20


class Cart:
    """Giỏ hàng chứa tối đa MAX_NUMBERS_ORDERED đĩa DVD."""

    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= MAX_NUMBERS_ORDERED:
            print("The cart is almost full")
            return False
        self.items.append(dvd)
        print("The disc has been added")
        return True

    def remove_dvd(self, dvd):
        if dvd in self.items:
            self.items.remove(dvd)
            print("The disc has been removed")
            return True
        print("The disc is not in the cart")
        return False

    def total_cost(self):
        return sum(item.cost for item in self.items)

    def print_cart(self):
        """In danh sách đĩa trong giỏ và tổng tiền."""
        if not self.items:
            print("The cart is empty")
            return
        print("********************** CART **********************")
        print("Ordered items:")
        for index, dvd in enumerate(self.items, start=1):
            print(f"{index}. {dvd}")
        print(f"Total cost: {self.total_cost():.2f} $")
        print("**************************************************")
