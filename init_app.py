import os

from database import init_db
import shutil
from pathlib import Path

if Path("./db/GreenGround.db").is_file() == False:
    shutil.copy('./init-static/img/', './static/img/')
    os.mkdir('./static/img/post-img/')

    print("Please enter the app's bcrypt key")
    key = input()
    file = open('key', 'w')
    file.write(key)
    file.close()

    print("You need to create a moderator account before initializing the databse REMEMBER THE USERNAME AND PASSWORD")
    print("Username:")
    userName = input()
    print("Display Name:")
    displayName = input()
    print("Password:")
    password = input()

    init_db(userName, displayName, password)

