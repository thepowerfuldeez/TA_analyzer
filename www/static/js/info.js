function loadAnalytics() {
    var par = linkinput.value.split("/");
    var id = par[par.length - 1];
    $.ajax({url: "analytics?id="+id, success: function(result){
        document.getElementById("information").className = "container";
        document.getElementById("loader").className = "sk-cube-grid hidden";
        renderAnalytics(JSON.parse(result));
    }});
    document.getElementById("loader").className = "sk-cube-grid visible";
    var table = [
          ['Task', 'Hours per Day'],
          ['Work',     11],
          ['Eat',      2],
          ['Commute',  2],
          ['Watch TV', 2],
          ['Sleep',    7]
        ];
    var 
    drawChart(table, 'Hello!', 'piechart'); 
    drawChart()       
}

function renderAnalytics(data){
    document.getElementById('image').innerHTML ="<img class = 'rounded' src='" + data['response'][0]['photo_100']+ "' />";
    document.getElementById('name_of_public').innerHTML="<h3>" + data['response'][0]['name'] + "</h3>";
    document.getElementById('about').innerHTML= data['response'][0]['description'];
    document.getElementById("ours").innerHTML = "Ваше сообщество";
}
document.getElementById("linkinput")
    .addEventListener("keyup", function(event) {
    event.preventDefault();
    if (event.keyCode == 13) {
        document.getElementById("go").click();
    }
});