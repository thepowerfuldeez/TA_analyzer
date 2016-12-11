google.charts.load('current', {'packages':['corechart']});

function loadAnalytics() {
    var par = linkinput.value.split("/");
    var id = par[par.length - 1];
    $.ajax({url: "analytics?id="+id, success: function(result){
        document.getElementById("information").className = "container";
        document.getElementById("loader").className = "sk-cube-grid hidden";
        renderAnalytics(JSON.parse(result));
    }});
    document.getElementById("loader").className = "sk-cube-grid visible";     
}

function renderAnalytics(data){
    document.getElementById('image').innerHTML ="<img class = 'rounded' src='" + data['response'][0]['photo_100']+ "' />";
    document.getElementById('name_of_public').innerHTML="<h3>" + data['response'][0]['name'] + "</h3>";

    var sexData = [
     ['Пол', '%'],
     ['Женщины', data['sexes']['women']],
     ['Мужчины', data['sexes']['men']],
     ['Не указано', data['sexes']['undefined']]
    ];
    drawSexChart(sexData, "m_and_m")
}

document.getElementById("linkinput")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode == 13) {
        document.getElementById("go").click();
    }
});

function drawSexChart(data, elementId) {
    var data_to_show = google.visualization.arrayToDataTable(data);
    var options = {
      title: "Соотношение полов",
    };
    var chart = new google.visualization.PieChart(document.getElementById(elementId));
    chart.draw(data_to_show, options);
}