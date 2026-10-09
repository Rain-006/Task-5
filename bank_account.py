
from decimal import Decimal, InvalidOperation


class BankAccount:
    """Класс для управления банковским счётом."""

    def __init__(self, owner: str, account_number: str):
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError("Имя владельца не должно быть пустым.")

        if not isinstance(account_number, str) or not account_number.strip():
            raise ValueError("Номер счёта не должен быть пустым.")

        self._owner = owner
        self._account_number = account_number
        self._balance = Decimal("0.00")

    @property
    def owner(self):
        """Возвращает имя владельца."""
        return self._owner

    @property
    def account_number(self):
        """Возвращает номер счёта."""
        return self._account_number

    @staticmethod
    def _validate_amount(amount):
        """Проверяет корректность денежной суммы."""
        if isinstance(amount, bool):
            raise ValueError("Сумма должна быть положительным числом.")

        try:
            amount = Decimal(str(amount))
        except (InvalidOperation, ValueError, TypeError):
            raise ValueError("Некорректная сумма.")

        if not amount.is_finite() or amount <= 0:
            raise ValueError("Сумма должна быть положительной.")

        if amount.as_tuple().exponent < -2:
            raise ValueError("Допускается не более двух знаков после запятой.")

        return amount

    def deposit(self, amount):
        """Пополняет счёт."""
        amount = self._validate_amount(amount)
        self._balance += amount

    def withdraw(self, amount):
        """Снимает деньги со счёта."""
        amount = self._validate_amount(amount)

        if amount > self._balance:
            raise ValueError("Недостаточно средств на счёте.")

        self._balance -= amount

    def transfer(self, recipient, amount):
        """Переводит деньги на другой счёт."""
        if not isinstance(recipient, BankAccount):
            raise ValueError("Получатель должен быть банковским счётом.")

        if recipient is self:
            raise ValueError("Нельзя переводить деньги на тот же счёт.")

        amount = self._validate_amount(amount)

        if amount > self._balance:
            raise ValueError("Недостаточно средств для перевода.")

        # Изменяем оба баланса только после всех проверок.
        self._balance -= amount
        recipient._balance += amount

    def get_balance(self):
        """Возвращает текущий баланс."""
        return self._balance

    def is_empty(self):
        """Проверяет, равен ли баланс нулю."""
        return self._balance == Decimal("0.00")