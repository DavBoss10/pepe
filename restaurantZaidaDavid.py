# Абстракция
from abc import ABC, abstractmethod


class MenuItem(ABC):

    def __init__(self, name: str, base_price: float):
        self._name = name
        self._base_price = base_price

    @property
    def name(self) -> str:
        return self._name

    @property
    def base_price(self) -> float:
        return self._base_price

    @abstractmethod
    def calculate_price(self) -> float:
        pass


# Блюда
class Pizza(MenuItem):

    def __init__(self, name: str, base_price: float, size: str):
        super().__init__(name, base_price)
        self.size = size

    def calculate_price(self) -> float:
        if self.size.lower() == "большая":
            return self.base_price * 1.30
        return self.base_price


class Drink(MenuItem):

    def __init__(self, name: str, base_price: float, is_ice: bool):
        super().__init__(name, base_price)
        self.is_ice = is_ice

    @property
    def name(self) -> str:
        if self.is_ice:
            return f"{self._name} (со льдом)"
        return self._name

    def calculate_price(self) -> float:
        return self.base_price


class ComboSet(MenuItem):

    def __init__(self, name: str, items: list[MenuItem]):
        super().__init__(name, 0)
        self.items = items

    def calculate_price(self) -> float:
        total = sum(item.calculate_price() for item in self.items)
        return total * 0.85


# Оплата
class PaymentStrategy(ABC):

    @abstractmethod
    def collect_payment(self, amount: float):
        pass


class CardPayment(PaymentStrategy):

    def __init__(self, card_number: str, expiry_date: str):
        self.card_number = card_number
        self.expiry_date = expiry_date

    def collect_payment(self, amount: float):
        if self.expiry_date:
            print(f"Списано {amount:.2f} руб. с карты {self.card_number}")
        else:
            print("Ошибка оплаты: не указан срок действия карты!")


class CashPayment(PaymentStrategy):

    def collect_payment(self, amount: float):
        print(f"Оплата наличными при получении: {amount:.2f} руб.")


# Заказ
class Order:
    STATUSES = ["Создан", "Готовится", "В пути", "Доставлен"]

    def __init__(self):
        self.__items = []
        self.__status_index = 0

    @property
    def status(self) -> str:
        return self.STATUSES[self.__status_index]

    def add_item(self, item: MenuItem):
        if self.__status_index > 0:
            print(
                f"Ошибка! Нельзя добавить '{item.name}'. Заказ уже в статусе '{self.status}'!"
            )
            return
        self.__items.append(item)
        print(f"Добавлено в корзину: {item.name}")

    def next_step(self):
        if self.__status_index < len(self.STATUSES) - 1:
            self.__status_index += 1
            print(f"Статус заказа изменен на: {self.status}")
        else:
            print("Заказ уже доставлен!")

    def get_total_cost(self) -> float:
        return sum(item.calculate_price() for item in self.__items)

    def pay(self, payment_method: PaymentStrategy):
        total = self.get_total_cost()
        print("\n--- Оформление оплаты ---")
        print(f"Сумма к оплате: {total:.2f} руб.")
        payment_method.collect_payment(total)


# Запуск
if __name__ == "__main__":
    my_order = Order()

    pizza1 = Pizza("Пепперони", 500, "Большая")
    drink1 = Drink("Кола", 100, is_ice=True)

    combo1 = ComboSet(
        "Комбо Обед",
        [
            Pizza("Маргарита", 400, "Маленькая"),
            Drink("Сок", 100, is_ice=False),
        ],
    )

    my_order.add_item(pizza1)
    my_order.add_item(drink1)
    my_order.add_item(combo1)

    card = CardPayment("4400 1234 5678 9012", "12/28")
    my_order.pay(card)

    print("\n--- Переход к готовке ---")
    my_order.next_step()

    extra_pizza = Pizza("4 Сыра", 450, "Маленькая")
    my_order.add_item(extra_pizza)

    my_order.next_step()
    my_order.next_step()
