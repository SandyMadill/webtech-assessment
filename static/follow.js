function init(following){
	if(following = "true"){
		document.getElementById("follow").innerHTML
	}
}

function follow(id){
        $.ajax({
                url: ('http://127.0.0.1:5000/follow/'+id),
                type: 'POST',
                contentType: 'application/json',
                success: function(response) {
                                document.getElementById("follow").innerHTML = response
                },
                error: function(error) {
                    console.log(error);
                }
            });
}

