import string

def clean(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text