# Write your code here
import random
# import BankingDb
import Account


# def account_login(account_number):
#     check_account_query = f"SELECT * FROM card WHERE number=? , {account_number}"
#     user_account_num = input('Enter your card number: \n')
#     user_pin = input('Enter your PIN: \n')
#     if accounts.__contains__(user_account_num):
#         if user_pin == accounts[user_account_num]:
#             user_account = Account(user_account_num, user_pin)
#             user_account.account_menu_action()
#         else:
#             print('Wrong card number or PIN!')
#     else:
#         print('Wrong card number or PIN!')


def main_menu():
    user_input = input(f"""1. Create an account
2. Log into account
0. Exit   
""")
    if user_input == '1':
        new_account = Account.Account.create_account()
        new_account.save_to_db()
        print(new_account.card_number)
        print(new_account.pin_number)
    elif user_input == '2':
        print('Log into account')
        usr_account = input("Enter Account number ")
        db_account = Account.Account.account_from_db(usr_account)
        if db_account:
            print(f"Account number: {db_account.card_number}")
            usr_pin = input("Enter pin ")
            print(db_account.pin_number)
            if usr_pin == str(db_account.pin_number):
                db_account.account_menu_action()

            else:
                print("Wrong pin number")
        else:
            print(f"Wrong account number: {usr_account} account in DB \n Please provide correct account number:")
    elif user_input == '0':
        print('Bye')
        exit()


def main():
    # banking_database = BankingDb.BankingDb('card.s3db')
    # banking_database.create_accounts_table()
    while True:
        main_menu()


if __name__ == "__main__":
    main()
