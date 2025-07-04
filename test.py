from datetime import date, time, datetime

d1 = date.today()
print(d1)

d2 = datetime.now()
print(d2)

d3 = date(2020, 3, 21)
print(d3)

time1 = time(4, 35, 30)
print(time1)

#-----------------------

date1 = date(2007, 2, 4)
date2 = date(2016, 7, 16)


date3 = date2 - date1
print(date3)#(date3.days)

user_date = date(2015, 10, 23)
formatted_date = user_date.strftime("%d-%m-%Y")
print(formatted_date)
