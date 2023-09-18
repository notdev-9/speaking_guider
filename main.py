import os
import whisper

AUDIO_FOLDER = 'audio-files'
TRANSCRIBED_FOLDER = 'transcribed-files'

def writeTranscribedTextToFile(text: str, equivalentAudioFileName: str, folderName: str = TRANSCRIBED_FOLDER):
    if not os.path.exists(folderName):
        os.mkdir(folderName)
        print(f"Folder '{folderName}' created successfully.")
    # split and remove the right most strings after the last '.' and add 'txt'
    # e.g. 'abc.zxc.sedew' => 'abc.zxc.txt'
    fileName = ''.join(equivalentAudioFileName.split('.')[:-1]) + '.txt'
    with open(folderName + '\\' + fileName, 'w') as transcribedFile:
        transcribedFile.write(text)

# Main function
def main():
    audioFileNames = os.listdir(os.path.abspath(os.getcwd()) + '\\' + AUDIO_FOLDER)
    whisperModel = whisper.load_model('base')
    for fileName in audioFileNames:
        result = whisperModel.transcribe(AUDIO_FOLDER + '\\' + fileName)
        transcribedText = result['text']
        if transcribedText:
            writeTranscribedTextToFile(transcribedText, fileName, TRANSCRIBED_FOLDER)

if __name__ == '__main__':
    main()