
function getLikes(postId){
    $.ajax({
        url: (`${config.host}/post/like/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null") {
                for (const element of document.getElementsByClassName(`like-count-${postId}`)){
                    element.innerHTML = response.length
                }
            }},
        error: function(error) {
            console.log(error);
        }
    });
}

function likePost(postId){
    $.ajax({
        url: (`${config.host}/post/like/${postId}/`),
        type: 'POST',
        contentType: 'application/json',
        success: function(response) {
            if (response !== "null") {
                for (const element of document.getElementsByClassName(`like-button-${postId}`)) {
                    element.innerHTML = response
                }
                getLikes(postId)
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}

function unlikePost(postId){
    $.ajax({
        url: (`${config.host}/post/like/${postId}/`),
        type: 'DELETE',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null"){
                for (const element of document.getElementsByClassName(`like-button-${postId}`)){
                    element.innerHTML = response
                }
                getLikes(postId)
            }
            },
        error: function(error) {
            console.log(error);
        }
    });
}

function getReposts(postId) {
    $.ajax({
        url: (`${config.host}/post/repost/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null") {
                this.reposts = response.length
                for (const element of document.getElementsByClassName(`repost-count-${postId}`)){
                    element.innerHTML = response.length
                }
            }},
        error: function (error) {
            console.log(error);
        }
    });
}

function repostPost(postId){
    $.ajax({
        url: (`${config.host}/post/repost/${postId}/`),
        type: 'POST',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null") {
                for (const element of document.getElementsByClassName(`repost-button-${postId}`)) {
                    element.innerHTML = response
                }
                getReposts(postId)
            }
        },
        error: function (error) {
            console.log(error);
        }
    });
}

function unrepostPost(postId){
    $.ajax({
        url: (`${config.host}/post/repost/${postId}/`),
        type: 'DELETE',
        contentType: 'application/json',
        success: function (response) {
            if (response !== "null"){
                for (const element of document.getElementsByClassName(`repost-button-${postId}`)) {
                    element.innerHTML = response
                }
                getReposts(postId)
            }},
        error: function (error) {
            console.log(error);
        }
    });
}


