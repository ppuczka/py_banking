import _sqlite3


class BankingDb:

    sql_create_account_table_query = """ CREATE TABLE IF NOT EXISTS card (
                                           id INTEGER PRIMARY KEY,
                                           number TEXT,
                                           pin TEXT,
                                           balance INTEGER DEFAULT 0
                                       ); """

    __connection = None
    __cursor = None

    def __init__(self, database):
        self.__database = database
        self.__connection = _sqlite3.connect(self.__database)

    def create_accounts_table(self):
        try:
            __cursor = self.__connection.cursor()
            __cursor.execute(self.sql_create_account_table_query)
        except _sqlite3.Error as e:
            print(e)
        return self.__cursor

    def execute_no_params_query(self, query):
        try:
            __cursor = self.__connection.cursor()
            __cursor.execute(query)
            self.__connection.commit()
        except _sqlite3.Error as e:
            print(e)
        return self.__cursor

    def execute_query(self, query, params):
        rs = self.__connection.execute(query, params)
        self.__connection.commit()
        print(f'Total executed query: {self.__connection.total_changes}')
        return rs




