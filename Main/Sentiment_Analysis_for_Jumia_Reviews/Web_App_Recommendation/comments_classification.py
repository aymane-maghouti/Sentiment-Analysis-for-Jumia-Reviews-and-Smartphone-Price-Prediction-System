import mysql.connector
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pickle
from clean_comment import clean_text


model_class = pickle.load(open('model.pkl', 'rb'))
model_tfidf = pickle.load(open('model_tfidf.pkl', 'rb'))






# Function to fetch comments for a product from the database
def fetch_comments(product_id):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='aymane2002',
        database='product_db'
    )

    # Fetch comments for the given product_id
    query = f"SELECT  text FROM commentaire WHERE id_prod =  {product_id}"
    comments_df = pd.read_sql(query, connection)

    # Close the database connection
    connection.close()

    # Return comments as a list
    return comments_df['text'].tolist()


# Function to analyze sentiment and make recommendations
def analyze_sentiment(product_id):
    comments = fetch_comments(product_id)
    if not comments:
        print(f"No comments for product {product_id} - Unable to provide a recommendation.")
        return 'Unable to provide a recommendation.'

    # Clean comments
    cleaned_comments = [clean_text(comment) if pd.notnull(comment) else '' for comment in comments]
    # cleaned_comments = [comment for comment in comments]
    print(cleaned_comments)
    # Transform comments using TF-IDF vectorizer
    comments_tfidf = model_tfidf.transform(cleaned_comments)


    # Predict sentiment using Naive Bayes model
    predictions = model_class.predict(comments_tfidf)
    print(predictions)

    # Count positive and negative predictions
    positive_count = sum(predictions == 1)
    negative_count = sum(predictions == -1)

    print(positive_count ," -- ",negative_count)
    # Provide recommendations based on sentiment distribution
    if positive_count > negative_count:
        print(f"Product {product_id}: This product is recommended to buy.")
        return "This product is recommended to buy"
    elif positive_count < negative_count:
        print(f"Product {product_id}: This product is not recommended to buy.")
        return "This product is not recommended to buy."
    else:
        print(f"Product {product_id}: Unable to make a clear recommendation based on sentiment distribution.")
        return "Unable to make a clear recommendation based on sentiment distribution."



