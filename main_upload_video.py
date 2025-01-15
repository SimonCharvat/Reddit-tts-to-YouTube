
def start(row_index):

    import os
    import pandas
    from datetime import date
    import youtube
    #import youtube_as_script
    import subprocess

    df_videos = pandas.read_csv("./videos/0_videos_list.csv", sep=";")

    title = ""

    row = df_videos.iloc[row_index]
    
    """for i, row in df_videos.iterrows():
    if row["uploaded"] == 1:
        continue
        print()"""

    file_location_abs = os.path.abspath(f"./videos/{row['video']}").replace("\\", "/")
    title = row["title"]
    description = f"""Few interesting posts from r/{row['subreddit']}--!-- --!--Video created on: {row['date_created']}--!--{open(f"./videos/{row['sufix']}", 'r').read()}"""
    print("Description 1:")
    print(description)
    description.replace("\n", "--!--")
    print("Description 2:")
    print(description)
    keywords = f"Reddit, stories, r/{row['subreddit']}, {row['subreddit']}"

    df_videos.loc[row_index, "date_uploaded"] = date.today().strftime("%Y/%m/%d")
    df_videos.loc[row_index, "uploaded"] = 1
    print(f"Uploading video:\n{row['title']}")
        
    #    break

    if title == "":
        raise ValueError("All videos have been already uploaded!")

    #Test noveho scriptu
    #youtube_as_script.start(file_location_abs, title, description, "24", "test1, test2", "public")

    #Posledni semi-funkcni.
    #os.system(f"""python youtube.py --file="{file_location_abs}" --title="{title}" --description="{description}" --keywords="{keywords}" --category="24" --privacyStatus="public" """)

    #Subprocess test:
    subprocess.call(fr"""python youtube.py --file="{file_location_abs}" --title="{title}" --description="{description}" --keywords="{keywords}" --category="24" --privacyStatus="public" """, shell=True)

    #os.system(f"""python youtube.py --file="D:/OneDrive - Vysoká škola ekonomická v Praze/0 Privat/Programming/Reddit video maker/videos/talesfromtechsupport_1" --title="{title}" --description="{description}" --keywords="{keywords}" --category="24" --privacyStatus="public" """)

    print("Uploading finished - saving metadata")

    df_videos.to_csv("./videos/0_videos_list.csv", sep=";", index=False)


    print("Finished")