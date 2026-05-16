# using tf-idf and jd-resume similarity to rank resumes.
import pdfplumber
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def pdf_txt(path):
    text = ""
    with pdfplumber.open("path") as resume:
        for page in resume.pages:
            if page.extract_text():
                text+= page.extract_text()+ " "
    
    return text.strip()


def find_scores(jd, resumes):
    docs = [jd] + resumes # list
    vectorizer = TfidfVectorizer(ngram_range=(1,2), stop_words="English")
    tfidf_matrix = vectorizer.fit_transform(docs)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    results = list()
    for idx, score in enumerate(similarities):
        results.append((idx,score*100))
    results.sort(key=lambda x: x[1],reverse = True) # sort by scores
    return results
