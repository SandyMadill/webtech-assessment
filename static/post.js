let userId;
let postId;
let likes;
let reposts;

function  initPost(uId, pId){
    userId = uId
    postId = pId
    $.ajax({
                url: (`http://127.0.0.1:5000/follow/button/${userId}/`),
                type: 'GET',
                contentType: 'application/json',
                success: function(response) {
                    if (response !=="null"){
                        document.getElementById("follow-button").innerHTML = response
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
    getLikes()
    getReposts()
}

function getLikes(){

    $.ajax({
        url: (`http://127.0.0.1:5000/post/like/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null") {
                likes = response.length
                document.getElementById("like-count").innerHTML = likes
            }
        },
        error: function(error) {
            console.log(error);
        }
    });

    $.ajax({
        url: (`http://127.0.0.1:5000/post/like/button/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null"){
                document.getElementById("like-button").innerHTML = response
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}

function likePost(){
    $.ajax({
        url: (`http://127.0.0.1:5000/post/like/${postId}/`),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null"){
                document.getElementById("like-button").innerHTML = response
                getLikes()
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}

function unlikePost(){
    $.ajax({
        url: (`http://127.0.0.1:5000/post/like/${postId}/`),
        type: 'DELETE',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null"){
                document.getElementById("like-button").innerHTML = response
                getLikes()
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}

function getReposts() {
    $.ajax({
        url: (`http://127.0.0.1:5000/post/repost/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null") {
                reposts = response.length
                document.getElementById("repost-count").innerHTML = reposts
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
    $.ajax({
        url: (`http://127.0.0.1:5000/post/repost/button/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null"){
                document.getElementById("repost-button").innerHTML = response
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function repostPost(){
    $.ajax({
        url: (`http://127.0.0.1:5000/post/repost/${postId}/`),
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null"){
                document.getElementById("repost-button").innerHTML = response
                getReposts()
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function unrepostPost(){
    $.ajax({
        url: (`http://127.0.0.1:5000/post/repost/${postId}/`),
        type: 'DELETE',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null"){
                document.getElementById("repost-button").innerHTML = response
                getReposts()
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}