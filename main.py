from datetime import date

import DataHandler
import DataVisualization
import DatabaseConn
import TransactionHandler

rent = 1950


def insertRecords(filename, recordtype='creditCard'):
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


def getCurrentMonthYear(month=None, year=None):
    today = date.today()
    if month is None:
        month = '%02d' % (today.month - 1)
    else:
        month = '%02d' % (month)
    if year is None:
        year = today.year
    month_year = str(year) + '-' + str(month)
    return month_year


def main(targetStart=None, targetEnd=None, targetYear=None):
    if targetStart is None or targetEnd is None:
        targetStart = getCurrentMonthYear()
        targetEnd = getCurrentMonthYear()

    targetStart = getCurrentMonthYear(targetStart, targetYear)
    targetEnd = getCurrentMonthYear(targetEnd, targetYear)
    data_handler = DataHandler.DataHandler()
    dv = DataVisualization.DataVisualizer(data_handler)

    debit_by_location = data_handler.construct_sum_by_column(column='description', numeric='debit',
                                                             tablename='creditCard',
                                                             range_lower=targetStart + '-01',
                                                             range_upper=targetEnd + '-31')
    dv.barChartByLocation(data=debit_by_location, title="Credit Card Top Spend by Location")

    checking_by_location = data_handler.construct_sum_by_column(column='description', numeric='amount',
                                                                tablename='checkingAccount',
                                                                range_lower=targetStart + '-01',
                                                                range_upper=targetEnd + '-31')
    dv.barChartByLocation(data=checking_by_location, title="Checking Activity by Location", number=3)

    savings_by_location = data_handler.construct_sum_by_column(column='description', numeric='amount',
                                                               tablename='savingsAccount',
                                                               range_lower=targetStart + '-01',
                                                               range_upper=targetEnd + '-31')
    dv.barChartByLocation(data=savings_by_location, title="Savings Activity by Location")

    credit_card_expense_by_category = data_handler.construct_sum_by_column(column='category', numeric='debit',
                                                                           tablename='creditCard',
                                                                           range_lower=targetStart + '-01',
                                                                           range_upper=targetEnd + '-31')
    dv.barChartByLocation(data=credit_card_expense_by_category, title="Credit Card Spend by Category")

    monthly_sum_credit = data_handler.getTotals(column='credit', tablename='creditCard',
                                                range_lower=targetStart + '-01',
                                                range_upper=targetEnd + '-31')
    print("Credit Card: " + monthly_sum_credit.__str__())


    ubs_income = data_handler.getIncome(column='amount', tablename='checkingAccount',
                                        range_lower=targetStart + '-01',
                                        range_upper=targetEnd + '-31')
    print("UBS Income: " + ubs_income.__str__())


    month_over_month_income = data_handler.checkMonthOverMonth(column='amount', tablename='checkingAccount')
    dv.lineChartMonthOverMonth(data=month_over_month_income, title="UBS Income Month over Month")

    month_over_month_expenses = data_handler.checkMonthOverMonth(column='credit', tablename='creditCard',
                                                                 type=DataHandler.DataHandler.getTotals)
    dv.lineChartMonthOverMonth(data=month_over_month_expenses, title="Month over Month Expenses")

    month_over_month_savings = data_handler.checkMonthOverMonth(column='balance', tablename='savingsAccount',
                                                                type=DataHandler.DataHandler.getSavingsBalance)
    dv.lineChartMonthOverMonth(data=month_over_month_savings, title="Savings Balance Month over Month Expenses")

main(targetStart=1, targetEnd=7, targetYear=2021)
