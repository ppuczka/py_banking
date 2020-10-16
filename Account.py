import banking
import random
from BankingDb import BankingDb


class Account:

    BIN = '400000'

    MENU = """1. Balance
    2. Add income
    3. Do transfer
    4. Close account
    5. Log out
    0. Exit"""

    __db = None

    def __init__(self, card_number, pin_number, menu=MENU, bin=BIN, balance=0):
        self.card_number = card_number
        self.pin_number = pin_number
        self.menu = menu
        self.bin = bin
        self.balance = balance
        self.__db = BankingDb('card.s3db')

    @classmethod
    def account_from_db(cls, num, menu=MENU, bin=BIN):
        cls.__db = BankingDb('card.s3db')
        cls.menu = menu
        cls.bin = bin

        query_ = "SELECT * FROM card WHERE number = ?"
        cursor = cls.__db.execute_query(query_, (num,)).fetchone()
        if cursor is None:
            return False
        else:
            card_number_ = cursor[1]
            pin_number_ = cursor[2]
            balance_ = int(cursor[3])
            return cls(card_number_, pin_number_, menu, bin, balance_)

    @classmethod
    def create_account(cls, menu=MENU, bin=BIN, balance=0):
        card_number_ = cls.generate_account_number(bin)
        pin_number_ = cls.generate_pin_number()
        balance_ = balance
        cls.menu = menu
        cls.bin = bin
        return cls(card_number_, pin_number_, menu, bin, balance_)

    def account_menu_action(self):
        print('You have successfully logged in!')
        print(self.menu)
        while True:
            user_input_ = input(self.menu)
            if user_input_ == '1':
                self.get_balance()
            elif user_input_ == '2':
                amount = int(input('Amount to be added: '))
                self.add_income(amount)
            elif user_input_ == '3':
                receiver = input('Receiver account num: ')
                self.do_transfer(receiver)
            elif user_input_ == '4':
                self.close_account()
            elif user_input_ == '5':
                self.log_out()
            elif user_input_ == '0':
                print('Bye')
                exit()

    @staticmethod
    def generate_account_number(bin_):
        account_identifier = []
        for x in range(9):
            account_identifier.append(str(random.randint(0, 9)))

        card_number_ = bin_ + ''.join(account_identifier)
        card_num_list_ = (int(x) for x in card_number_)
        count_nums_ = []
        y = 0
        for x in card_num_list_:
            if y % 2 == 0:
                x *= 2
            if x > 9:
                x -= 9
            y += 1
            count_nums_.append(x)
        result = 10 - (sum(count_nums_) % 10)
        if result == 10:
            checksum_ = 0
        else:
            checksum_ = result
        return ''.join(card_number_) + str(checksum_)

    @staticmethod
    def generate_pin_number():
        user_pin = []
        for x in range(4):
            user_pin.append(str(random.randint(0, 9)))

        user_pin_str = ''.join(user_pin)
        return user_pin_str

    def save_to_db(self):
        query_ = "INSERT INTO card(number, pin, balance) VALUES (?, ?, ?)"
        rs = self.__db.execute_query(query_, (self.card_number, self.pin_number, self.balance))
        return rs

    def get_card_number(self):
        return self.card_number

    def get_balance(self):
        return print(f"Account balance: ${self.balance}")

    def add_income(self, income):
        self.balance += int(income)
        __query = "UPDATE card SET balance = ? WHERE number = ?"
        rs = self.__db.execute_query(__query, (self.balance, self.card_number))
        print(f"New account balance: {self.balance}")
        return rs

    def do_transfer(self, receiver_account):
        if self.card_number == receiver_account:
            print("You can't transfer money to the same account!")
        else:
            temp_num_arr_str = list(receiver_account)
            if len(temp_num_arr_str) < 16:
                print('Probably you made mistake in card number. Please try again!')
                return False
            temp_num_arr_int = list((int(x) for x in temp_num_arr_str))
            checksum = temp_num_arr_int.pop()
            count_nums_ = []
            y = 0
            for x in temp_num_arr_int:
                if y % 2 == 0:
                    x *= 2
                if x > 9:
                    x -= 9
                y += 1
                count_nums_.append(x)
            if (sum(count_nums_) + checksum) % 10 == 0:
                __query = "SELECT * FROM card WHERE number = ?"
                rs = self.__db.execute_query(__query, (receiver_account,)).fetchone()
                if rs is None:
                    print('Such a card does not exist.')
                    return False
                else:
                    receiver_balance = int(rs[3])
                    to_transfer = int(input('Amount to transfer'))
                    if self.balance < to_transfer:
                        print("Not enough money!")
                        return False
                    else:
                        self.balance -= to_transfer
                        __query = "UPDATE card SET balance = ? WHERE number = ?"
                        self.__db.execute_query(__query, (self.balance, self.card_number))
                        print(f"New account balance: {self.balance}")
                        __transfer_query = "UPDATE card SET balance = ? WHERE number = ?"
                        receiver_balance += to_transfer
                        transfer_rs = self.__db.execute_query(__transfer_query, (receiver_balance, receiver_account))
                        print('Money transfer')
                        return True
            else:
                print('Probably you made mistake in card number. Please try again!')
                return False

    def close_account(self):
        __query = "DELETE FROM card WHERE number = ?"
        self.__db.execute_query(__query, (self.card_number,))
        return True

    @staticmethod
    def log_out():
        print('You have successfully logged out!')
        banking.main_menu()
