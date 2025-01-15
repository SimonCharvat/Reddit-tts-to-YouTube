from PIL import Image,ImageDraw,ImageFont
import pandas
from text_handler import wrap_long_text





#max_line_len_glob = 63 # maximum string length per line
#max_line_count_glob = 21 # maximum lines per image/page


def get_size_of_string(string: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    """Returns the width and height of the string
    Used for compatibility. Old version of PIL used function 'getsize' which is now replaced with 'getbox'.

    Args:
        string (str): _description_
        font (ImageFont.FreeTypeFont): _description_

    Returns:
        tuple[int, int]: _description_
    """
    left, top, right, bottom = font.getbbox(string)
    width, height = right - left, bottom - top
    return width, height



#font.getsize(line)[1]

font_path = "./font/Cousine-Regular.ttf"
font_text = ImageFont.truetype(font_path, 35)
font_left_top_corner = ImageFont.truetype(font_path, 25)
font_url = ImageFont.truetype(font_path, 16)
font_title = ImageFont.truetype(font_path, 45)
font_outro = ImageFont.truetype(font_path, 40)

col_white = (255, 255, 255)
col_gray = (150, 150, 150)

# Commented out and replaced with custom function for compatibility with new pillow version
# height_text = font_text.getsize("X")[1] * 1.1
# height_left_top_corner = font_left_top_corner.getsize("X")[1] * 1.1
# height_url = font_url.getsize("X")[1] * 1.1
# height_title = font_title.getsize("X")[1] * 1.2
# height_outro = font_outro.getsize("X")[1] * 1.1

# New compatible functions
height_text = get_size_of_string("X", font_text)[1] * 1.1
height_left_top_corner = get_size_of_string("X", font_left_top_corner)[1] * 1.1
height_url = get_size_of_string("X", font_url)[1] * 1.1
height_title = get_size_of_string("X", font_title)[1] * 1.2
height_outro = get_size_of_string("X", font_outro)[1] * 1.1

x_pos = 300
y_pos = 200
width = 1920
height = 1080

def generate_images(list_of_seperated_lines, post_index, page_index, title, author, url):
    image = Image.open("./images/canvas.png")

    draw_engine = ImageDraw.Draw(image)
    draw_engine.text((10 , 10), title, font=font_left_top_corner, fill = col_gray)
    draw_engine.text((10 , 10 + height_left_top_corner), f"Author: {author}", font=font_left_top_corner, fill = col_gray)
    draw_engine.text((10 , height - 10 - height_url), f"Source: {url}", font=font_url, fill = col_gray)

    for i, string in enumerate(list_of_seperated_lines):
        draw_engine.text((x_pos , y_pos + height_text * i), string, font=font_text, fill = col_white)
        
    image.save(f"./TEMP/{post_index}_{page_index}_image.png")

    
def generate_post_intro(post_index, title, author, url):
    image = Image.open("./images/canvas.png")
    draw_engine = ImageDraw.Draw(image)
    
    
    
    text_as_list = wrap_long_text(title, 35, 1000)[0]
    n_rows = len(text_as_list)

    for i, string in enumerate(text_as_list):
        string = string
        w1, h1 = get_size_of_string(string, font_title)
        draw_engine.text(((width - w1) / 2, height / 2 - n_rows * height_title + i * height_title), string, font=font_title, fill=col_white) # Main title - centered

    
    w2, h2 = get_size_of_string(author, font_title)
    draw_engine.text(((width - w2)/2,(height - h2)/2 + height_title + h1), author, font=font_title, fill=col_white) # Author - centered
    draw_engine.text((10 , height - 10 - height_url), f"Source: {url}", font=font_url, fill = col_gray) # url

    image.save(f"./TEMP/{post_index}_intro_image.png")





def generate_post_outro(post_index, title, author = "Reddit Voiceover", music_file_name = None):

    image = Image.open("./images/canvas.png")
    draw_engine = ImageDraw.Draw(image)
    
    
    text_as_list = wrap_long_text(title, 35, 1000)[0]
    n_rows = len(text_as_list)

    for i, string in enumerate(text_as_list):
        string = string
        w1, h1 = get_size_of_string(string, font_outro)
        draw_engine.text(((width - w1) / 2, height / 2 - n_rows * height_title + i * height_title + 2*height_title), string, font=font_outro, fill=col_white) # Main title - centered

    w2, h2 = get_size_of_string(author, font_outro)
    draw_engine.text(((width - w2)/2,(height - h2)/2 + 2 * height_title + h1 + 2*height_title), author, font=font_outro, fill=col_white) # Author - centered
    
    if music_file_name != None:
        for i, row in pandas.read_csv("./music/0_music_list.csv", sep=";").iterrows():
            if row["file_name"] == music_file_name:
                music_track = row["name"]
                music_author = row["author"]
        
        draw_engine.text((10 , height - 10 - height_url), f"Music: {music_track} | by {music_author}", font=font_url, fill = col_gray) # url

    image.save(f"./TEMP/{post_index}_outro_image.png")





def resize_image(new_resolution, load_file_path, save_file_path):
    """
    Description
    ---------
    Resizes image.

    Parameters
    ---------
    new_resolution : tuple
        New desired reesolution
        Example: (1280, 720)
    
    load_file_path : str
        Path to the source image. Path must include files extension
    
    save_file_path : str
       Path must include files extension
    
    Returns
    ---------
    Returns nothing.
    """

    image = Image.open(load_file_path)
    new_image = image.resize(new_resolution)
    new_image.save(save_file_path)

    print(f"Image resized: {save_file_path}")









#draw_engine.text((300, 200), string, font=font_text, fill = (255, 255, 255))


#image.show()

#generate_post_intro(100, "01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789", "Author", "url")