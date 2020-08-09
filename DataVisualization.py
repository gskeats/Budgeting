import seaborn as sns
import matplotlib.pyplot as plt
import DataHandler
import pandas
import math

class DataVisualizer():

    def __init__(self,data_handler=None):
        if data_handler is None:
            data_handler=DataHandler.DataHandler()
        self.data_handler=data_handler


    def barChartByLocation(self,data=None,number=10,title="Amount by Category"):
        if data is None:
            data = self.data_handler.construct_sum_by_column(column='description',numeric='debit',tablename='creditCard',range_lower='2020-05-01',range_upper='2020-05-31')
        dataframe = pandas.DataFrame(data=data, columns=['Location', 'AggregateSpend'])

        sns.set()
        plot=sns.catplot(x="Location", y="AggregateSpend",kind="bar",palette=sns.color_palette("GnBu_d"),
                    data=dataframe.nlargest(number,'AggregateSpend'),height=7,aspect=2)

        y=dataframe["AggregateSpend"]
        for x in range(0,dataframe.shape[0]):
            plt.annotate(round(dataframe["AggregateSpend"][x],2),xy=(x,y[x]))

        plt.title(title)
        plt.draw()
        plt.waitforbuttonpress()
        plt.close()

    def lineChartMonthOverMonth(self,data=None,number=10,title="Amount by Month"):

        a4_dims = (15, 10)
        fig, ax = plt.subplots(figsize=a4_dims)

        if data is None:
            data = self.data_handler.checkMonthOverMonth("amount","checkingAccount")
        dataframe = pandas.DataFrame(data=data, columns=['Month', 'Aggregate'])

        sns.set()
        plot = sns.lineplot(ax=ax,x="Month", y="Aggregate", palette=sns.color_palette("GnBu_d"),
                           data=dataframe, marker='o')

        y = dataframe["Aggregate"]
        point=0
        for index in range(0,dataframe.shape[0]):
            if not math.isnan(y[index]):
                plt.annotate(round(dataframe["Aggregate"][index], 2), xy=(point, y[index]))
                point+=1


        plt.title(title)
        #plt.draw()
        plt.waitforbuttonpress()
        plt.close()
