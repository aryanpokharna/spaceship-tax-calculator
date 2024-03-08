from datetime import datetime
import json

class Transaction():
    def __init__(self, sell):
        self.s = sell
        self.b = []
        self.pl = 0
        self.tax = 0

class Sell():
    def __init__(self):
        self.date = None
        self.unit = None
        self.qty = None
        self.total = None

class Buy():
    def __init__(self):
        self.date = None
        self.unit = None
        self.qty = None
        self.total = None
        self.pl = None
        self.disc = False
        self.discTotal = 0

def organise():
    with open('response.json', 'r') as f:
        data = json.load(f)
    
    transactions = data["data"]["contact"]["account"]["saverProductInstances"][0]["investments"]["transactions"]

    allApplications = []
    allRedemptions = []
    allFees = []
      
    for t in transactions:

        if t["status"] != "PAID":
            continue
        
        if t["__typename"] == "Application":
            allApplications.append(t)
        
        if t["__typename"] == "Redemption":
            allRedemptions.append(t)

        if t["__typename"] == "Referral":
            allApplications.append(t)

        if t["__typename"] == "AccountFee":
            allRedemptions.append(t)
                
    return allApplications, allRedemptions

def date(transaction):
    date_str = transaction["unitExchange"]["unitPrice"]["effectiveDate"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj 

def taxCalculator(allA, allR):

    FY20 = []
    FY21 = []
    FY22 = []
    FY23 = []
    FY24 = []

    while allR:

        # Object: SELL 
        sell = Sell()
        oldestSell = allR.pop()
        sell.date = date(oldestSell) 
        sell.unit = float(oldestSell['unitExchange']['unitPrice']['price']) 
        sell.qty = float(oldestSell['unitExchange']['units']) * -1
        sell.total = float(oldestSell['audAmount'])

        # Object: Transaction 
        transaction = Transaction(sell)

        # Financial Year
        if sell.date < datetime(2020, 7, 1):
            FY20.append(transaction)
        elif sell.date < datetime(2021, 7, 1):
            FY21.append(transaction)
        elif sell.date < datetime(2022, 7, 1):
            FY22.append(transaction)
        elif sell.date < datetime(2023, 7, 1):
            FY23.append(transaction)
        else:
            FY24.append(transaction)
        
        # Counter
        oldestBuyUnits = float(0)
        oldestBuy = None

        while sell.qty > oldestBuyUnits:

            # Object(s): BUY
            buy = Buy()
            oldestBuy = allA.pop()      
            buy.date = date(oldestBuy)
            buy.unit = float(oldestBuy['unitExchange']['unitPrice']['price'])
            buy.qty = float(oldestBuy['unitExchange']['units'])
            buy.total = float(oldestBuy['audAmount'])

            if oldestBuyUnits + buy.qty > sell.qty:
                # Account for partial sells
                gap = sell.qty - oldestBuyUnits
                total = gap * buy.unit

                oldestBuy['unitExchange']['units'] = buy.qty - gap
                oldestBuy['audAmount'] = buy.total - total
                allA.append(oldestBuy)

                buy.qty = sell.qty - oldestBuyUnits
                buy.total = total

            # P&L
            if oldestSell["__typename"] != "AccountFee":
                buy.pl = (sell.unit - buy.unit) * buy.qty
            else:
                buy.pl = -buy.total
            transaction.pl += buy.pl

            # Increment Total Buy Counter
            oldestBuyUnits += buy.qty

            # CGT Discount
            if (sell.date - buy.date).days > 366: 
                buy.disc = True

            # P&L CGT Discount
            if buy.pl > 0 and buy.disc:
                buy.discTotal = buy.pl / 2
                transaction.tax += buy.discTotal

            # Add Buy to Transaction
            transaction.b.append(buy)

    # allA remainder should be current balance.
    return [FY20, FY21, FY22, FY23, FY24]

def report(FY_array):
    with open('transaction_report.txt', 'w') as file:
        for i, transactions in enumerate(FY_array, start=1):
            total = 0
            totalCGT = 0
            breaker = "-"*80 + "\n"
            file.write("\n")
            file.write("FY" + str(19 + i) + "\n")
            file.write(breaker)
            file.write("{:<11}|{:5}|{:10}|{:9}|{:10}|{:8}|{:3}|{:8}\n".format("Date", "Type", " Quantity", "  Unit $", "  Total", "  P/(L)", "CGT", "  P/(L)"))
            for j, transaction in enumerate(transactions, start=1):
                file.write(breaker)
                sell = transaction.s
                file.write(f"{sell.date.strftime('%Y-%m-%d').ljust(11)}|{'SELL'.ljust(5)}|{(-1 * sell.qty):>10.2f}|{sell.unit:>9.2f}|{sell.total:>10.2f}|{'':>8}|{'':>3}|{'':>8}\n")
                for buy in transaction.b:
                    file.write(f"{buy.date.strftime('%Y-%m-%d').ljust(11)}|{'BUY'.ljust(5)}|{buy.qty:>10.2f}|{buy.unit:>9.2f}|{buy.total:>10.2f}|{buy.pl:>8.2f}|{' Y ' if buy.disc else ' N ':>3}|{'' if not buy.disc else buy.discTotal:>8}\n")
                    total += buy.pl
                    totalCGT += buy.discTotal
                file.write(breaker)
                file.write("{:<11}|{:5}|{:10}|{:9}|{:10}|{:8}|{:3}|{:8}\n".format("", " NET ", "", "", "", round(transaction.pl, 2), "", round(transaction.tax, 2)))
            file.write(breaker)
            file.write("{:<11}|{:5}|{:10}|{:9}|{:10}|{:8}|{:3}|{:8}\n".format("", "TOTAL", "", "", "", round(total, 2), "", round(totalCGT, 2)))
            file.write(breaker)   

allApplications, allRedemptions = organise()
FY_array = taxCalculator(allApplications, allRedemptions)
report(FY_array)