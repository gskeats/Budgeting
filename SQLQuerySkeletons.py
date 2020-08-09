basic_order_by_sum="SELECT %s, SUM(%s) COLUMNSUM FROM %s WHERE transactionDate BETWEEN '%s' AND '%s' GROUP BY %s ORDER BY COLUMNSUM DESC"
insert_creditCard="INSERT INTO creditCard(transactionDate,postedDate,description,category,credit,debit) VALUES(?,?,?,?,?,?)"
insert_Chase="INSERT INTO %s(transactionDate,description,amount,type,balance) VALUES(?,?,?,?,?)"
totals="SELECT SUM(%s) COLUMNSUM FROM %s WHERE transactionDate BETWEEN '%s' AND '%s'"
income="SELECT SUM(%s) COLUMNSUM FROM %s WHERE description LIKE '%%UBS Business%%' AND transactionDate BETWEEN '%s' AND '%s'"
savings_balance="SELECT max(balance) FROM savingsAccount WHERE transactionDate BETWEEN '%s' AND '%s'"


years=['2019','2020']
days=['01','31']
months=['01','02','03','04','05','06','07','08','09','10','11','12']
