import urllib.request as ub
import urllib
from urllib.error import URLError
import json
import statistics as st
import ssl
import sys
def menu():
    print("Welcome to the Currency terminal")
    print("1: Currency Exchange")
    print("2: Difference in power between 2 currencies at different times")
    print("3: High and Low of a period")
    print("4: Which Currency is more stable")
def frankfurter(url):
    req = ub.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    try:
        with ub.urlopen(req, context=context, timeout=10) as response:
                raw_data = response.read().decode("utf-8")
                data_1 = json.loads(raw_data)
    except urllib.error.URLError:
        print("Sorry API not working properly try again")
        sys.exit()
    return data_1
def Currency_Exchange():
    base = input("What currency are you starting with? (type in the 3 letter code) ")
    quote = input("What currency do you you want to exchange it to (type in the 3 letter code) ")
    amount = float(input("How much money do you have "))
    date = input("What date would you like (yyyy-mm-dd format)")
    url = f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote}&date={date}"  
    data_1 = frankfurter(url)
    data = data_1[0]["rate"]
    data = float(data)
    number = round(data*amount, 2)
    return data, number, quote
def power_over_different_dates():
    base = input("What currency are you starting with? (type in the 3 letter code) ")
    quote = input("What currency do you you want to exchange it to (type in the 3 letter code) ")
    date1 = input("What date would you like to start with (yyyy-mm-dd format and must be or be past 1999-01-04")
    date2 = input("What date would you like to compare it to (yyyy-mm-dd format) ")
    url1 = f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote}&date={date1}"
    url2 = f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote}&date={date2}"
    data_1 = frankfurter(url1)
    data_2 = frankfurter(url2)
    data1 = data_1[0]["rate"]
    data2 = data_2[0]["rate"]
    diff = (data1 - data2)/data2
    return base, quote, data1, data2, diff
def Highs_and_Lows():
    base = input("What currency are you setting as baseline \n(recommended to use USD but if analysing USD use GBP or EUR) ")
    quote = input("What currency are you trying to find highs and lows (type in the 3 letter code) ")
    dateS = input("What is the first date in your range? (yyyy-mm-dd format and must be or be past 1999-01-04) ")
    dateE = input("What is the last date in your range? (yyyy-mm-dd format) ")
    url = f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote}&from={dateS}&to={dateE}"
    data_1 = frankfurter(url)
    high = 0
    for data in data_1:
        date = data["date"]
        data = data["rate"]
        if data > high:
            dateh = date
            high = data
    low = high
    for data in data_1:
        date = data["date"]
        data = data["rate"]
        if data < low:
            datel = date
            low = data
    return base, quote, dateS, dateE, high, low, datel, dateh    
def Stability():
    base = input("What currency are you is your baseline? (rec USD or GBP) ")
    quote1 = input("What is your starting currency? (type in the 3 letter code) ")
    quote2 = input("What currency are you comparing it to? (type 3 letter code) ")
    dateS = input("What is the first date in your range (yyyy-mm-dd format and must be or be past 1999-01-04) ")
    dateE = input("What is the last date? (yyyy-mm-dd format and must be or be past 1999-01-04) ")
    url1 = f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote1}&from={dateS}&to={dateE}"
    url2 = f"https://api.frankfurter.dev/v2/rates?base={base}&quotes={quote2}&from={dateS}&to={dateE}"
    data_1 = frankfurter(url1)
    data_2 = frankfurter(url2)
    numbers1 = [data["rate"] for data in data_1]
    numbers2 = [data["rate"] for data in data_2]
    stability1 = st.stdev(numbers1)
    stability1 = round(stability1, 2)
    stability2 = st.stdev(numbers2)
    stability2 = round(stability2, 2)
    return stability1, stability2, quote1, quote2, dateS, dateE
menu()
choice = input("Which one would you like to use? ")
if choice == "1":
    print("This is the currency exchange panel")
    data, number, quote = Currency_Exchange()
    print(f"With the exchange rate of {data}, you would have approximently {number} {quote}")
elif choice == "2":
    print("Welcome to the strength comparison over 2 different dates ")
    base, quote, data1, data2, diff = power_over_different_dates()
    if diff < 0:
        diff = abs(diff)
        diff = round(diff*100, 2)
        print(f"On the orginal date the exchange rate between {base} and {quote} was {data1}\nOn the next date the exchange rate was {data2} this means {base} has gotten stronger in relation to {quote} by %{diff}")
    elif diff > 0:
        diff = abs(diff)
        diff = round(diff*100, 2)
        print(f"On the orginal date the exchange rate between {base} and {quote} was {data1}\nOn the next date the exchange rate was {data2} this means {base} has gotten weaker in relation to {quote} by %{diff}")
    else:
        print(f"Nothing changes between the two dates, they both have the exchange rate of {data1}")
elif choice == "3":
    print("Welcome to the high and low of a currency between a specific date range")
    base, quote, dateS, dateE, high, low, datel, dateh = Highs_and_Lows()
    print(f"Between the period {dateS} to {dateE} the weakest value of {quote} was {high} {base} on {dateh} and the strongest was {low} {base} on {datel}")
elif choice == "4":
    print("Welcome to the stability tester of currencies")
    stability1, stability2, quote1, quote2, dateS, dateE = Stability()
    if stability1 < stability2:
        print(f"The average daily change of {quote1} between dates {dateS} and {dateE} is {stability1} while the average daily change of {quote2} is {stability2}\nThis means that {quote1} is more stable than {quote2}")
    elif stability1 > stability2:
        print(f"The average daily change of {quote1} between dates {dateS} and {dateE} is {stability1} while the average daily change of {quote2} is {stability2}\nThis means that {quote2} is more stable than {quote1}")

