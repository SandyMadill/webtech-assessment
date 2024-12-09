var newNotifications
var oldNotifications
//  displays the new notifications on the page
function initNotifications(oldNotif, newNotif){
    newNotifications = newNotif
    oldNotifications = oldNotif
    for (i in newNotif){
        document.getElementById("notifications").innerHTML+=newNotifications[i]
    }
    seenPosts()
}

//  if the notification is a follow then it will redirect the user to the users profile
//  otherwise it will redirect the user to the post
function notificationClicked(action, userId, postId){
    if (action === "follow"){
        window.location.href = `/profile/${userId}`
    }
    else{
        window.location.href = `/post/${postId}`
    }
}

function loadNew(){
    document.getElementById("notifications").innerHTML=""
    for (i in newNotifications){
        document.getElementById("notifications").innerHTML+=newNotifications[i]
    }
    document.getElementById("new-tab").setAttribute("selected", "true")
    document.getElementById("old-tab").setAttribute("selected", "false")
}

function loadOld(){
    document.getElementById("notifications").innerHTML=""
    for (i in oldNotifications){
        document.getElementById("notifications").innerHTML+=oldNotifications[i]
    }
    document.getElementById("old-tab").setAttribute("selected", "true")
    document.getElementById("new-tab").setAttribute("selected", "false")
}

function seenPosts(){
    $.ajax({
        url: (`/notifications/seen/`),
        type: 'PUT',
        contentType: 'application/json',
        error: function(error) {
            console.log(error);
        }
    });
}