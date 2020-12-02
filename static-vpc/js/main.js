$(function () {
    $('#search_form').on('submit', function (e)  {
        e.preventDefault();  //prevent form from submitting
        console.log("Search button clicked");
        query = $('#note-textarea').val();
        console.log("Search query from text box:", query);
        send_request(query)
    });
});



// API Gateway SDK
var apigClient = apigClientFactory.newClient();

URL = window.URL || window.webkitURL;

// AJAX - GET request
function send_request(query) {
    $.ajax({
        method: 'GET',
        // headers: {'Access-Control-Allow-Origin': '*'},
        url: 'https://cors-anywhere.herokuapp.com/https://5q6du9z86k.execute-api.us-east-1.amazonaws.com/api/search?q=' + query,
        success: function (res) {
            console.log(res);
            body = res["body"];
            console.log(body);
            if (typeof body === 'string'){
                $('#results').html(body).css("color", "red");
            }
            else {
                $.ajax({
                    method: 'PUT',
                    data: JSON.stringify(body),
                    contentType: 'application/json',
                    dataType: 'json',
                    url: 'https://cors-anywhere.herokuapp.com/https://5q6du9z86k.execute-api.us-east-1.amazonaws.com/api/es',
                    success: function (res) {
                        console.log(res);
                        body = res["body"]
                        console.log(body);
                        if (typeof body === 'string'){
                            $('#results').html(body).css("color", "red");
                        }
                        else{
                            $('#results').html("");
                            $.each(body, function (index, value) {
                                console.log("i:" + index + " val:" + value);
                                $('#results').prepend($('<img>',{id:'theImg'+index,src:value,style:'width:500px;margin-bottom:15px'}))
                            });
                        }
                    }
                })
            }
        },
        error: function (err) {
            let message_obj = JSON.parse(err.responseText);
            let message = message_obj.message.content;
            $('#results').html('Error:' + message).css("color", "red");
            console.log(err);
        }
    });
}


// Upload Photos on photo album
$(document).ready(function () {
    $("#upload-btn").click(function () {
        // var fd = new FormData();
        var files = $('#file_path')[0].files[0];
        // fd.append('file',files);
        // console.log(fd)
        console.log(files)
        console.log(files.type)
        console.log(files.name)
        let config = {
            headers: { 'Content-Type': files.type }
        };
        url = 'https://cors-anywhere.herokuapp.com/https://5q6du9z86k.execute-api.us-east-1.amazonaws.com/api/upload/photo-album-demo/' + files.name
        axios.put(url, files, config).then(response => {
            console.log(response)
            alert("Photo uploaded successfully!");
        })
    });
});