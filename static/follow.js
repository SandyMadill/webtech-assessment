function init(id){
    $.ajax({
                url: ('http://127.0.0.1:5000/follow/button/'+id),
                type: 'GET',
                contentType: 'application/json',
                success: function(response) {

                                document.getElementById("button").innerHTML = response
                },
                error: function(error) {
                    console.log(error);
                }
            });
}

function follow(id){
        $.ajax({
                url: ('http://127.0.0.1:5000/follow/follow-user/'+id),
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                    console.log("AAAAAAAAAAAAAAAAAAAAAAA")
                    document.getElementById("button").innerHTML = response
                },
                error: function(error) {
                    console.log(error);
                }
            });
}

function unfollow(id){
        $.ajax({
                url: ('http://127.0.0.1:5000/follow/unfollow-user/'+id),
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                    console.log("AAAAAAAAAAAAAAAAAAAAAAA")
                    document.getElementById("button").innerHTML = response
                },
                error: function(error) {
                    console.log(error);
                }
            });
}