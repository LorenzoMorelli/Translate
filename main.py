# -*- coding: utf-8 -*-
import webbrowser
from textblob import TextBlob, exceptions
from wox import Wox, WoxAPI
import nltk
from nltk.corpus import words

LANGUAGE_OTHER = 'it'
LANGUAGE_MAIN = 'en'

def contains_english_word(phrase: str):
    return phrase.split(" ")[0] in set(words.words())


def translate(query):
    query_modified = query.strip().lower()
    en = set(chr(i) for i in range(ord('a'), ord('z') + 1))
    results = []
    if query_modified:
        try:
            # detect if first word is in english or italian           
            from_lang, to_lang = (LANGUAGE_MAIN, LANGUAGE_OTHER) if contains_english_word(query_modified) else (LANGUAGE_OTHER, LANGUAGE_MAIN)
            translation = TextBlob(query_modified).translate(from_lang, to_lang)
            results.append({
                "Title": str(translation),
                "SubTitle": query,
                "IcoPath":"Images/app.png",
                "JsonRPCAction":{'method': 'openUrl',
                                 'parameters': [r'http://translate.google.com/#{}/{}/{}'.format(from_lang, to_lang, query)],
                                 'dontHideAfterAction': False}
            })
        except exceptions.NotTranslated:
            pass
    if not results:
        results.append({
                "Title": 'Not found',
                "SubTitle": '',
                "IcoPath":"Images/app.png"
            })
    return results

class Translate(Wox):
    def query(self, query):
        return translate(query)

    def openUrl(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    nltk.download('words')
    Translate()
