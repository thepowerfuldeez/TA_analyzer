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

     document.getElementById('ins').innerHTML="<h4>" + data['university'] + "</h4>";
      document.getElementById('school').innerHTML="<h4>" + data['school'] + "</h4>";
       document.getElementById('city').innerHTML="<h4>" + data['city'] + "</h4>";
        document.getElementById('country').innerHTML="<h4>" + data['country'] + "</h4>";

    var sexData = [
        ['Пол', '%'],
        ['Женщины', data['sexes']['women']],
        ['Мужчины', data['sexes']['men']],
        ['Не указано', data['sexes']['undefined']]
];
var picData = [
        ['Картинки', '%'],
        ['Картинки', data['content']['photo']]
];
var textData = [
        ['Картинки', '%'],
        ['Картики', data['content']['text']]
];
var musicData = [
        ['Картинки', '%'],
        ['Картики', data['content']['music']]
];
    
    drawSexChart(sexData, 'm_and_m');
    drawPicChart(picData, 'pictures');
    drawTextChart(textData, 'text');
    drawMusicChart(musicData, 'music');
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
      title: "Соотношение полов"
  };

    var chart = new google.visualization.PieChart(document.getElementById(elementId));
    chart.draw(data_to_show, options);
}
function drawPicChart(data, elementId) {
    var data_to_show = google.visualization.arrayToDataTable(data);
    var options = {
      title: "Картинки в постах"
  };

    var chart = new google.visualization.PieChart(document.getElementById(elementId));
    chart.draw(data_to_show, options);
}

function drawTextChart(data, elementId) {
    var data_to_show = google.visualization.arrayToDataTable(data);
    var options = {
      title: "Текст в постах"
  };

    var chart = new google.visualization.PieChart(document.getElementById(elementId));
    chart.draw(data_to_show, options);
}

function drawMusicChart(data, elementId) {
    var data_to_show = google.visualization.arrayToDataTable(data);
    var options = {
      title: "Музыка в постах"
  };

    var chart = new google.visualization.PieChart(document.getElementById(elementId));
    chart.draw(data_to_show, options);
}

