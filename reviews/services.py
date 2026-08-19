from cats.bad_words import BAD_WORDS

def censor_text(text):
    """Заменяет плохие слова на звездочки"""
    has_bad = False
    for word in BAD_WORDS:
        w = word.strip().lower()
        if w and w in text.lower():
            has_bad = True
            text = text.replace(word, '*' * len(word))
            text = text.replace(word.capitalize(), '*' * len(word))
            text = text.replace(word.upper(), '*' * len(word))
    return text, has_bad