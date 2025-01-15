

from math import remainder


def format_time(time_in_sec):
    """
    Parameters
    ---------
    time_in_sec : float
        Time in seconds

    Returns
    ---------
    Returns string, timestamp in format hh:mm:ss
    """

    hh = str(int(time_in_sec // 3600))
    remaining = time_in_sec % 3600
    mm = str(int(remaining // 60))
    ss = str(int(round(remaining % 60)))

    # checks for minutes or hours having value 60 (youtube doesn't support 60 as valid value)
    if ss == 60:
        ss = 59
    if mm == 60:
        mm = 0
        hh += 1

    # formats 1 digit value as 2 digits ( 5 -> 05 )
    if len(hh) == 1:
        hh = f"0{hh}"
    if len(mm) == 1:
        mm = f"0{mm}"
    if len(ss) == 1:
        ss = f"0{ss}"

    return f"{hh}:{mm}:{ss}"

def get_chapters_text(lenght_list):
    """
    Parameters
    ---------
    lenght_list : list
        List of lenghts of audio files (including video intro, subreddit intro, outro) [in seconds]

    Returns
    ---------
    Returns length of audio file in seconds
    """

    rows = []
    rows.append(" ")
    rows.append("Timestamps:")
    rows.append(f"{format_time(lenght_list.pop(0))} Intro")

    cur_time = 0

    for i, leng in enumerate(lenght_list):
        
        cur_time += leng

        if i + 1 == len(lenght_list):
            rows.append(f"{format_time(cur_time)} Outro")
            break

        rows.append(f"{format_time(cur_time)} Post #{i + 1}")

    final = "--!--".join(rows)
    print(final)
    return final