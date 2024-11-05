class Post:
    def __init__(self, postId, userId, postText, hasImages, dateAndTime, replyId, repostId):
        self.postId = postId
        self.userId = userId
        self.postText = postText
        self.hasImages = hasImages
        self.replyId = replyId
        self.dateAndTime = dateAndTime
        self.repostId = repostId
