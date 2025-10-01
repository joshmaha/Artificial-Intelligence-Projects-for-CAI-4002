# Joshua Maharaj Sentiment Analysis
# Sentiment Analysis Implementation using a vectorization approach.
# This module provides functionality to train a sentiment model from labeled data and use it to classify the sentiment of new text as positive or negative.

import json # used to access json files storing reviews
import string # to modify strings (lowercase, splitting and joining strings)
from nltk.tokenize import word_tokenize # to split words into individual pieces
from nltk.corpus import stopwords # unnecessary words to analysis
from nltk.stem import WordNetLemmatizer # to normalise different variations of the same word
from sklearn.feature_extraction.text import TfidfVectorizer # for text to vector conversion
from sklearn.linear_model import LogisticRegression # to train sentiment classifier
import joblib # joblib is used to save and load training model

# global filenames for storing trained model and vectorizer
model_file = "training_model.pkl"
vectorize_file = "vectorizer.pkl"

# initialize variables to preprocess data properly
stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

# remove stopwords (unimportant words) from text, for example I, me, the, ...
def remove_stopwords(words):
    return [word for word in words if word.lower() not in stop_words]

# converts words to their base/dictionary form for example, "running," "ran," and "runs" are all lemmatized to "run."
def lemmatize(words):
    return [lemmatizer.lemmatize(word) for word in words]

# takes the given text and translates it to lowercase, removes both punctuations and stopwords and then stems and lemmatizes the text
def preprocess_text(text):

    lowercase_text = text.lower()  # lowercase all text
    only_text = lowercase_text.translate(str.maketrans("", "", string.punctuation))  # delete all punctuation
    words = word_tokenize(only_text)  # split text into individual words
    clean_text = remove_stopwords(words)  # delete all stopwords
    final_text = lemmatize(clean_text) # apply lemmatizing to applicable words
    return " ".join(final_text) # return final data as one new string with all unneccessary data removed

# uses given json training file to train sentiment analysis model
def calcSentiment_train(trainFile):

    reviews, sentiments = [], [] # review is the string of movie review and sentiment is a score (1 for positive or 0 for negative) of the review

    # open training file in read mode and set encoding to utf-8 for proper special case handling
    with open(trainFile, "r", encoding="utf-8") as file:
        for line in file:
            data = json.loads(line) # convert each string into a dictionary
            reviews.append(preprocess_text(data["review"]))  # preprocess the review text then add it to the review list
            sentiments.append(1 if data["sentiment"] else 0)  # convert boolean to integer then add to sentiment list
    
    # convert preprocessed reviews into vectors
    vectorizer = TfidfVectorizer(max_features=10000)  # only consider the most important 10000 words so that code runs faster
    # tfidf measures how important each word is in a review relative to the dataset
    X = vectorizer.fit_transform(reviews)  # matrix that will help the model learn vocabulary and transform reviews into feature vectors
    model = LogisticRegression(max_iter=500)  # set max iterations to 500 to ensure convergence
    model.fit(X, sentiments)  # train model on feature vectors and sentiment labels

    # save trained model and vectorizer to disk for later use
    joblib.dump(model, model_file)
    joblib.dump(vectorizer, vectorize_file)

# predicts the sentiment of movie review based on training model
def calcSentiment_test(review):

    model = joblib.load(model_file) # load trained model and vectorizer from disk
    vectorizer = joblib.load(vectorize_file)
    processed_review = preprocess_text(review)  # preprocess given review    
    X = vectorizer.transform([processed_review]) # convert processed review into a feature vector using the trained vectorizer
    prediction = model.predict(X)[0]  # predict the sentiment (0 = negative and 1 = positive)
    
    return bool(prediction)  # convert predictions from integer to boolean and return it
