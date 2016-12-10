function loadAnalytics() {
    var par = linkinput.value.split("/");
    var id = par[par.length - 1];
    var xhr = new XMLHttpRequest();
        xhr.open('POST', '/analytics?id='+id, true);
        xhr.send();
        xhr.onreadystatechange = function() {
          if (xhr.readyState != 4) return;
          if (xhr.status == 200) {
            document.getElementById("information").className = "container";
            document.getElementById("loader").className = "sk-cube-grid hidden";
            // xhr.responseText - тут ответ
          }
        }
        document.getElementById("loader").className = "sk-cube-grid visible";
}
function get_page(){
              if(document.getElementById("link").value != ""){
                document.getElementById("loader").className = "sk-cube-grid visible";
                document.getElementById("information").className = "container hidden";
                document.getElementById("ours").className = "text-center hidden";
                url = document.getElementById("link").value;
                var par = url.split("/");
                var id = par[par.length - 1];
                document.getElementById("link").className= "form-control";
                
                var curl = "https://api.vk.com/method/groups.getById?group_id=" + id + "&fields=photo_100,description";

                    var pageRequest = new XMLHttpRequest(curl);
                    pageRequest.open("GET", curl, false);
                    pageRequest.send();
                    var pageSourceCode = pageRequest.response;
                     
                    pageSourceCode = JSON.parse(pageSourceCode);
                    //Changing values on page
                    document.getElementById('image').innerHTML ="<img class = 'rounded' src='" + pageSourceCode['response'][0]['photo_100']+ "' />";
                    document.getElementById('name_of_public').innerHTML="<h3>" + pageSourceCode['response'][0]['name'] + "</h3>";
                    document.getElementById('about').innerHTML= pageSourceCode['response'][0]['description'];
                    document.getElementById("loader").className = "sk-cube-grid hidden";
                    document.getElementById("ours").innerHTML = "Ваше сообщество";
                    document.getElementById("information").className = "container visible";
              }
              else{
                document.getElementById("link").placeholder = "Пожалуйста, введите имя паблика!";
                document.getElementById("link").className= "form-control grey_color";
                document.getElementById("loader").className = "sk-cube-grid hidden";
              }
}