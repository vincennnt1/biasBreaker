import requests
import os
import json
import csv

FILE = "history.csv"
INFO_FILE = "appInfo.json"

def submit(row):
    with open(FILE, 'a', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(row)
    
    # UPDATING ID COUNT
    with open(INFO_FILE, 'r') as file:
        info = json.load(file)
    
    currentID = info.get("idNum")
    info['idNum'] = currentID + 1

    with open(INFO_FILE, 'w') as file:
        json.dump(info, file, indent=4)


def remove(id):
    rows = []

    with open(FILE, 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader if row[0] != str(id)]

    with open(FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

# finds a row based on id, if id doesnt exist, returns 0
def find(id):
    with open(FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == str(id):
                return row
    return 0
