import speech_recognition as sr
import os
import datetime

def write_text_to_file(data, base_file_name, out_file=None):
    print("Current_working", os.getcwd())
    out_file_name = out_file if out_file else 'text_' + base_file_name + '.txt'
    with open(out_file_name, 'w') as of:
        of.write(' '.join(data))
    print("Generated Text Output: ", out_file_name)


def convert_wav_to_txt(audio_split_file):
    r = sr.Recognizer()
    # use the audio file as the audio source
    with sr.AudioFile(audio_split_file) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Sphinx
    try:
        # data = r.recognize_sphinx(audio)
        data = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
    return data


def process_files(files_directory, base_file_name):
    text_data = []
    for filename in os.listdir(files_directory):
        if base_file_name in os.path.basename(filename):
            text_data.append(convert_wav_to_txt(os.path.join(files_directory, filename)))
            print("filename: ", filename)
    return text_data


def split_audio_files(audio_file, base_file_name, ffmpeg_directory):
    cwd = os.getcwd()
    os.chdir(ffmpeg_directory)
    temp_folder = r'temp_audio_files'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    temp_files_path = os.path.join(ffmpeg_directory, temp_folder)
    # os.chdir(temp_files_path)
    ffmpeg_command = f"ffmpeg -i {audio_file} -f segment -segment_time 15 -c copy {temp_folder}/{base_file_name}%09d.wav"
    print("ffmpeg_command: ", ffmpeg_command)
    os.system(ffmpeg_command)
    os.chdir(cwd)
    return temp_files_path


def main(audio_file_name, ffmpeg_directory):
    # audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    #                           r"D:\Python\Speech_toText\AudioFiles\a_dream.wav")
    audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              audio_file_name)
    base_file_name = os.path.splitext(os.path.basename(audio_file))[0]
    files_directory = split_audio_files(audio_file, base_file_name, ffmpeg_directory)
    text_data = process_files(files_directory, base_file_name)
    write_text_to_file(text_data, base_file_name, out_file=None)


if __name__ == '__main__':
    start = datetime.datetime.now()
    audio_file_name = r"D:\Python\Speech_toText\audio_file.wav"
    ffmpeg_directory = r"D:\Python\Speech_toText\ffmpeg\ffmpeg_win64_static\bin"
    main(audio_file_name, ffmpeg_directory)
    print("time took: ", datetime.datetime.now()-start)
