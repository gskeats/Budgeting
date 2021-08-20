import sqlite3

import SQLQuerySkeletons as sqlstrings


class DatabaseManager:
    def __init__(self, db_name=None):
        if db_name is None:
            db_name = 'Budgeting.db'
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def insert_transaction(self, transaction, string):
        self.execute(string, transaction.values)
        self.db.commit()

    def populate_transactions(self, list_transactions, table_name='creditCard'):
        self.print_warning(list_transactions, table_name)
        count = 0
        if table_name == 'creditCard':
            inserter_string = sqlstrings.insert_creditCard
        else:
            inserter_string = sqlstrings.insert_Chase % table_name

        for transaction in list_transactions:
            self.insert_transaction(transaction, inserter_string)
            count += 1
        print("%i records inserted" % count)

    def print_warning(self, transactions, table_name):
        print("Warning you are about to insert the following records to %s" % table_name)
        for transaction in transactions:
            print(transaction.__dict__)
        response = input("Press y to accept, n to reject changes\n")
        if response != "y":
            print("Aborting, exiting")
            exit(0)

    def execute(self, sql, task):
        self.cursor.execute(sql, task)
        return list(self.cursor)
