function follow(userId){
    $.ajax({
        url: (`/follow/${userId}/`),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response !== "null"){
                for (const element of document.getElementsByClassName(`follow-button-${userId}`)){
                    element.innerHTML = response
                }
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}
function unfollow(userId){
    $.ajax({
        url: (`/follow/${userId}/`),
        type: 'DELETE',
        contentType: 'application/json',
        success: function(response) {
            if (response !== "null"){
                for (const element of document.getElementsByClassName(`follow-button-${userId}`)){
                    element.innerHTML = response
                }
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}
