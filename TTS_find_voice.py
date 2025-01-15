import pyttsx3
engine = pyttsx3.init()

# Find the right voice by looping through all avaliavble voices
# recommended: MSTTS_V110_enCA_RichardM <- find this by changing ID

engine.setProperty("rate", 135) # default = 200, recommended: 135
engine.setProperty('volume',1.0) # default = 1.0 (in range 0-1), recommended: 1.0

voices = engine.getProperty('voices') 

engine.setProperty('voice', voices[3].id) 

engine.runAndWait()

test_phrase = "Hello World!"

for i, voice in enumerate(voices):
    print(f"Index: {i}, Name: {voice.name}")
    engine.setProperty("voice", voice.id)
    engine.say(f"{i}, {test_phrase}")
    engine.runAndWait()
    engine.stop()