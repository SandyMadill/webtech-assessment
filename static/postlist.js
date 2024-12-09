let lastDate
let loading = true
let stopLoading = false
let where

//  initialize the page when loaded by the index.html
//  the post paremter holds the posts in a 2d array with it's id as the first item and the post's rendered template as the second item
//  ld holds the date of the last item recieved in this batch of posts
//  args holds the arguments made in the postlist request
function initPostList(posts, ld, args){
    where = args
    lastDate = ld
    insertPosts(posts)
    observer.observe(document.querySelector(".end"))
}

//  This function will display every post recieved in the parameter onto the postlist page
//  the post paremter holds the posts in a 2d array with it's id as the first item and the post's rendered template as the second item
//  additionally each post displayed will have and event listener for when if clicked will redirect the user to that post unless another link or button is being clicked (username, follow button etc)
function insertPosts(posts){
    // for loop for every post received in the params
    for (i=0;i<posts.length;i++){
        //  create the element that will hold this post
        post = document.createElement("div")
        post.setAttribute("class", "post-list-item")

        //  event listener for if the post is clicked with the post's id as a peramter
        post.addEventListener('click', postClicked, true)
        post.postId = posts[i][0];

        //  insert hte post template into the post list
        post.innerHTML = posts[i][1]
        document.getElementById("post-list").appendChild(post)
        loading=false
    }
}



//  if the user scrolls to the bottom page this cross intersection will request to load another batch of posts
//  unless the last batch loaded has recieved less than 10 posts indicating that it was the last batch
let isVisible = null;

const container = document.querySelector(".core");

const options={
    root: container,
    threshold: 1,
    rootMargin: '20% 0% 20% 0%',
}

const callBack = (entries) => {
    isVisible = entries[0].isIntersecting;
};

 document.addEventListener("scroll", function(){
     if(isVisible && stopLoading === false && loading === false){
         loading = true
         $.ajax({
            url: (`${config.host}/post-list/${JSON.stringify(where)}/desc/${lastDate}/`),
            type: 'GET',
            contentType: 'application/json',
        success: function(response) {
            insertPosts(response[0])
            lastDate=response[1]
            if (response[0].length < 10){
                stopLoading = true
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
     }
 });

 function getAncestor(node, tagName) {
  if (!node || !tagName) return;
  while (node.parentNode) {
    node = node.parentNode;
    if (node.tagName && node.tagName.toLowerCase() == tagName) {
      return node;
    }
  }
  return null;
}

//  redirect the user to the post they clicked on if they arent clicking on another link or button within the post
 function postClicked(evt){
     // if the useer isn't clicking a button or link within the post
     if (evt.target.tagName!="A" && evt.target.tagName!="BUTTON"){
         // redirect the user to the post they clicked
         window.location.href = `${config.host}/post/${evt.currentTarget.postId}/`
     }
}

 const observer = new IntersectionObserver(callBack,options);