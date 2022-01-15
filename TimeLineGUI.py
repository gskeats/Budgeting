from tkinter import *
from tkcalendar import Calendar
from datetime import date
import TransactionHandler
import DatabaseConn
import DataHandler
import DataVisualization

class CalendarGUI():

    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x500")

        self.frame1=Frame(self.root,height=150,width=300)
        self.frame2=Frame(self.root,height=150,width=300)

        self.frame1.pack(side=TOP)
        self.frame2.pack()

        self.cal=Calendar(self.frame1, selectmode='day',
                       year=2019, month=6,
                       day=14,selectforeground='red',date_pattern="yyyy-mm-dd")
        self.cal.pack(fill="both",expand=True,side=LEFT)
        self.populateCalendar()

        self.start_date=""
        self.end_date=""

    def populateCalendar(self):
        Button(self.frame2, text="Set Start Date",
               command=self.start_date).grid(row=0,column=0)
        Button(self.frame2, text="Set End Date", command=self.end_date).grid(row=0,column=1)
        Button(self.frame2, text="Get Current Day", command=self.set_end_today).grid(row=0,column=2)
        Button(self.frame2, text="Exit", command=self.terminate).grid(row=0,column=3)
        Button(self.frame2, text="Generate Report",command=self.generate_report).grid(row=1,column=1)
        Button(self.frame2, text="Insert CreditCard", command=self.insert_credit_card).grid(row=2,column=0)
        Button(self.frame2, text="Insert Savings", command=self.insert_savings).grid(row=2,column=1)
        Button(self.frame2, text="Insert Checking", command=self.insert_checking).grid(row=2,column=2)

        self.filename=Text(self.root,height=5,width=300)
        self.filename.config(highlightthickness = 4, borderwidth=2,relief="sunken")
        self.filename.pack(pady=20)

        self.start_date_label = Label(self.root, text="")
        self.start_date_label.pack(pady=20)

        self.end_date_label = Label(self.root, text="")
        self.end_date_label.pack(pady=20)

        self.root.mainloop()

    def insert_credit_card(self):
        self.insertRecords(self.filename.get("1.0",END).rstrip(),recordtype='creditCard')
        self.filename.delete("1.0",END)

    def insert_checking(self):
        self.insertRecords(self.filename.get("1.0",END).rstrip(),recordtype='checkingRecord')
        self.filename.delete("1.0",END)

    def insert_savings(self):
        self.insertRecords(self.filename.get("1.0",END).rstrip(),recordtype='savingsRecord')
        self.filename.delete("1.0",END)

    def insertRecords(self,filename, recordtype='creditCard'):
        if recordtype is 'creditCard':
            engine = TransactionHandler.TransactionEngine(filename)
            tablename = 'creditCard'
        elif recordtype is 'savingsRecord':
            engine = TransactionHandler.ChaseTransactionEngine(filename)
            tablename = 'savingsAccount'
        elif recordtype is 'checkingRecord':
            engine = TransactionHandler.ChaseTransactionEngine(filename)
            tablename = 'checkingAccount'
        else:
            exit(0)

        db = DatabaseConn.DatabaseManager()
        db.populate_transactions(engine.list_transactions, table_name=tablename)

    def set_end_today(self):
        today = date.today()
        self.end_date=self.cal.format_date(today)
        self.end_date_label.config(text="End Date is: " + self.end_date)

    def start_date(self):
        self.start_date_label.config(text="Start Date is: " + self.cal.get_date())
        self.start_date=self.cal.get_date()

    def end_date(self):
        self.end_date_label.config(text="End Date is: " + self.cal.get_date())
        self.end_date=self.cal.get_date()

    def terminate(self):
        exit()

    def generate_report(self):

        data_handler = DataHandler.DataHandler()
        dv = DataVisualization.DataVisualizer(data_handler)

        debit_by_location = data_handler.construct_sum_by_column(column='description', numeric='debit',
                                                                 tablename='creditCard',
                                                                 range_lower=self.start_date,
                                                                 range_upper=self.end_date)
        dv.barChartByLocation(data=debit_by_location, title="Credit Card Top Spend by Location")

        checking_by_location = data_handler.construct_sum_by_column(column='description', numeric='amount',
                                                                    tablename='checkingAccount',
                                                                    range_lower=self.start_date,
                                                                    range_upper=self.end_date)
        dv.barChartByLocation(data=checking_by_location, title="Checking Activity by Location", number=3)

        savings_by_location = data_handler.construct_sum_by_column(column='description', numeric='amount',
                                                                   tablename='savingsAccount',
                                                                   range_lower=self.start_date,
                                                                   range_upper=self.end_date)
        dv.barChartByLocation(data=savings_by_location, title="Savings Activity by Location")

        credit_card_expense_by_category = data_handler.construct_sum_by_column(column='category', numeric='debit',
                                                                               tablename='creditCard',
                                                                               range_lower=self.start_date,
                                                                               range_upper=self.end_date)
        dv.barChartByLocation(data=credit_card_expense_by_category, title="Credit Card Spend by Category")

        monthly_sum_credit = data_handler.getTotals(column='credit', tablename='creditCard',
                                                    range_lower=self.start_date,
                                                    range_upper=self.end_date)
        print("Credit Card: " + monthly_sum_credit.__str__())

        ubs_income = data_handler.getIncome(column='amount', tablename='checkingAccount',
                                            range_lower=self.start_date,
                                            range_upper=self.end_date)
        print("UBS Income: " + ubs_income.__str__())

        month_over_month_income = data_handler.checkMonthOverMonth(column='amount', tablename='checkingAccount')
        dv.lineChartMonthOverMonth(data=month_over_month_income, title="UBS Income Month over Month")

        month_over_month_expenses = data_handler.checkMonthOverMonth(column='credit', tablename='creditCard',
                                                                     type=DataHandler.DataHandler.getTotals)
        dv.lineChartMonthOverMonth(data=month_over_month_expenses, title="Month over Month Expenses")

        month_over_month_savings = data_handler.checkMonthOverMonth(column='balance', tablename='savingsAccount',
                                                                    type=DataHandler.DataHandler.getSavingsBalance)
        dv.lineChartMonthOverMonth(data=month_over_month_savings, title="Savings Balance Month over Month Expenses")

calendar=CalendarGUI()