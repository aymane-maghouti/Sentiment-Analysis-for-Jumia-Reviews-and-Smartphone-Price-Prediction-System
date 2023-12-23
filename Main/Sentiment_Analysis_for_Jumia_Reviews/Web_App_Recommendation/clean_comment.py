import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from contractions import contractions_dict
import nltk

# nltk.download('punkt')
# nltk.download('stopwords')





def clean_text(text):
    # Convert to lowercase
    text = text.lower()

    # Expand contractions
    text = expand_contractions(text, contractions_dict)

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Remove non-alphanumeric characters
    text = remove_non_alphanumeric(text)

    # Remove URLs
    text = remove_urls(text)

    # Remove stop words with English
    stop_words = set(stopwords.words('english'))  # You can replace 'english' with the appropriate language
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Remove stop words with French
    stop_words = set(stopwords.words('french'))  # You can replace 'english' with the appropriate language
    words = word_tokenize(text)
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Remove short words
    text = remove_short_words(' '.join(filtered_words))

    # Lemmatization (optional)
    lemmatizer = nltk.WordNetLemmatizer()
    filtered_words = [lemmatizer.lemmatize(word) for word in filtered_words]

    # Join the words back into a string
    cleaned_text = ' '.join(filtered_words)

    return cleaned_text



# Contractions dictionary for expanding contractions
contractions_dict = {
    "it's": "it is",
    "i'm": "i am",
    "don't": "do not",
    "won't": "will not",
    "can't": "cannot",
    "I'll": "I will",
    "you're": "you are",
    "he's": "he is",
    "she's": "she is",
    "we're": "we are",
    "they're": "they are",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "haven't": "have not",
    "hasn't": "has not",
    "hadn't": "had not",
    "could've": "could have",
    "should've": "should have",
    "would've": "would have",
    "didn't": "did not",
}

def expand_contractions(text, contractions_dict):
    words = text.split()
    expanded_text = [contractions_dict.get(word, word) for word in words]
    return ' '.join(expanded_text)


def remove_non_alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)


def remove_urls(text):
    return re.sub(r'http\S+', '', text)


def remove_short_words(text, min_length=2):
    words = text.split()
    long_words = [word for word in words if len(word) >= min_length]
    return ' '.join(long_words)






