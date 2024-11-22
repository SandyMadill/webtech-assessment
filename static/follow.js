function initFollow(id){
    $.ajax({
                url: (`http://127.0.0.1:5000/follow/button/${id}/`),
                type: 'GET',
                contentType: 'application/json',
                success: function(response) {

                                document.getElementById("follow-button").innerHTML = response
                },
                error: function(error) {
                    console.log(error);
                }
            });
}

function follow(id){
        $.ajax({
                url: (`http://127.0.0.1:5000/follow/${id}/`),
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                    if (response !== "null"){
                        document.getElementById("follow-button").innerHTML = response
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
}

function unfollow(id){
        $.ajax({
                url: (`http://127.0.0.1:5000/follow/${id}/`),
                type: 'DELETE',
                contentType: 'application/json',
                success: function(response) {
                    if (response !== "null"){
                        document.getElementById("follow-button").innerHTML = response
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
}