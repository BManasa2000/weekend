var script = document.createElement('script');
script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js';
script.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(script);

$(function(){
    $('button').click(function(){
        var checked = document.querySelectorAll("input[type=checkbox]:checked");
        var genres = [];
        for (var i = 0; i < checked.length; i++) {
            genres.push(checked[i].value);
        }
        // var user = $('#inputUsername').val();
        // var pass = $('#inputPassword').val();
        var json_genres = JSON.stringify(genres);
        $.ajax({
            url: '/filterBooks',
            type: 'POST',
            contentType: 'application/json',
            dataType : 'json',
            data : json_genres,
            success: function(data){
                // data.forEach(function(book) => {
                //     $('#tex').innerHTML = book.title;
                // })
                var len = 0;
                for (book in data)
                {
                    len++;
                }
                alert("WORKING!!!")
                // alert(data);
                var html = '';
                html += '<table id = "book_list" class="table table-striped">';
                html += '<th>Book ID</th>';
                html += '<th>Title</th>';
                html += '<th>Author</th>';
                html += '<th>Genre</th>';
                html += '<th>Tier</th>';
                html += '<th>Read</th>';

                for (var i = 0; i < len; i++) 
                {
                    html += '<tr>'
                    html += '<td>' + data[i][0] + '</td>';
                    html += '<td>' + data[i][1] + '</td>';
                    html += '<td>' + data[i][2] + '</td>';
                    html += '<td>' + data[i][3] + '</td>';
                    html += '<td>' + data[i][4] + '</td>';
                    html += '<td>' + "r" + '</td>';
                    html += '</tr>';
                }
                html += '</table>';
                document.getElementById('div_books').innerHTML = html;
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});

/*function filter_gen()
{
    var checked = document.querySelectorAll("input[type=checkbox]:checked");
    var genres = [];
    for (var i = 0; i < checked.length; i++) {
        genres.push(checked[i].value);
    }
    document.getElementById('tex').innerHTML = genres[0];
    alert(genres);
};*/

// for changing the shelf
function showShelf(shelfName) {
  var i;
  var x = document.getElementsByClassName("shelf");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  document.getElementById(shelfName).style.display = "block";
}