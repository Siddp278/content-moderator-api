import re
import nltk
from nltk.corpus import stopwords

# nltk.download('stopwords')

def clean_text(text):
    # Takes in sentences one by one.
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"y'all", 'you all ', text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub("dis", " this ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"arne't", " are not ", text)
    text = re.sub("bout", " about ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub("im", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub("yall", "you all", text)
    text = re.sub(" u", " you", text)
    text = re.sub("^[u] ", "you ", text)
    text = re.sub(" r", " are", text)
    text = re.sub("^[r] ", "are ", text)
    text = re.sub(" m", " am", text)
    text = re.sub("^[m] ", "am ", text)
    text = text.strip(' ')
    return text


def clean_sen(sen):
    sen = clean_text(sen)
    sen=re.sub("[\"*&#0-9;:~|?'!`]", "" , sen)
    sen=re.sub("[-.]", " " , sen)
    sen=sen.lower()
    sen=sen.split()
    sen = " ".join([i for i in sen if len(re.findall("[*@0-9/]", i))==0])
    return sen 


def clean_sen_spa(sen):
    stop_words = set(stopwords.words('spanish'))
    sen=re.sub("[\"*&#0-9;:~|?'!`]", "" , sen)
    sen=re.sub("[-.]", " " , sen)
    sen=sen.lower()
    sen=sen.split()
    sen = [w for w in sen if not w.lower() in stop_words]
    sen = " ".join([i for i in sen if len(re.findall("[*@0-9/]", i))==0])
    return sen    