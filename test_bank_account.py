
import unittest
from decimal import Decimal

from bank_account import BankAccount


class TestBankAccount(unittest.TestCase):
    """Модульные тесты банковского счёта."""

    def setUp(self):
        """Создаёт тестовые счета перед каждым тестом."""
        self.account = BankAccount("Иван Иванов", "10001")
        self.recipient = BankAccount("Пётр Петров", "10002")

    # 1. Тестирование создания счёта

    def test_account_creation(self):
        self.assertEqual(self.account.owner, "Иван Иванов")
        self.assertEqual(self.account.account_number, "10001")
        self.assertEqual(
            self.account.get_balance(), Decimal("0.00")
        )
        self.assertTrue(self.account.is_empty())

    def test_invalid_account_creation(self):
        with self.assertRaises(ValueError):
            BankAccount("", "10001")

        with self.assertRaises(ValueError):
            BankAccount("Иван Иванов", "")

    # 2. Тестирование пополнения

    def test_deposit(self):
        self.account.deposit("500.00")
        self.assertEqual(
            self.account.get_balance(), Decimal("500.00")
        )

    def test_multiple_deposits(self):
        self.account.deposit("100.00")
        self.account.deposit("250.50")
        self.assertEqual(
            self.account.get_balance(), Decimal("350.50")
        )

    def test_invalid_deposit(self):
        for amount in [0, -100, "abc", None, True, "NaN", "Infinity", "10.123"]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.deposit(amount)

        self.assertTrue(self.account.is_empty())

    # 3. Тестирование снятия

    def test_withdraw(self):
        self.account.deposit("500.00")
        self.account.withdraw("200.00")
        self.assertEqual(
            self.account.get_balance(), Decimal("300.00")
        )

    def test_withdraw_entire_balance(self):
        self.account.deposit("100.00")
        self.account.withdraw("100.00")
        self.assertTrue(self.account.is_empty())

    def test_withdraw_more_than_balance(self):
        self.account.deposit("100.00")

        with self.assertRaises(ValueError):
            self.account.withdraw("150.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("100.00")
        )

    def test_invalid_withdraw(self):
        self.account.deposit("100.00")

        for amount in [0, -10, "abc", True, "NaN", "1.234"]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.withdraw(amount)

        self.assertEqual(
            self.account.get_balance(), Decimal("100.00")
        )

    # 4. Тестирование перевода

    def test_successful_transfer(self):
        self.account.deposit("500.00")
        self.account.transfer(self.recipient, "200.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("300.00")
        )
        self.assertEqual(
            self.recipient.get_balance(), Decimal("200.00")
        )

    def test_transfer_entire_balance(self):
        self.account.deposit("100.00")
        self.account.transfer(self.recipient, "100.00")

        self.assertTrue(self.account.is_empty())
        self.assertEqual(
            self.recipient.get_balance(), Decimal("100.00")
        )

    def test_transfer_more_than_balance(self):
        self.account.deposit("100.00")

        with self.assertRaises(ValueError):
            self.account.transfer(self.recipient, "150.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("100.00")
        )
        self.assertTrue(self.recipient.is_empty())

    def test_transfer_invalid_amount(self):
        self.account.deposit("100.00")

        for amount in [0, -10, "abc", "NaN", "1.234"]:
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    self.account.transfer(self.recipient, amount)

        self.assertEqual(
            self.account.get_balance(), Decimal("100.00")
        )
        self.assertTrue(self.recipient.is_empty())

    def test_transfer_to_invalid_recipient(self):
        self.account.deposit("100.00")

        with self.assertRaises(ValueError):
            self.account.transfer("не счёт", "50.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("100.00")
        )

    def test_transfer_to_same_account(self):
        self.account.deposit("100.00")

        with self.assertRaises(ValueError):
            self.account.transfer(self.account, "50.00")

        self.assertEqual(
            self.account.get_balance(), Decimal("100.00")
        )

    # 5. Тестирование получения баланса

    def test_get_balance_after_operations(self):
        self.account.deposit("1000.00")
        self.account.withdraw("250.00")
        self.assertEqual(
            self.account.get_balance(), Decimal("750.00")
        )

    # 6. Тестирование проверки пустого счёта

    def test_is_empty(self):
        self.assertTrue(self.account.is_empty())

        self.account.deposit("50.00")
        self.assertFalse(self.account.is_empty())

        self.account.withdraw("50.00")
        self.assertTrue(self.account.is_empty())


if __name__ == "__main__":
    unittest.main(verbosity=2)