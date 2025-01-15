
from math import ceil
import requests
import pandas
from time import sleep, time
from os.path import exists
import random
import numpy


def replace_text(original):
    new = original.replace("\"", "'")
    new = new.replace("$", "")
    new = new.replace("*", "")
    new = new.replace("&lt", "") # less than
    new = new.replace("&gt", "") # greater than
    new = new.replace("&#x200b", " ") # zero width space
    new = new.replace("&#x200B", " ") # zero width space
    new = new.replace("#x200B;", " ") # zero width space
    new = new.replace("#x200B", " ") # zero width space
    new = new.replace("&amp;", "") # &
    new = new.replace("&amp", "") # &

    return new



def authorise():
    import reddit_credentials as rc
    
    global headers
    auth = requests.auth.HTTPBasicAuth(rc.creds["public"], rc.creds["secret"])
    headers = {"User-Agent": "MyAPI/0.0.1"}
    request_token = requests.post("https://www.reddit.com/api/v1/access_token",
                        auth=auth,
                        data=rc.data,
                        headers=headers)

    token = request_token.json()["access_token"]
    headers["Authorization"] = f"bearer {token}"
    print("Reddit API authorised:")
    print(headers)



def reddit_request(subreddit_string, n_posts, required_listing = None, required_time_period = None):
    path = f"./texts/{subreddit_string}.csv"
    
    if exists(path):
        df = pandas.read_csv(path, sep=";")
        
        if required_listing != None:
            listings_bool = numpy.array(df["listing"]) == required_listing
            listings_bool.tolist()
            request_amount = n_posts - sum(listings_bool)
        else:
            request_amount = n_posts - (len(df["already_used"].to_list()) - sum(df["already_used"].to_list()))
    else:
        request_amount = n_posts

    if required_listing != None:
        listing = required_listing
    else:
        listing = random.choice(["controversial", "hot", "new", "rising", "top"])

    if required_time_period != None:
        time_period = required_time_period
    else:
        time_period = random.choice(["all", "year", "month", "week", "day"])

    saved_posts = 0

    if request_amount <= 0:
        print("Enouqh posts already saved in file - no requests to Reddit API")
        return

    saved_posts += reddit_API_get(subreddit_string, request_amount, listing, time_period)

    while saved_posts < request_amount:
        saved_posts += reddit_API_get(subreddit_string, ceil(request_amount / 3), listing, time_period)
        print("Randomizing API request")
        time_period = random.choice(["all", "year", "month", "week", "day"])
        listing = random.choice(["controversial", "hot", "rising", "top"])

    
    



def reddit_API_get(subreddit_string, n_posts, listing = "top", time_period = "all", n_comments = None, last_fullname = None):
    """
    Parameters
    ---------
    subreddit_string : str
        Name of subreddit. The string following r/ ....
    n_posts : float
        Number of posts to download
        Maximum of 100 posts is allowed by Reddit API rules
    listing : str
        By which metric to sort (choose) posts for download
        Default = "top"
        Examples: controversial, best, hot, new, random, rising, top 
    time_period : str
        Time constrains of requests
        Default = "all"
        Examples: all, year, month, week, day, hour
    n_comments : float
        Default = None
        Number of comments to download. Ignored if subreddit is focused on original post only (as set in .csv file)
    last_fullname : str
        Optional
        Default = None
        String of last known post full ID ("URL" string)
        Only used for optimalization or debugging
    
    Examples
    ---------
    reddit_request("talesfromtechsupport", 5, "top")
    
    Returns
    ---------
    Nothing to return
    """

    # TODO add option to read comments


    path = f"./texts/{subreddit_string}.csv"

    try:
        df = pandas.read_csv(path, sep=";")
    except:
        df = pandas.DataFrame(columns=["already_used", "listing", "time_period", "fullname", "author", "title", "length", "text", "url"])



    authorise()

    
    repeated_posts_iteration = 1 # Non-zero value to start while loop
    repeated_posts_total = 0
    posts_saved = 0

    while repeated_posts_iteration != 0:
        
        repeated_posts_iteration = 0
        
        sleep(1.01) # To limit API for 60 requests per minute to comply with Reddit rules
        if listing == "top":
            request = requests.get(f"https://oauth.reddit.com/r/{subreddit_string}/{listing}/?t={time_period}&after={last_fullname}&limit={n_posts}", headers=headers)
        else:
            request = requests.get(f"https://oauth.reddit.com/r/{subreddit_string}/{listing}/?after={last_fullname}&limit={n_posts}", headers=headers)
            time_period = "None"

        if len(request.json()["data"]["children"]) == 0:
            print("Not enough unique posts in this request!")
            return posts_saved
        
        for post in request.json()["data"]["children"]:
            
            last_fullname = post["data"]["name"]

            if post["data"]["name"] in df["fullname"].to_list():
                repeated_posts_iteration += 1
                repeated_posts_total += 1
                continue

            df.loc[len(df.index)] = [0, listing, time_period, post["data"]["name"], post["data"]["author"], post["data"]["title"], len(post["data"]["selftext"]), replace_text(post["data"]["selftext"]), post["data"]["url"]]
            posts_saved += 1



        
        print(f"Number of already saved files in iteration: {repeated_posts_iteration}, total: {repeated_posts_total}")


    print(df)

    df.to_csv(path, sep=";", index=False)

    print("Request handeled sucessfully")
    return posts_saved




#reddit_API_get("talesfromtechsupport", 5, "top")

#reddit_request("talesfromtechsupport", 50)