import DatabaseConn
import SQLQuerySkeletons as sqlstring

class DataHandler:
    def __init__(self):
        self.database_conn=DatabaseConn.DatabaseManager()

    def construct_sum_by_column(self,column,numeric,tablename,range_lower='1990-01-01', range_upper='9999-12-31'):
        sql=sqlstring.basic_order_by_sum%(column,numeric,tablename,range_lower,range_upper,column)
        task=[]
        results=self.database_conn.execute(sql,task)
        return results

    def getTotals(self,column,tablename,range_lower='1990-01-01',range_upper='9999-12-31'):
        sql = sqlstring.totals % (column,tablename, range_lower, range_upper)
        task=[]
        results=self.database_conn.execute(sql,task)
        return results[0][0]

    def getIncome(self,column,tablename,range_lower='1990-01-01',range_upper='9999-12-31'):
        sql = sqlstring.income % (column,tablename, range_lower, range_upper)
        task=[]
        results=self.database_conn.execute(sql,task)
        return results[0][0]

    def getSavingsBalance(self,column,tablename,range_lower='1990-01-01',range_upper='9999-12-31'):
        sql = sqlstring.savings_balance % ( range_lower, range_upper)
        task = []
        results = self.database_conn.execute(sql, task)
        return results[0][0]

    def checkMonthOverMonth(self,column,tablename,type=getIncome):
        list_month_value=[]
        for year in sqlstring.years:
            for month in sqlstring.months:
                start=year+"-"+month+"-"+sqlstring.days[0]
                end=year+"-"+month+"-"+sqlstring.days[1]
                result=type(self,column,tablename,start,end)
                list_month_value.append((year+"-"+month,result))
        return list_month_value