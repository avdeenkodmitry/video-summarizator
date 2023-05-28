import whisper_timestamped as whisper


def run_transcription(path_to_videofile, model):
    audio = whisper.load_audio(path_to_videofile)
    transcription_result = whisper.transcribe(model, audio, language="en")
    return transcription_result['text']


model = whisper.load_model("small")



#if __name__ == "__main__":
#    model = whisper.load_model("small")
#    transcription_text = run_transcription('dimas_zarabatyvat.mp4')
#    print(transcription_text)
#    time.sleep(30)
#