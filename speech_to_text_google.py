# import os
# import speech_recognition as sr
# from tqdm import tqdm
# from multiprocessing.dummy import Pool
#
# pool = Pool(8)  # Number of concurrent threads
#
# with open("api_key.json") as f:
#     GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()
#
# r = sr.Recognizer()
# audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                           r'D:\Python\Speech_toText\ffmpeg\ffmpeg_win64_static\bin\temp_audio_files')
# files = sorted(os.listdir(audio_file))
#
#
# def transcribe(data):
#     idx, file = data
#     # name = "parts/" + file
#     name = os.path.join(audio_file, f)
#     print(" started", name )
#     # Load audio file
#     with sr.AudioFile(name) as source:
#         audio = r.record(source)
#     # Transcribe audio file
#     text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
#     print(name + " done")
#     return {
#         "idx": idx,
#         "text": text
#     }
#
#
# all_text = pool.map(transcribe, enumerate(files))
# pool.close()
# pool.join()
#
# transcript = ""
# for t in sorted(all_text, key=lambda x: x['idx']):
#     total_seconds = t['idx'] * 30
#     # Cool shortcut from:
#     # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
#     # to get hours, minutes and seconds
#     m, s = divmod(total_seconds, 60)
#     h, m = divmod(m, 60)
#
#     # Format time as h:m:s - 30 seconds of text
#     transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t['text'])
#
# print(transcript)
#
# with open("transcript.txt", "w") as f:
#     f.write(transcript)

import os
import speech_recognition as sr
from tqdm import tqdm

with open("api_key.json") as f:
    GOOGLE_CLOUD_SPEECH_CREDENTIALS = f.read()

r = sr.Recognizer()
audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                          r'D:\Python\Speech_toText\ffmpeg\ffmpeg_win64_static\bin\temp_audio_files')
files = sorted(os.listdir(audio_file))

all_text = []

for f in tqdm(files):
    name = os.path.join(audio_file, f)
    # print("files: ", f)
    # Load audio file
    with sr.AudioFile(name) as source:
        audio = r.record(source)
    # Transcribe audio file
    text = r.recognize_google_cloud(audio, credentials_json=GOOGLE_CLOUD_SPEECH_CREDENTIALS)
    all_text.append(text)

transcript = ""
for i, t in enumerate(all_text):
    total_seconds = i * 30
    # Cool shortcut from:
    # https://stackoverflow.com/questions/775049/python-time-seconds-to-hms
    # to get hours, minutes and seconds
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)

    # Format time as h:m:s - 30 seconds of text
    transcript = transcript + "{:0>2d}:{:0>2d}:{:0>2d} {}\n".format(h, m, s, t)

print(transcript)

with open("transcript.txt", "w") as f:
    f.write(transcript)
