import csv

with open("exchange_rates.csv") as file:
    reader = csv.DictReader(file)
    exchange_rates = list(reader)


print(exchange_rates)

