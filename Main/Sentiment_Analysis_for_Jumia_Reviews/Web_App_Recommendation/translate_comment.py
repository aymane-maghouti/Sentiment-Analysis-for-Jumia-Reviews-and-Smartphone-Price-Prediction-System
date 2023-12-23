from translate import Translator

def translate_french_to_english(phrase):
    translator= Translator(to_lang="en", from_lang="fr")
    translation = translator.translate(phrase)
    return translation





