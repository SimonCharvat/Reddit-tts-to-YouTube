import pyttsx3
from pydub import AudioSegment

engine = pyttsx3.init()

engine.setProperty("rate", 135) # default = 200, recommended: 135
engine.setProperty('volume',1.0) # default = 1.0 (in range 0-1), recommended: 1.0

voices = engine.getProperty('voices') 

engine.setProperty('voice', voices[3].id)
engine.runAndWait()

print(f"Voice:\n{engine.getProperty('voice')}\nText to speeach ready for input")



def tts_to_file(text_string, save_file_path, input_is_list = False): #add .mp3 to file path
    """
    Parameters
    ---------
    text_string : str
        String of text to be converted to speech .mp3 file
    save_file_path : str
        The file path for saving. Path must include file name and afix .mp3
    input_is_list : bool
        True if the input string is list, false if input string is regular string.
        Default: False

    Returns
    ---------
    Returns length of audio file in seconds
    """

    global engine

    if input_is_list:
        text_string = " ".join(text_string)

    text_string = text_string.replace("#", "")
    text_string = text_string.replace("\\", "")
    text_string = text_string.replace("_", "")
    text_string = text_string.replace("https:\\\\", "")
    text_string = text_string.replace("https", "")
    
    engine.save_to_file(text_string, save_file_path)
    engine.runAndWait()

    audio_length = AudioSegment.from_file(save_file_path).duration_seconds
    return audio_length


#tts_to_file('Hello, welcome to new reddit voiceover update. Today we will take a look on subreddit: Tales From Tech Support, Enjoy. \n \n ', './TEMP/00_intro_voice.mp3')