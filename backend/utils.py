from underthesea import word_tokenize

def preprocess_text(text):
    stopwords = set(['là', 'và', 'của', 'trong', 'đó', 'với', 'có'])
    words = word_tokenize(text, format="text")
    words = [word for word in words.split() if word not in stopwords]
    return ' '.join(words)
