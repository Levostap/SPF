from datetime import datetime

from flask import Flask, render_template, request
import json
import dataWorker as dw

app = Flask(__name__, template_folder='template')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html", )


@app.route('/success_json', methods=['POST'])
def success_json():
    if request.method == 'POST':
        f = request.files['get_json_file']
        f.save("Data Files/" + "days.txt")
        return render_template("success.html")


@app.route('/success_csv', methods=['POST'])
def success_csv():
    if request.method == 'POST':
        f = request.files['get_csv_file']
        f.save("Data Files/" + "csv.txt")
        csvcon = dw.CSVConverter()
        csvcon.load_csv("Data Files/csv.txt")
        with open("Data Files/days.txt", "w") as file:
            file.write(csvcon.get_json_data())
        return render_template("success.html")


@app.route('/work', methods=['GET', 'POST'])
def work():
    file_name = 'Data Files/days.txt'
    devices = set()
    with open(file_name, 'r', encoding='utf-8') as file_json:
        data = json.load(file_json)
        for key, value in data.items():
            devices.add(f'{value["uName"]}({value["serial"]})')
    els = list(data.items())
    devices = sorted(devices)
    return render_template("work.html", unames=devices, start_date=els[0][1]["Date"], end_date=els[-1][1]["Date"])


@app.route('/get_params', methods=['GET'])
def params():
    arg = request.args.get('uname')
    print(arg)
    file_name = 'Data Files/days.txt'
    with open(file_name, 'r', encoding='utf-8') as file_json:
        data = json.load(file_json)
        for key, value in data.items():
            if f'{value["uName"]}({value["serial"]})' == arg:
                devices_parameters = list(value["data"])
                return json.dumps(devices_parameters)
    return "error"


@app.route('/get_chart_data', methods=['GET'])
def getChartData():
    namearg = request.args.get('uname')
    xarg = request.args.get('chartX')
    yarg = request.args.get('chartY')
    modify_selector = request.args.get('modify')
    start_time = request.args.get('start_date')
    end_time = request.args.get('end_date')
    file_name = 'Data Files/days.txt'
    x_chart = list()
    y_chart = list()
    datet = list()

    with open(file_name, 'r', encoding='utf-8') as file_json:
        data = json.load(file_json)
        if yarg == "ЭТ":
            temp, hum = dw.get_temp_hum_name(data, namearg)
        for key, value in data.items():
            if f'{value["uName"]}({value["serial"]})' == namearg:
                if xarg == "Date":
                    x_chart.append(value[xarg])
                else:
                    x_chart.append(value["data"][xarg])
                datet.append(value["Date"])
                if yarg == "ЭТ":
                    y_chart.append(float(value["data"][temp])-0.4*(float(value["data"][temp])-10)*(1-float(value["data"][hum])/100))
                else:
                    y_chart.append(value["data"][str(yarg)])
        if modify_selector == 'maxmin':
            main_chart = dw.max_min_x(x_chart, y_chart, datet,
                                      datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"),
                                      datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
        else:
            main_chart = dw.middle_x_all(x_chart, y_chart, datet, modify_selector,
                                         datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"),
                                         datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"))
    return json.dumps(main_chart)


if __name__ == '__main__':
    app.run()
