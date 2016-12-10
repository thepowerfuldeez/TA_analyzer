 function get_page(){
              var url = document.getElementById("link").value;
              var par = url.split("/");
              var id = par[par.length - 1];
              alert(id);
              url = "https://api.vk.com/method/groups.getById?group_id=" + id + "&fields=photo_100,description";
              var pageRequest = new XMLHttpRequest(url);
              pageRequest.open("GET", url, false);
              pageRequest.send();
              var pageSourceCode = pageRequest.response;
              pageSourceCode = JSON.parse(pageSourceCode);
              var elem = document.getElementById('image');
              var name = document.getElementById('name_of_public');
              var about = document.getElementById('about');
              elem.innerHTML ="<img class = 'rounded' src='" + pageSourceCode['response'][0]['photo_100']+ "' />";
              name_of_public.innerHTML="<h3>" + pageSourceCode['response'][0]['name'] + "</h3>";
              about.innerHTML= pageSourceCode['response'][0]['description'];
}