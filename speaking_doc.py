from gtts import gTTS


def speaking(content, lang):
    tts = gTTS(text=content, lang=lang)
    file_path = f"output_{lang}.mp3"
    tts.save(file_path)
    return file_path
