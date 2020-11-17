#!python3
import requests
import json
import csv


api_key = 'Enter Here'
headers = {'Authorization': 'Bearer %s' % api_key}
url = 'https://api.yelp.com/v3/businesses/search'
params = {'term':'restaurants','location':'San Francisco','radius':1000}
hour_array = [0, False, False, False, False, 1, False, False, False, False, 2, False, False, False, False, 3, False, False, False, False,
              4, False, False, False, False, 5, False, False, False, False, 6, False, False, False, False, ]
switch_day = {
    0: [0, False, False, False, False],
    1: [0, False, False, False, False],
    2: [0, False, False, False, False],
    3: [0, False, False, False, False],
    4: [0, False, False, False, False],
    5: [0, False, False, False, False],
    6: [0, False, False, False, False],
}

# parse the hours
def hour_gathering(hours):
    for hour in hours:
        print(hour)
        day = switch_day[hour["day"]]

        start = int(hour["start"])
        end = int(hour["end"])

        # Get total time open
        if start == end:
            day[0] = 24
            day[1] = True
            day[2] = True
            day[3] = True
            day[4] = True
        elif end > start:
            day[0] += end - start
        else: # If open past midnight
            day[0] += 24 - end + start
            day[4] = True

        # Overnight & Morning/Afternoon/Evening
        if hour["is_overnight"]:
            day[4] = True
        if start > end or start < 11:
            day[1] = True
        if end > 14 and start < 12:
            day[2] = True
        if end > 19 and start < 19:
            day[3] = True

    for key, value in switch_day.items():
        key_index = key * 5
        for i in range(5):
            hour_array[key_index+i] = value[i]
    for thing in hour_array:
        row.append(thing)
    return row


req = requests.get(url, params=params, headers=headers) # for search
parsed = json.loads(req.text)
businesses = parsed["businesses"]

with open('test.csv', mode='w') as employee_file:
    #CSV Setup
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    employee_writer.writerow(
        ["Name", "Latitude", "Longitude", "Closed", "Rating", "Review Count", "Transactions", "Price", "Attributes",
         "Day 0 Hours", "Day 0 Morning", "Day 0 Afternoon", "Day 0 Evening", "Day 0 Overnight",
         "Day 1 Hours", "Day 1 Morning", "Day 1 Afternoon", "Day 1 Evening", "Day 1 Overnight",
         "Day 2 Hours", "Day 2 Morning", "Day 2 Afternoon", "Day 2 Evening", "Day 2 Overnight",
         "Day 3 Hours", "Day 3 Morning", "Day 3 Afternoon", "Day 3 Evening", "Day 3 Overnight",
         "Day 4 Hours", "Day 4 Morning", "Day 4 Afternoon", "Day 4 Evening", "Day 4 Overnight",
         "Day 5 Hours", "Day 5 Morning", "Day 5 Afternoon", "Day 5 Evening", "Day 5 Overnight",
         "Day 6 Hours", "Day 6 Morning", "Day 6 Afternoon", "Day 6 Evening", "Day 6 Overnight"])

    for bus in businesses:
        url = 'https://api.yelp.com/v3/businesses/' + bus["id"]

        req = requests.get(url, headers=headers)  # for details
        business = json.loads(req.text)
        #print(business)

        row = [business["name"], business["coordinates"]["latitude"], business["coordinates"]["longitude"],
                business["is_closed"], business["rating"], business["review_count"],
                business["transactions"]]
        if "price" in business:
            row.append(len(business["price"]))
        else:
            row.append("")
        if "attributes" in business:
            row.append(business["attributes"])
        else:
            row.append("")

        hours = business["hours"][0]["open"]
        #print(hours)
        row = hour_gathering(hours)
        employee_writer.writerow(row)
