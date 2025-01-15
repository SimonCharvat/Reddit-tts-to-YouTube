import pandas

import datetime
from os import path


print()



def add(string, priority = 1):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    string = f"{date} | {string}"

    print(string)

    

    with open("./TEMP/log.txt", "a") as file:
        file.write(f"\n{string}")