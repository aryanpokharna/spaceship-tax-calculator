from datetime import datetime
import json

def calculate():
    with open('response.json', 'r') as f:
        data = json.load(f)
    
    investments = data["data"]["contact"]["account"]["saverProductInstances"][0]["investments"]
    transactions = investments["transactions"]

    FY20 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2019-07-01 to 2020-06-30
    FY21 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2020-07-01 to 2021-06-30
    FY22 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2021-07-01 to 2022-06-30
    FY23 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2022-07-01 to 2023-06-30
    FY24 = {"fees": [], "application": [], "referral": [], "redemption": []} # 2023-07-01 to 2024-06-30

    for t in transactions:
        if t["status"] != "PAID":
            continue
        
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

    return FY20, FY21, FY22, FY23, FY24

def report(FY):
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
    

FY20, FY21, FY22, FY23, FY24 = calculate()

print(report(FY20))
print(report(FY21))
print(report(FY22))
print(report(FY23))
print(report(FY24))