import streamlit as st
import requests
import json
import soundfile as sf
import io
import tempfile
import pydub 
import numpy as np
import os
import whisper
import pathlib

AUDIO_FOLDER = 'audio-files'
TRANSCRIBED_FOLDER = 'transcribed-files'

def createFolderIfNotExist(folderName: str):
    if not os.path.exists(folderName):
        os.mkdir(folderName)
        print(f"Folder '{folderName}' created successfully.")

def getEquivalentTextFileName(audioFileName: str) -> str:
    return ''.join(audioFileName.split('.')[:-1]) + '.txt'

def writeTranscribedTextToFile(text: str, audioFileName: str, \
    folderName: str = TRANSCRIBED_FOLDER):
    createFolderIfNotExist(folderName)
    # split and remove the right most strings after the last '.' and add 'txt'
    # e.g. 'abc.zxc.sedew' => 'abc.zxc.txt'
    fileName = getEquivalentTextFileName(audioFileName)
    with open(folderName + '\\' + fileName, 'w') as transcribedFile:
        transcribedFile.write(text)

def main():
    # create TRANSCRIBED_FOLDER if not exist
    createFolderIfNotExist(TRANSCRIBED_FOLDER)

    st.title("💡AI-powered apps for IELTS")
    # Upload section
    st.subheader("Upload your IELTS speaking answer 💭")
    uploaded_file = st.file_uploader("Choose an audio or video file", \
        type=["mp3", "wav", "ogg", "flac", "mp4", "mov", "avi", "mkv", "m4a"])
    # Handle uploaded file
    if uploaded_file is not None:
        # file is transcribed, just use it
        transcribedFileNames = os.listdir(os.path.abspath(os.getcwd()) + \
            '\\' + TRANSCRIBED_FOLDER)
        equivalentTranscribedFileName = \
            getEquivalentTextFileName(uploaded_file.name)
        if equivalentTranscribedFileName in transcribedFileNames:
            file_path = os.path.abspath(os.getcwd()) + '\\' + \
                TRANSCRIBED_FOLDER + '\\' + equivalentTranscribedFileName
            try:
                # Open the file for reading
                with open(file_path, "r") as f:
                    # Read the entire content of the file
                    file_content = f.read()
                    print(
                        f'Read {uploaded_file.name} from FOLDER={TRANSCRIBED_FOLDER}'
                    )
                    transcribedText = file_content
            except FileNotFoundError:
                print(f"The file '{file_path}' does not exist.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        else: # new file, use whisper to transcribe it
            st.audio(uploaded_file)
            transcribedText = None
            with st.spinner("Analyzing file..."):
                whisperModel = whisper.load_model('base')
                save_filename = 'audio.m4a'
                with open(save_filename, "wb") as f:
                    f.write(uploaded_file.read())

                result = whisperModel.transcribe('audio.m4a')
                transcribedText = result['text']
                pathlib.Path('audio.m4a').unlink()
                writeTranscribedTextToFile(
                    transcribedText, uploaded_file.name, TRANSCRIBED_FOLDER
                )
        st.success("Transcribed text:")
        st.text_area("Transcribed text:", transcribedText, label_visibility = 'hidden')     

if __name__ == "__main__":
    main()