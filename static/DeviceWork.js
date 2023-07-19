
function DeviceCount(count, uname)
{
    var list = document.getElementsByName("DevicesName");
    for(let i = 0; i < count; i++){
        list[0].appendChild(new Option(uname[i], uname[i]));
    }
}

function checkParams(){
    $.ajax({
        type: "GET",
        url: "/get_params?uname=" + document.getElementById("DevicesName").selectedOptions[0].value,
        success: function(response){
            let str_json = JSON.parse(response);
            let str = new String(str_json);
            if(str == "error"){
                alert("Ошибка в файле.");
            }
            else{
                var x = document.getElementById("DeviceOptionsX");
                var y = document.getElementById("DeviceOptionsY");
                x.replaceChildren();
                y.replaceChildren();
                x.appendChild(new Option("Date", "Date"));
                const response_arr = str.split(',');
                alert(response_arr)
                console.log("Data succesfully loaded.");
                x.size = y.size = response_arr.length/2;
                let is_temp = 0;
                let is_hum = 0;
                for(let o = 0; o < response_arr.length; o++){
                    if(response_arr[o].includes("temp")){
                        is_temp = 1;
                    }
                    if(response_arr[o].includes("humidity")){
                        is_hum = 1;
                    }
                    x.appendChild(new Option(response_arr[o], response_arr[o]));
                    y.appendChild(new Option(response_arr[o], response_arr[o]));
                }
                if(is_hum == 1 && is_temp == 1){
                    y.appendChild(new Option("ЭТ", "ЭТ"));
                }
            }
        },
        error: function(error){
            alert("Ошибка.\n" + error);
        }

    });
}

function data_is_correct(){
    var date1 = new Date(document.getElementById("start_date").value.split("T")[0]);
    var date2 = new Date(document.getElementById("end_date").value.split("T")[0]);
    var time1 = document.getElementById("start_date").value.split("T")[1];
    var time2 = document.getElementById("end_date").value.split("T")[1];
    if((time1 > time2 && date1 > date2) || date1 > date2 || (date1 == date2 && time1>time2)){
        document.getElementById("end_date").value = null;
    }

}

function CreateButton(){
    var clear = document.getElementById("ClearButton");
    if(clear.disabled == true){
        clear.disabled = false; 
    }
    document.getElementById("CreateButton").disabled = true;
    modify = getMod();
    var end_time;
    var start_time;
    if (document.getElementById("start_date").value == '' || document.getElementById("end_date").value == ''){
        end_time = document.getElementById("end_date").max.replace("T"," ");
        start_time = document.getElementById("start_date").min.replace("T"," ");
    }else{
        start_time = document.getElementById("start_date").value.replace("T", " ")+":00";
        end_time = document.getElementById("end_date").value.replace("T", " ") + ":00";
    }
    $.ajax({
        type: "GET",
        url: "/get_chart_data?uname="+document.getElementById("DevicesName").selectedOptions[0].value + "&chartX="
        + document.getElementById("DeviceOptionsX").selectedOptions[0].value + "&chartY=" + document.getElementById("DeviceOptionsY").selectedOptions[0].value
        + "&modify=" + modify + "&start_date=" + start_time + "&end_date=" + end_time,
        success: function(response){
            var resp_json = JSON.parse(response);
            var resp = new String(resp_json);
            var response_arr = resp.split(",END,");
            var chartX = [];
            var chartY = [];
            var chartY2 = [];
            if(modify!="maxmin"){
                chartX = response_arr[0].split(",");
                chartY = response_arr[1].split(",");
            }else{
                chartX = response_arr[0].split(",");
                chartY = response_arr[1].split(",");
                chartY2 = response_arr[2].split(",");
            }
            if(getChartType()=="scatter"){
                chartY.push(chartX);
            }
            let mChart = new Chart("myChart",{
                type:getChartType(),
                data:{
                    labels: chartX,
                    datasets:[{
                        data:chartY
                    },{
                        data:chartY2
                    }]
                },
                options: {
                    legend: {display: false},
                    title: {
                      display: true,
                      text: document.getElementById("DevicesName").selectedOptions[0].value + document.getElementById("DeviceOptionsX").selectedOptions[0].value + document.getElementById("DeviceOptionsY").selectedOptions[0].value,
                    }
                }
            });

        },
        error:function(error){
            alert("Ошибка");
        }
    })
}

function getChartType(){
    if(document.getElementById("line_chart").checked == true){
        return "line";
    } else if(document.getElementById("column_chart").checked == true){
        return "bar";
    }else{
        return "scatter";
    }
}

function getMod(){
    let modify = "none";
    if(document.getElementById("one_hour_radio").checked == true){
        modify = "hour";
    }else if(document.getElementById("three_hours_radio").checked == true){
        modify = "3hour";
    }else if(document.getElementById("day_radio").checked == true){
        modify = "day";
    }
    else if(document.getElementById("how_it_is_radio").checked == true){
        modify = "none";
    } else if(document.getElementById("max_min_radio").checked == true){
        modify = "maxmin";
    }
    return modify;
}

function ClearButton(){
    document.getElementById("ClearButton").disabled = true;
    document.getElementById("CreateButton").disabled = false;
    Chart.getChart("myChart").destroy();
}


function AddButton(){
    modify = getMod();
    var end_time;
    var start_time;
    if (document.getElementById("start_date").value == '' || document.getElementById("end_date").value == ''){
        end_time = document.getElementById("end_date").max.replace("T"," ");
        start_time = document.getElementById("start_date").min.replace("T"," ");
    }else{
        start_time = document.getElementById("start_date").value.replace("T", " ")+":00";
        end_time = document.getElementById("end_date").value.replace("T", " ") + ":00";
    }
    $.ajax({
        type: "GET",
        url: "/get_chart_data?uname="+document.getElementById("DevicesName").selectedOptions[0].value + "&chartX="
        + document.getElementById("DeviceOptionsX").selectedOptions[0].value + "&chartY=" + document.getElementById("DeviceOptionsY").selectedOptions[0].value
        + "&modify=" + modify + "&start_date=" + start_time + "&end_date=" + end_time,
        success: function(response){
            let resp_json = JSON.parse(response);
            let resp = String(resp_json);
            var response_arr = resp.split(",END,");
            var chartX = [];
            var chartY = [];
            var chartY2 = [];
            if(modify!="maxmin"){
                chartX = response_arr[0].split(",");
                chartY = response_arr[1].split(",");
            }else{
                chartX = response_arr[0].split(",");
                chartY = response_arr[1].split(",");
                chartY2 = response_arr[2].split(",");
            }
            if(getChartType()=="scatter"){
                chartY.push(chartX);
            }
            var chart = Chart.getChart("myChart");
            chart.data.datasets[chart.data.datasets.length] = {
                data: chartY,
            }
            chart.update();

        },
        error:function(error){
            alert("Ошибка");
        }
    })

}