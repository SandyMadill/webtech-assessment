//  when a post's page is loaded
function initPage(postId, replyId){
    //  load replies
    getReplies(postId)

    //  if this post is part of a thread retrieve the posts that come before it in the thread and display them above the selected post
    if (replyId != undefined){
        getThread(replyId)
    }

}

//  retrieves the posts that come before the selected post in the thread
function getThread(postId){
    //  retrieve the posts in the thread before it
    //  and then display them on the page above the selected post
    $.ajax({
        url: (`/post/thread/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            console.log(response)
            for (i=0; i<response.length; i++){
                console.log(response[i][0])
                //  create the element that will hold this post
                post = document.createElement("div")
                post.setAttribute("class", "post-list-item")

                //  event listener for if the post is clicked with the post's id as a peramter
                post.addEventListener('click', postClicked, true)
                post.postId = response[i][0];

                //  insert hte post template into the thread
                post.innerHTML = response[i][1]
                document.getElementById("thread").appendChild(post)
            }
            },
        error: function(error) {
            console.log(error);
        }
    });

}


//  retrives all of the replies to the selected post and displays them in the reply section
function getReplies(postId){
    $.ajax({
        url: (`/replies/${postId}/`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            if (response !=="null") {
                lastDate = response[1]
                insertPosts(response[0])
            }},
        error: function(error) {
            console.log(error);
        }
    });
}

//  get's the count of likes that the selected post has recieved
function getLikes(postId){
    $.ajax({
        url: (`/post/like/${postId}/`),
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

//  sends a request for the logged in user to like the selected post
function likePost(postId){
    $.ajax({
        url: (`/post/like/${postId}/`),
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

//  sends a request to remove the like that the user has for this selected post
function unlikePost(postId){
    $.ajax({
        url: (`/post/like/${postId}/`),
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

// get's the count of likes that this selected post has recieved and then displays it on the selected post
function getReposts(postId) {
    $.ajax({
        url: (`/post/repost/${postId}/`),
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

//  sends a request for the logged in user to make a repost of this post
function repostPost(postId){
    $.ajax({
        url: (`/post/repost/${postId}/`),
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

//  sends a request to remove the repost of the selected post that this user has made
function unrepostPost(postId){
    $.ajax({
        url: (`/post/repost/${postId}/`),
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

//  when an instance of the create post form has been submitted instead of reloading the page it will instead carry out this function
$(document).on('submit','#create-post',function(e)
{
    //  this blocks the normal procedure for when a post is submitted (the page gets reloaded as a post request)
    e.preventDefault();
    $.ajax({
        type:'POST',
        url:'/create-post/',
        data:{
          text:$("#text").val(),
          replyId:$("#replyId").val()
        },
        success:function(response){

        }
      })

});


