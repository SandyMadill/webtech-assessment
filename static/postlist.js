let lastDate
function initPostList(posts, ld){

    lastDate = ld
    console.log(lastDate)
    insertPosts(posts)
    observer.observe(document.querySelector(".end"))

}

function insertPosts(posts){
    for (i=0;i<posts.length;i++){
        post = document.createElement("div")
        post.innerHTML = posts[i]
        document.getElementById("post-list").innerHTML+=posts[i]
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
     console.log(lastDate)
     if(isVisible){
         $.ajax({
        url: (`${config.host}/post-list/${lastDate}/desc`),
        type: 'GET',
        contentType: 'application/json',
        success: function(response) {
            print(response)
        },
        error: function(error) {
            console.log(error);
        }
    });
     }
 });

 const observer = new IntersectionObserver(callBack,options);