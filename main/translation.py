from googletrans import Translator

def translate_text(text, src_language, out_language='en'):
    translator = Translator()
    translation = translator.translate(text, src=src_language, dest=out_language)

    return translation.text
