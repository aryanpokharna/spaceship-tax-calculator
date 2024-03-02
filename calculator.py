from datetime import datetime
import json

def organise():
    with open('response.json', 'r') as f:
        data = json.load(f)
    
    investments = data["data"]["contact"]["account"]["saverProductInstances"][0]["investments"]
    transactions = investments["transactions"]

    FY20 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2019-07-01 to 2020-06-30
    FY21 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2020-07-01 to 2021-06-30
    FY22 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2021-07-01 to 2022-06-30
    FY23 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2022-07-01 to 2023-06-30
    FY24 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2023-07-01 to 2024-06-30
    # typeName = []

    allApplications = []
    allRedemptions = []
      
    for t in transactions:

        # if t["__typename"] not in typeName:
        #     typeName.append(t["__typename"])

        if t["status"] != "PAID":
            continue
        
        if t["__typename"] == "Application":
            allApplications.append(t)
        
        if t["__typename"] == "Redemption":
            allRedemptions.append(t)
        
        date_str = t["unitExchange"]["unitPrice"]["effectiveDate"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")

        if date_obj < datetime(2020, 7, 1):
            if t["__typename"] == "AccountFee":
                FY20["fees"].append(t)
            elif t["__typename"] == "Application":
                FY20["application"].append(t)
            elif t["__typename"] == "Referral":
                FY20["referral"].append(t)
            elif t["__typename"] == "Redemption":
                FY20["redemption"].append(t)
        
        elif date_obj < datetime(2021, 7, 1):
            if t["__typename"] == "AccountFee":
                FY21["fees"].append(t)
            elif t["__typename"] == "Application":
                FY21["application"].append(t)
            elif t["__typename"] == "Referral":
                FY21["referral"].append(t)
            elif t["__typename"] == "Redemption":
                FY21["redemption"].append(t)
        
        elif date_obj < datetime(2022, 7, 1):
            if t["__typename"] == "AccountFee":
                FY22["fees"].append(t)
            elif t["__typename"] == "Application":
                FY22["application"].append(t)
            elif t["__typename"] == "Referral":
                FY22["referral"].append(t)
            elif t["__typename"] == "Redemption":
                FY22["redemption"].append(t)
        
        elif date_obj < datetime(2023, 7, 1):
            if t["__typename"] == "AccountFee":
                FY23["fees"].append(t)
            elif t["__typename"] == "Application":
                FY23["application"].append(t)
            elif t["__typename"] == "Referral":
                FY23["referral"].append(t)
            elif t["__typename"] == "Redemption":
                FY23["redemption"].append(t)
        
        else:
            if t["__typename"] == "AccountFee":
                FY24["fees"].append(t)
            elif t["__typename"] == "Application":
                FY24["application"].append(t)
            elif t["__typename"] == "Referral":
                FY24["referral"].append(t)
            elif t["__typename"] == "Redemption":
                FY24["redemption"].append(t)
    # print(typeName)
                
    taxCalculator(allApplications, allRedemptions)

    return FY20, FY21, FY22, FY23, FY24

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
        oldestBuyUnits = 0
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

            # Increment Total Buy Counter
            oldestBuyUnits += buy.qty

            # P&L
            buy.pl = (sell.unit - buy.unit) * buy.qty
            transaction.pl += buy.pl 

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
    report([FY20, FY21, FY22, FY23, FY24])

def report(FY_array):
    with open('transaction_report.txt', 'w') as file:
        for i, transactions in enumerate(FY_array, start=1):
            total = 0
            totalCGT = 0
            breaker = "-"*80 + "\n"
            file.write("\n")
            file.write("FY" + str(19 + i) + "\n")
            file.write(breaker)
            file.write("{:<11}|{:5}|{:10}|{:9}|{:10}|{:8}|{:3}|{:8}\n".format("Date", "Type", " Quantity", "  Unit", "  Total", "  P/(L)", "CGT", "  P/(L)"))
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

def date(transaction):
    date_str = transaction["unitExchange"]["unitPrice"]["effectiveDate"]
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return date_obj

def yearlySummary(FY):
    opening = 0
    deposit = 0
    referral = 0
    fee = 0
    withdraw = 0
    closing = 0

    # Calculate FY Deposits
    for f in FY["application"]:
        deposit += float(f["audAmount"])

    # Calculate FY Deposits
    for f in FY["referral"]:
        referral += float(f["audAmount"])
    
    # Calculate FY Fees
    for f in FY["fees"]:
        fee += float(f["audAmount"])

    # Calculate FY Withdraws
    for f in FY["redemption"]:
        withdraw += float(f["audAmount"])


    return deposit, referral, fee, withdraw
    

FY20, FY21, FY22, FY23, FY24 = organise()