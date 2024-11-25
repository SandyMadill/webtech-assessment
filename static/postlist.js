let lastDate
let loading = true
let stopLoading = false
function initPostList(posts, ld){

    lastDate = ld
    insertPosts(posts)
    observer.observe(document.querySelector(".end"))
}

function insertPosts(posts){
    for (i=0;i<posts.length;i++){
        post = document.createElement("div")
        post.innerHTML = posts[i]
        document.getElementById("post-list").innerHTML+=posts[i]
        loading=false
    }
}


let isVisible = null;

const container = document.querySelector(".container");

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
        url: (`${config.host}/post-list/${lastDate}/desc`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            initPostList(response[0])
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

 function loadPosts(){
     console.log(lastDate)
     if(isVisible && stopLoading === false){
         $.ajax({
        url: (`${config.host}/post-list/${lastDate}/desc`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            initPostList(response[0])
            lastDate=response[1]
            console.log(response[0].length)
            console.log(lastDate)
            if (response[0].length < 10){
                stopLoading = true
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
     }
 }

 const observer = new IntersectionObserver(callBack,options);