import os
import speech_recognition as sr
from multiprocessing.dummy import Pool
import logging
import argparse
import datetime
import shutil

logging.basicConfig(level=logging.INFO)


def write_text_to_file(text, base_file_name, out_file=None):
    """
    write the converted text into a text file
    :param text: list of all file chunks text output
    :param base_file_name: base name of audio file without extension
    :param out_file: output text file name
    """
    out_file_name = out_file if out_file else 'text_' + base_file_name + '.txt'
    with open(out_file_name, 'w') as of:
        of.write('\n'.join(text))
    logging.info(f"Generated Text Output: {out_file_name}")


def transcribe(data):
    """
    convert the audio file chunk into text output
    :param data: tuple of file name and file id
    :return: dictionary of file id and corresponding text output
    """
    idx, file = data
    r = sr.Recognizer()
    # use the audio file as the audio source
    with sr.AudioFile(file) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)  # read the entire audio file

    # recognize speech using google
    try:
        text = r.recognize_sphinx(audio)
        # text = r.recognize_wit(audio, key='HMLOVTKLARJR2FDJC5776ZS2VSSDIJCW')
    except sr.UnknownValueError:
        logging.error("Google could not understand audio")
    except sr.RequestError as e:
        logging.error("Google error; {0}".format(e))
    return {
        "idx": idx,
        "text": text
    }


def process_files(files_directory, base_file_name):
    """
    process all the file chunks parallelly in pools of threads with each pool size of 8 and
    collect all the text outputs and make a list.
    :param files_directory:
    :return: output text that converted form audiofile
    """
    files = os.listdir(files_directory)
    files = [os.path.join(files_directory, file) for file in files if base_file_name in file]
    print("files: ", files)
    pool = Pool(10)
    all_text = pool.map(transcribe, enumerate(files))
    pool.close()
    pool.join()
    transcript = []
    for t in sorted(all_text, key=lambda x: x['idx']):
        transcript.append(t['text'])
    return transcript


def split_audio_files(audio_file, base_file_name, ffmpeg_directory):
    """
    Split the given audio file into multiple file chunks. Each file chunk is 15sec duration
    :param audio_file: audio file to be converted
    :param base_file_name: base name of audio file without extension
    :param ffmpeg_directory: ffmpeg.exe directory
    :return: file chunks directory
    """
    cwd = os.getcwd()
    os.chdir(ffmpeg_directory)
    temp_folder = r'temp_audio_files'
    if not os.path.exists(temp_folder):
        os.mkdir(temp_folder)
    temp_files_path = os.path.join(ffmpeg_directory, temp_folder)
    ffmpeg_command = f"ffmpeg -i {audio_file} -f segment -segment_time 15 " \
                     f"-c copy {temp_folder}/{base_file_name}%09d.wav"
    logging.info(f"ffmpeg_command: {ffmpeg_command}")
    os.system(ffmpeg_command)
    os.chdir(cwd)
    return temp_files_path


def main(audio_file_name, ffmpeg_directory, out_file=None):
    """
    Initiate the speech to text conversion
    :param audio_file_name: audio file to be converted
    :param ffmpeg_directory: ffmpeg.exe directory
    """
    audio_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                              audio_file_name)
    if audio_file.endswith('wav'):
        base_file_name = os.path.splitext(os.path.basename(audio_file))[0]
        files_directory = split_audio_files(audio_file, base_file_name, ffmpeg_directory)
        text_data = process_files(files_directory, base_file_name)
        write_text_to_file(text_data, base_file_name, out_file=out_file)
        shutil.rmtree(files_directory)
    else:
        raise Exception("Audio file should be in .wav format")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a', '--wavfile',
        help='Audio file in wav format',
        required=True)

    parser.add_argument(
        '-f', '--ffmpeg',
        help='ffmpeg.exe directory',
        required=True)

    parser.add_argument(
        '-o', '--outfile',
        help='Output text file name(optional)',
        required=False)
    args = parser.parse_args()
    audio_file_name = args.wavfile
    ffmpeg_directory = args.ffmpeg
    out_filename = args.outfile if args.outfile else None
    start = datetime.datetime.now()
    main(audio_file_name, ffmpeg_directory, out_file=out_filename)
    print("time took: ", datetime.datetime.now() - start)