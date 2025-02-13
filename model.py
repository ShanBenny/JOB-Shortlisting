# model.py
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import pickle
import os

nltk.download('punkt_tab')
# Set the NLTK data path
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

# Download NLTK data
nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)

def preprocess_text(text):
    # Tokenize and remove punctuation
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalnum()]
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

def calculate_similarity(resume, job_description):
    # Preprocess texts
    resume_processed = preprocess_text(resume)
    job_description_processed = preprocess_text(job_description)
    
    # Vectorize texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_processed, job_description_processed])
    
    # Calculate cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

# Save the model (optional)
def save_model():
    with open('models/nlp_model.pkl', 'wb') as f:
        pickle.dump(calculate_similarity, f)

if __name__ == '__main__':
    
    save_model()