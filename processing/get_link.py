from bot_set.texts import LETTERS_PARS
from bot_set.links import NOUN_LINK, ENDINGS, VERB_LINK
import requests


def get_noun_link(text: str) -> str:
    """Функция-преобразователь, возвращает готовую ссылку на изображение

    Предварительно проводит проверку на содержание умлаутов в слове. Если умлаут присутствует, то он будет заменен на
    релевантный кодовый знак, применяемый автором изображений.
    """
    text = text.strip().capitalize()
    for letter, umlaut in LETTERS_PARS.items():
        if umlaut in text:
            text = text.replace(umlaut, letter + "3")

    word_link = NOUN_LINK + text + ".png"
    return word_link


def get_verb_link(text: str) -> str | None:
    """Функция-преобразователь, возвращает готовую ссылку на изображение

    Предварительно проводит проверку на содержание умлаутов в слове. Если умлаут присутствует, то он будет заменен на
    релевантный кодовый знак, применяемый автором изображений.
    """
    text = text.strip().lower()
    for letter, umlaut in LETTERS_PARS.items():
        if umlaut in text:
            text = text.replace(umlaut, letter + "3")

    for i_end in ENDINGS:
        wort_link = VERB_LINK + text + i_end
        response = requests.get(url=wort_link)
        if response.status_code == 200:
            return wort_link
    else:
        return None
