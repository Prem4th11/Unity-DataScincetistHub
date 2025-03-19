import pandas as pd
import re
import nltk
import streamlit as st
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import pyttsx3  # Import text-to-speech

# ---------------------- STEP 1: Load Dataset ----------------------
df = pd.read_csv("fake_news_dataset.csv")

# ---------------------- STEP 2: Data Preprocessing ----------------------
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = ' '.join(word for word in text.split() if word not in stop_words)
    return text

df['clean_text'] = df['text'].apply(clean_text)

# ---------------------- STEP 3: Split Data ----------------------
X = df['clean_text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------- STEP 4: Apply TF-IDF ----------------------
tfidf = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf.fit_transform(X_train).toarray()
X_test_tfidf = tfidf.transform(X_test).toarray()

# ---------------------- STEP 5: Encode Labels ----------------------
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(y_train)
y_test = label_encoder.transform(y_test)

# ---------------------- STEP 6: Balance Data with SMOTE ----------------------
smote = SMOTE(sampling_strategy='auto', k_neighbors=1)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_tfidf, y_train)

# ---------------------- STEP 7: Train the Model ----------------------
model = LogisticRegression()
model.fit(X_train_resampled, y_train_resampled)

# Predict on test data
y_pred = model.predict(X_test_tfidf)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# ---------------------- STEP 8: Define Prediction Function ----------------------
def predict_news(news_text):
    news_text = clean_text(news_text)
    vectorized_text = tfidf.transform([news_text]).toarray()
    prediction = model.predict(vectorized_text)[0]
    return label_encoder.inverse_transform([prediction])[0]  # Convert to "Fake News" or "Real News"

# ---------------------- STEP 9: Set Up Streamlit App with Dropdown ----------------------
st.title("📰 Fake News Detector")

# Dropdown menu with available news headlines
selected_news = st.selectbox("Select a News Article:", df['text'].tolist())

# Button to check the prediction
if st.button("Check"):
    result = predict_news(selected_news)
    st.write(f"### Prediction: **{result}**")

    # ---------------------- STEP 10: Announce Result with Text-to-Speech ----------------------
    engine = pyttsx3.init()
    engine.say(f"The selected news is {result}")
    engine.runAndWait()

# Run this with:
# streamlit run fake_news_detection.py
