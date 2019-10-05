#!python3
import requests
import json
import csv

api_key = 'x7-Y6Xx3bYocGlXvipR-fXVgVDpxzuAEyLQN5ufLJdq5LiLxxP12YwYMMy7EUL3y91SPrGQIGRkUdVgnd_ZaOxLw3fb4WD4sPocqBTtaGDXNYWxIzMKHfzXkkP2XXXYx'
headers = {'Authorization': 'Bearer %s' % api_key}

url = 'https://api.yelp.com/v3/businesses/bZ7lvi5_BQ6UKK10OKPV7Q'
params = {'term':'restaurants','location':'San Francisco'}

#req = requests.get(url, params=params, headers=headers) # for search
req = requests.get(url, headers=headers) # for details

parsed = json.loads(req.text)

#businesses = parsed["businesses"]

print(parsed["name"])
print(parsed["coordinates"]["latitude"])
print(parsed["coordinates"]["longitude"])
print(parsed["hours"])
print(parsed["is_closed"])
print(parsed["price"])
print(parsed["rating"])
print(parsed["review_count"])
print(parsed["transactions"])
#print(parsed["attributes"])

with open('test.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(
        ["Name", "Latitude", "Longitude", "Closed", "Price", "Rating", "Review Count", "Transactions", "Attributes",
         "Monday Overnight", "Monday Op"])
    try:
        employee_writer.writerow([parsed["name"], parsed["coordinates"]["latitude"], parsed["coordinates"]["longitude"],
                                  parsed["is_closed"], parsed["price"], parsed["rating"], parsed["review_count"],
                                  parsed["transactions"], parsed["attributes"]])
    except:
        employee_writer.writerow([parsed["name"], parsed["coordinates"]["latitude"], parsed["coordinates"]["longitude"],
                                  parsed["is_closed"], parsed["price"], parsed["rating"], parsed["review_count"],
                                  parsed["transactions"], "", ])




# with open('test.txt') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
#             line_count += 1
#     print(f'Processed {line_count} lines.')

#Name of business, lat, lon, opening hours of business, overnight hours, permanently closed, price, rating, review count, transactions, attributes


# for business in businesses:
#     print("Name:", business["name"])
#     print("Rating:", business["rating"])
#     print("Address:", " ".join(business["location"]["display_address"]))
#     print("Phone:", business["phone"])
#     print("\n")
#
#     id = business["id"]
#
#     url="https://api.yelp.com/v3/businesses/" + id + "/reviews"
#
#     req = requests.get(url, headers=headers)
#
#     parsed = json.loads(req.text)
#
#     reviews = parsed["reviews"]
#
#     print("--- Reviews ---")
#
#     for review in reviews:
#         print("User:", review["user"]["name"], "Rating:", review["rating"], "Review:", review["text"], "\n")
