import json
from datetime import datetime, timedelta
import csv

def get_mod(modify):
    d = timedelta(hours=0)
    if modify == "hour":
        d = timedelta(hours=1)
    elif modify == "3hour":
        d = timedelta(hours=3)
    elif modify == "day":
        d = timedelta(days=1)
    return d


def middle_x_all(xarg: list, yarg: list, date: list, modify, start_date: datetime, end_date: datetime):
    d = get_mod(modify)
    time_format = "%Y-%m-%d %H:%M:%S"
    x_mod = list()
    y_mod = list()
    main_chart = list()
    count = 0
    summ = 0
    summ_y = 0
    if modify == "none":
        for i in range(len(date)):
            if start_date <= datetime.strptime(date[i], time_format) < end_date:
                x_mod.append(xarg[i])
                y_mod.append(yarg[i])
        x_mod.append("END")
        main_chart.append(x_mod)
        main_chart.append(y_mod)
        return main_chart
    else:
        for i in range(len(xarg)):
            if start_date <= datetime.strptime(date[i], time_format) < end_date:
                if datetime.strptime(date[i], time_format) - start_date > d:
                    start_date = datetime.strptime(date[i], time_format)
                    if summ == 0:
                        x_mod.append(xarg[i])
                    else:
                        x_mod.append(summ/count)
                    if summ_y == 0:
                        y_mod.append(yarg[i])
                    else:
                        y_mod.append(summ_y/count)
                    count = 0
                    summ_y = 0
                    summ = 0
                else:
                    count += 1
                    try:
                        summ += float(xarg[i])
                    except:
                        summ = 0
                    try:
                        summ_y += float(yarg[i])
                    except:
                        summ_y = 0
        x_mod.append("END")
        main_chart.append(x_mod)
        main_chart.append(y_mod)
        return main_chart


def max_min_x(xarg: list, yarg: list, date: list, start_date: datetime, end_date: datetime):
    d = timedelta(days=1)
    time_format = "%Y-%m-%d %H:%M:%S"
    x_mod = list()
    y_mod1 = list()
    y_mod2 = list()
    main_chart = list()
    maxim = float("-inf")
    minim = float("inf")
    start_date = datetime.strptime(date[0], time_format)
    for i in range(len(xarg)):
        if start_date <= datetime.strptime(date[i], time_format) < end_date:
            if datetime.strptime(date[i], time_format) - start_date > d:
                start_date = datetime.strptime(date[i], time_format)
                x_mod.append(xarg[i])
                y_mod1.append(maxim)
                y_mod2.append(minim)
                maxim = float("-inf")
                minim = float("inf")
            else:
                maxim = max(maxim, float(yarg[i]))
                minim = min(minim, float(yarg[i]))

    x_mod.append("END")
    y_mod1.append("END")
    main_chart.append(x_mod)
    main_chart.append(y_mod1)
    main_chart.append(y_mod2)
    return main_chart


def get_temp_hum_name(data, uname):
    hum = "0"
    temp = "0"
    for key, value in data.items():
        if f'{value["uName"]}({value["serial"]})' == uname:
            for keys in value["data"]:
                if keys.split("_")[1] == "temp":
                    temp = keys
                if keys.split("_")[1] == "humidity":
                    hum = keys
                if hum != "0" and temp != "0":
                    break
            break
    return temp, hum


class CSVConverter:
    def __init__(self):
        self.data = {}

    def load_csv(self, filename):
        i = 0
        with open(filename, 'r', encoding="cp1251") as file:
            line = file.readline()
            pribor, serial = line.split(";")[1].split(" (")
            serial = serial.replace(")", "")
            print(serial, pribor)
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                keyys_json = [x for x in row.keys()]
                break
            for row in reader:
                b = {keyys_json[0]: row[keyys_json[0]], "uName": pribor, "serial" : serial}
                c = dict()
                for j in range(1, len(keyys_json)):
                    c[keyys_json[j]] = row[keyys_json[j]]
                b["data"] = c
                self.data[i] = b
                i += 1

    def get_json_data(self):
        return json.dumps(self.data)