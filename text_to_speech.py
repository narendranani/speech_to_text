import time
from gtts import gTTS


def convert(text_to_convert):
    # This module is imported so that we can
    # play the converted audio
    import os
    print("text_to_convert: ", text_to_convert)
    # Language in which you want to convert
    language = 'en'

    # Passing the text and language to the engine,
    # here we have marked slow=False. Which tells
    # the module that the converted audio should
    # have a high speed
    speech_object = gTTS(text=text_to_convert, lang=language, slow=False)

    # Saving the converted audio in a mp3 file named
    time_stamp = time.strftime("%Y%m%d_%H%M%S")
    mp3_file_name = "Notification" + time_stamp + '.mp3'
    speech_object.save(mp3_file_name)

    # Playing the converted file
    # os.system(" omxplayer " + mp3_file_name)

if __name__ == '__main__':
    text_to_convert = "Python is an interpreted high-level programming language for general-purpose programming. Created by Guido van Rossum and first released in 1991, Python has a design philosophy that emphasizes code readability, notably using significant whitespace. It provides constructs that enable clear programming on both small and large scales. Python features a dynamic type system and automatic memory management. It supports multiple programming paradigms, including object-oriented, imperative, functional and procedural, and has a large and comprehensive standard library"
    convert(text_to_convert)