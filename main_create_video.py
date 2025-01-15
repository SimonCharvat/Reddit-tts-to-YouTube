

#max_line_len_glob = 63 # maximum string length per line
#max_line_count_glob = 21 # maximum lines per image/page




def start(subreddit):

    from asyncio.log import logger
    import pandas
    from reddit_request import reddit_request
    import text_to_image as ttimg
    import text_handler as txt
    import text_to_speech as tts
    import video_handler as vid
    import numpy
    import chapters
    from datetime import date
    import log

    number_of_posts_per_video = None # Default = None -> is automatically assigned by 0_subreddit_list.csv


    subreddit_full_name = ""
    subreddit_comments = ""

    for i, row in pandas.read_csv("./texts/0_subreddit_list.csv", sep=";").iterrows():
        if row["string"] == subreddit:
            subreddit_full_name = row["name"]
            subreddit_comments = row["comments"] # Boolean if comments should be included in final video
            if number_of_posts_per_video == None:
                number_of_posts_per_video = row["posts_per_video"]
            break


    if subreddit_full_name == "":
        log.add("ERROR: Subreddit not found in 0_subreddit_list.csv")
        raise ValueError("Subreddit not found in 0_subreddit_list.csv")

    # TODO get posts from API - finished? Probably working
    reddit_request(subreddit, number_of_posts_per_video)


    # File containing info about all videos
    df_videos = pandas.read_csv("./videos/0_videos_list.csv", sep=";")

    episode = numpy.array(df_videos["subreddit"]) == subreddit
    episode = episode.tolist()
    episode = sum(episode) + 1

    df_videos.loc[len(df_videos.index)] = [
        f"{subreddit}_{episode}.mp4", # video
        f"{subreddit}_{episode}.png", # thumbnail
        f"{subreddit}_{episode}.txt", # sufix
        f"{subreddit_full_name} #{episode} | Reddit Voiceover", # title
        subreddit, # subreddit
        episode, # episode
        1, # files_exist
        0, # uploaded
        date.today().strftime("%Y/%m/%d"), # date_created
        "-" # date_uploaded
    ]


    df_posts = pandas.read_csv(f"./texts/{subreddit}.csv", sep=";")


    meta_data = pandas.DataFrame(columns=["post_number", "index", "page_count"])

    used_posts = 1

    intro_text = f"Hello, welcome to new reddit voiceover update. Today we will take a look on subreddit: {subreddit_full_name}, Enjoy. \n \n "
    outro_text = f"Thank you for watching, if you liked the video, please, like and subscribe \n\nIf you want to see your favourite subreddit in next video, leave a comment"

    segment_lenghts_l = []

    log.add("Generating intro for whole video")
    ttimg.generate_post_intro("00", f"{subreddit_full_name} #{episode}", f"r/{subreddit}", f"www.reddit.com/r/{subreddit}") # Subreddit intro (for the whole video)
    segment_lenghts_l.append(tts.tts_to_file(f"{intro_text}", "./TEMP/00_intro_voice.mp3"))

    for index, row in df_posts.iterrows():
        if row["already_used"] == 1:
            continue
        
        log.add(f"Generating images and audio for post: {used_posts}/{number_of_posts_per_video}")

        
        text_pages = txt.wrap_long_text(row["text"], 63, 21) # gets nested list of lines
        
        
        #text_pages = [x for xs in text_pages for x in xs] # flatten list

        #text_pages = txt.flatten(text_pages, list)

        short_title = row["title"]
        if len(short_title) >= 100:
            short_title = short_title[0:100] + "..."
        
        ttimg.generate_post_intro(index, row["title"], row["author"], row["url"])
        seqment_lenght = tts.tts_to_file(f"{row['title']} \n \n \n \n", f"./TEMP/{index}_intro_voice.mp3")

        for i, page in enumerate(text_pages):
            seqment_lenght += tts.tts_to_file(page, f"./TEMP/{index}_{i}_voice.mp3", True)
            ttimg.generate_images(page, index, i, short_title, row["author"], row["url"])
            meta_data.loc[used_posts - 1] = [used_posts, index, i+1]

        segment_lenghts_l.append(seqment_lenght)

        
        df_posts.loc[index, "already_used"] = 1
        used_posts += 1

        if used_posts >= number_of_posts_per_video + 1:
            break


    log.add("Generating outro for whole video")
    ttimg.generate_post_outro("00", f"{outro_text}",) # Outro of the whole video
    segment_lenghts_l.append(tts.tts_to_file(f"{outro_text}", "./TEMP/00_outro_voice.mp3"))

    description_suffix = chapters.get_chapters_text(segment_lenghts_l)

    meta_data.to_csv(f"./TEMP/meta_data.csv", sep=";", index=False)
    df_posts.to_csv(f"./texts/{subreddit}.csv", sep=";", index=False)

    log.add("Audio and video clips generated")

    list_of_paths_videos = []
    files_count = sum(meta_data["page_count"].to_list()) - 2 + 1

    list_of_paths_videos.append( vid.image_to_video("00_intro") )
    files_count_processed = 0

    for inx, post_row in meta_data.iterrows():
        list_of_paths_videos.append( vid.image_to_video(str(post_row["index"]) + "_intro") )
        files_count_processed += 1

        for j in range(post_row["page_count"]):
            log.add(f"Generating videos from text and image: {files_count_processed}/{files_count}")
            list_of_paths_videos.append( vid.image_to_video(str(post_row["index"]) + "_" + str(j)))
            files_count_processed += 1

    list_of_paths_videos.append( vid.image_to_video("00_outro") )

    ttimg.resize_image((1280, 720), "./TEMP/00_intro_image.png", f"./videos/{subreddit}_{episode}.png")

    with open(f"./videos/{subreddit}_{episode}.txt", "w") as f:
        f.write(description_suffix)

    vid.merge_videos(list_of_paths_videos, f"./videos/{subreddit}_{episode}.mp4")

    df_posts.to_csv(f"./texts/{subreddit}.csv", sep=";", index=False)

    df_videos.to_csv("./videos/0_videos_list.csv", sep=";", index=False)

    log.add("Video finished")

