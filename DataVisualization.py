import math
import pandas
import DataHandler
import plotly.express as px


class DataVisualizer():
    def __init__(self, data_handler=None):
        if data_handler is None:
            data_handler = DataHandler.DataHandler()
        self.data_handler = data_handler

    def barChartByLocation(self, data=None, number=10, title="Amount by Category"):
        if data is None:
            data = self.data_handler.construct_sum_by_column(column='description', numeric='debit',
                                                             tablename='creditCard', range_lower='2021-01-01',
                                                             range_upper='2021-07-31')
        dataframe = pandas.DataFrame(data=data,columns=['Location', 'AggregateSpend'])


        plot = px.bar(dataframe,x="Location", y="AggregateSpend",title=title)
        plot.show()


    def lineChartMonthOverMonth(self, data=None, number=10, title="Amount by Month"):

        if data is None:
            data = self.data_handler.checkMonthOverMonth("amount", "checkingAccount")
        dataframe = pandas.DataFrame(data=data,columns=['Month', 'Aggregate'])

        plot=px.line(dataframe,x="Month",y="Aggregate",title=title)
        plot.show()
