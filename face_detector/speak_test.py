from gtts import gTTS
import os

# The text that you want to convert to audio 
mytext = 'Face detected!'
# Language in which you want to convert 
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3") 

# Playing the converted file 
os.system("mpg321 welcome.mp3")
#os.system("start welcome.mp3")
