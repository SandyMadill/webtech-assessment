def getKey():
    file = open('key','r')
    key = file.readline()
    file.close()
    return key
