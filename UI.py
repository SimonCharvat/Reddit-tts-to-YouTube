from email.policy import default
from glob import glob
import tkinter as tk


from numpy import var
import main_create_video
import main_upload_video
from threading import Thread
import log
import pandas
import os



root = tk.Tk()

thread_create_video = Thread()
thread_upload_video = Thread()


subreddits_df = pandas.read_csv("./texts/0_subreddit_list.csv", sep=";")
subreddits_options = subreddits_df["name"].to_list()

subreddit_chosen_full_create = tk.StringVar(value="Select subreddit")
subreddit_chosen_full_upload = tk.StringVar(value="Select subreddit")

def create_video():
    global thread_create_video
    
    if subreddit_chosen_full_create.get() == "Select subreddit":
        log.add("No subreddit selected!")
        return

    subreddit_chosen_string = subreddits_df["string"].to_list()[subreddits_options.index(subreddit_chosen_full_create.get())]
    
    thread_create_video = Thread(target=main_create_video.start, args=[subreddit_chosen_string])
    thread_create_video.start()
    btn_create_video.config(state="disabled")
    drop_create_video.config(state="disabled")
    checkbtn_clear_temp.config(state="disabled")
    checkbtn_clear_log.config(state="disabled")
    root.after(1000, create_video_loop)
    

def change(root):
    pass
    #headline.config(text="TEST")

def create_video_loop():
    global thread_create_video
    if thread_create_video.is_alive():
        root.after(500, create_video_loop)
    else:
        log.add("Thread creating new video finished!")
        btn_create_video.config(state="normal")
        drop_create_video.config(state="normal")
        checkbtn_clear_temp.config(state="normal")
        checkbtn_clear_log.config(state="normal")
        clear_temp_files()
        update_upload_video_dropdown()
    



tk.Label(root, text="Create video:", fg="blue").pack()
tk.Label(root, text="Downloads new posts from reddit").pack()
tk.Label(root, text="if not already downloaded").pack()
tk.Label(root, text="Converts to text-to-speach").pack()
tk.Label(root, text="Creates images (subtitles)").pack()
tk.Label(root, text="Merges everything into a video").pack()
tk.Label(root, text="").pack()

drop_create_video = tk.OptionMenu(root, subreddit_chosen_full_create, *subreddits_options)
drop_create_video.pack()


btn_create_video = tk.Button(root, text="Create video", command=create_video)
btn_create_video.pack()



clear_temp_bool = tk.IntVar()
clear_log_bool = tk.IntVar()
clear_temp_bool.set(1)

checkbtn_clear_temp = tk.Checkbutton(root, text="Remove TEMP files after completion", variable=clear_temp_bool)
checkbtn_clear_temp.pack()
checkbtn_clear_log = tk.Checkbutton(root, text="Remove LOG file after completion", variable=clear_log_bool)
checkbtn_clear_log.pack()



#####################################

subreddits_lists = []
subreddits_options_upload = []

def update_upload_video_dropdown():
    global subreddits_options_upload
    subreddits_options_upload = []

    global drop_upload_video
    global subreddit_chosen_full_upload
    
    df_videos = pandas.read_csv("./videos/0_videos_list.csv", sep=";")
    df_videos = df_videos[df_videos["uploaded"] == 0]

    subreddits_names = list(set(df_videos["subreddit"]))
    

    for subreddit in subreddits_names:
        global subreddits_lists
        
        sub_full_name = subreddits_df["name"].to_list()[subreddits_df["string"].to_list().index(subreddit)]
        
        df = df_videos[df_videos["subreddit"] == subreddit]
        sub_list = [subreddit, sub_full_name, len(df), df.index[0]] # subreddit string | subreddit full name | number of unuploaded videos | index of first video | text string
        sub_list.append(f"{sub_full_name} | {len(df)} videos ready")
        subreddits_options_upload.append(f"{sub_full_name}   |   {len(df)} videos ready")

        subreddits_lists.append(sub_list)

    if "drop_upload_video" in globals():
        menu = drop_upload_video["menu"]
        menu.delete(0, "end")
        for string in subreddits_options_upload:
            menu.add_command(label=string, 
                                command=lambda value=string: subreddit_chosen_full_upload.set(value))
        subreddit_chosen_full_upload.set("Select subreddit")

update_upload_video_dropdown()

def upload_video():
    global thread_upload_video

    list_index = subreddits_options_upload.index(subreddit_chosen_full_upload.get())
    row_index = subreddits_lists[list_index][3]
    print(subreddits_lists[list_index])


    print(pandas.read_csv("./videos/0_videos_list.csv", sep=";"))
    print(row_index)
    print()
    
    thread_upload_video = Thread(target=main_upload_video.start, args=[row_index])
    thread_upload_video.start()
    btn_upload_video.config(state="disabled")
    drop_upload_video.config(state="disabled")
    root.after(1000, upload_video_loop)

def upload_video_loop():
    global thread_upload_video
    if thread_upload_video.is_alive():
        root.after(500, upload_video_loop)
    else:
        log.add("Thread uploading new video finished!")
        btn_upload_video.config(state="normal")
        drop_upload_video.config(state="normal")
        update_upload_video_dropdown()


def clear_temp_files(clear_all = False):
    try:
        dir = "./TEMP"
        
        global clear_temp_bool
        global clear_log_bool

        if clear_all or clear_temp_bool.get():
            for file in os.listdir(dir):
                if file == "log.txt":
                    continue
                os.remove(os.path.join(dir, file))
        
        if clear_all or clear_log_bool.get():
            os.remove("./TEMP/log.txt")
    except Exception as e:
        print("\n--- ERROR ---")
        print("Unable to remove TEMP files")
        print(e)



tk.Label(root, text="").pack()
tk.Label(root, text="").pack()
tk.Label(root, text="Upload created video", fg="blue").pack()


drop_upload_video = tk.OptionMenu(root, subreddit_chosen_full_upload, *subreddits_options_upload)
drop_upload_video.pack()

btn_upload_video = tk.Button(root, text="Upload video", command=upload_video)
btn_upload_video.pack()


tk.Label(root, text="").pack()
tk.Label(root, text="").pack()
tk.Label(root, text="Other:", fg="blue").pack()


btn_clear_temp = tk.Button(root, text="Remove TEMP and LOG files", command = lambda: clear_temp_files(clear_all=True))
btn_clear_temp.pack()

tk.Label(root, text="").pack()


def loop():
    
    root.after(1000, loop)

root.after(1000, loop)

root.mainloop()

#reddit_api()
#main_create_video.start_1()

#text_to_speech.tts_to_file("Hello world", "./TEMP/test_3.mp3")

#p = Thread(target=tts_to_file, args=("Hello world", "./TEMP/test_2.mp3"))
#p.start()
#p.join()




"""

class App(tk.Tk):
    def __init__(self):
        
        super().__init__()
        
        self.title("Title of the app here")
        
        self.headline = tk.Label(self, text="Hello").pack()
        btn_reddit = tk.Button(self, text="Download Reddit", command = lambda: self.change(self)).pack()

    
    def reddit_api(self):
        p = Thread(target=main_create_video.start_1, args=(self))
        p.start()
        p.join()

    def change(self):
        self.headline.config(text="TEST")





app = App()
app.mainloop()"""