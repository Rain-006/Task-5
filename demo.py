from bank_account import BankAccount


ivan = BankAccount("Иван Иванов", "10001")
petr = BankAccount("Пётр Петров", "10002")

print("Баланс Ивана при создании:", ivan.get_balance())
print("Счёт пустой:", ivan.is_empty())

ivan.deposit("1000.00")
ivan.withdraw("250.00")
ivan.transfer(petr, "300.00")

print("Баланс Ивана после операций:", ivan.get_balance())
print("Баланс Петра после перевода:", petr.get_balance())
print("Счёт Ивана пустой:", ivan.is_empty())

try:
    ivan.withdraw("500.00")
except ValueError as error:
    print("Снятие отклонено:", error)
    print("Баланс Ивана не изменился:", ivan.get_balance())
