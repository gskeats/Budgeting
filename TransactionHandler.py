import datetime

class TransactionEngine:

    def __init__(self, csv_transactions):
        self.list_transactions=[]
        self.transactions = self.parse_transactions(csv_transactions)



    def parse_transactions(self,file):
        with open(file,"r") as transaction_file:
            for line in transaction_file:
                args=line.split(",")
                if len(args)==7:
                    self.list_transactions.append(Transaction(*args))
        return self.list_transactions

class Transaction:
    def __init__(self,*args):
        date_list=args[0].split("-")
        date_list=[int(i) for i in date_list]
        self.transaction_date=datetime.date(*date_list)
        self.posted_date=args[1].rstrip()
        self.card_no=args[2].rstrip()
        self.description=args[3].rstrip()
        self.category=args[4].rstrip()
        self.debit=args[5].rstrip()
        self.credit=args[6].rstrip()
        self.values=[self.transaction_date,self.posted_date,self.description,self.category,self.credit,self.debit]


class ChaseRecord:
    def __init__(self,*args):
        date_list=args[1].split("/")
        date=[int(i) for i in reversed(date_list)]
        date[2]=date[2]+date[1]
        date[1]=date[2]-date[1]
        date[2]=date[2]-date[1]
        self.transaction_date=datetime.date(*date)
        self.description=args[2].rstrip()
        self.amount=args[3].rstrip()
        self.type=args[4].rstrip()
        self.balance=args[5].rstrip()
        self.values=[self.transaction_date,self.description,self.amount,self.type,self.balance]


class ChaseTransactionEngine:

    def __init__(self, csv_transactions):
        self.list_transactions=[]
        self.transactions = self.parse_transactions(csv_transactions)


    def parse_transactions(self,file):
        with open(file,"r") as transaction_file:
            for line in transaction_file:
                args=line.split(",")
                if len(args)==8:
                    self.list_transactions.append(ChaseRecord(*args))
        return self.list_transactions




