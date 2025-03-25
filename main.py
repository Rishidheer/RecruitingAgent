import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 1. Load Data with error handling
try:
    resumes = pd.read_csv('data/resumes.csv')
    with open('data/job_description.txt', 'r') as file:
        job_description = file.read()
except Exception as e:
    print(f" Error loading files: {e}")
    exit()

print(" Data loaded successfully!")

# 2. Clean Data - Handle missing values and convert to string
text_column = 'Resume_str'
resumes[text_column] = resumes[text_column].fillna('')  # Replace NaN with empty string
resumes[text_column] = resumes[text_column].astype(str)  # Ensure all are strings

# 3. Score Candidates with error handling
def score_candidates(job_desc, resumes_text):
    try:
        all_texts = [job_desc] + resumes_text.tolist()
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    except Exception as e:
        print(f" Error in scoring: {e}")
        return np.zeros(len(resumes_text))  # Return zero scores if error

resumes['score'] = score_candidates(job_description, resumes[text_column])
print(f" Scored {len(resumes)} candidates successfully!")

# 4. Get Top 3 Candidates
top_candidates = resumes.sort_values('score', ascending=False).head(3)

print("\n TOP 3 CANDIDATES:")
for idx, candidate in top_candidates.iterrows():
    print(f"\n👤 Candidate ID: {candidate['ID']} (Score: {candidate['score']:.2f})")
    print(f" Category: {candidate['Category']}")
    print(f" Skills/Experience: {candidate[text_column][:200]}...")

# 5. Save Results
try:
    top_candidates.to_csv('data/top_candidates.csv', index=False)
    print("\n Results saved to 'top_candidates.csv'!")
except Exception as e:
    print(f" Error saving results: {e}")