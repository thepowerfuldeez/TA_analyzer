google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);
function drawChart(data_list, title_of_chart, id) {
    var data_to_show = google.visualization.arrayToDataTable(data_list);
    var options = {
        title: title_of_chart,
    };
    var chart = new google.visualization.PieChart(document.getElementById(id));
    chart.draw(data_to_show, options);
}
