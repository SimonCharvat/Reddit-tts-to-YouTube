
#import moviepy
#from moviepy.editor import AudioFileClip, ImageClip, concatenate_videoclips, VideoFileClip
from moviepy import VideoFileClip, AudioFileClip, ImageClip, concatenate_videoclips

# Handles merging files from TEMP

""" def merge_files(meta_data):
    
 """


def image_to_video(filename, path = "./TEMP/"):
    audio = AudioFileClip(path + filename + "_voice.mp3")
    image = ImageClip(path + filename + "_image.png")

    #video = image.set_audio(audio)
    video = image.with_audio(audio) # updated for moviepy > 2.0

    video.duration = audio.duration
    video.fps = 1

    video.write_videofile(path + filename + "_video.mp4", logger=None)

    return path + filename + "_video.mp4"


def merge_videos(list_of_paths, save_path = "./TEMP/final.mp4", logger=None):
    print("Merging all videoclips...")
    video_list = []
    for path in list_of_paths:
        video_list.append(VideoFileClip(path))
    final_video = concatenate_videoclips(video_list)
    print("Videoclips merged - saving file...")
    final_video.write_videofile(save_path, logger=None)