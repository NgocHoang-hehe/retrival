import re
from underthesea import word_tokenize, pos_tag

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())

stopwords = load_stopwords('vietnamese-stopwords.txt')

def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    # Tách từ Tiếng Việt, dùng underthesea
    text = text.lower()
    tokens = word_tokenize(text)
    # Xóa stopwords và  các số không có ý nghĩa trong tài liệu
    tokens = [token for token in tokens if token.lower() not in stopwords and token.isalpha()]
    return ' '.join(tokens)


class SearchSystem:
    def __init__(self, documents):
        self.documents = documents
        self.preprocessed_docs = [preprocess_text(doc) for doc in documents]
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.preprocessed_docs)

    def search(self, query):
        preprocessed_query = preprocess_text(query)
        query_vector = self.vectorizer.transform([preprocessed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        sorted_indices = similarities.argsort()[::-1]
        return [(self.documents[i], similarities[i]) for i in sorted_indices]

    def rocchio_expansion(self, query, relevant_docs, irrelevant_docs, alpha=0.5, beta=0.5, gamma=0.1):
        query_vector = self.vectorizer.transform([preprocess_text(query)]).toarray()[0]
        
        relevant_indices = [self.documents.index(doc) for doc in relevant_docs if doc in self.documents]
        irrelevant_indices = [self.documents.index(doc) for doc in irrelevant_docs if doc in self.documents]
        
        relevant_vectors = self.tfidf_matrix[relevant_indices].toarray()
        irrelevant_vectors = self.tfidf_matrix[irrelevant_indices].toarray()

        centroid_relevant = np.mean(relevant_vectors, axis=0) if len(relevant_vectors) > 0 else np.zeros_like(query_vector)
        centroid_irrelevant = np.mean(irrelevant_vectors, axis=0) if len(irrelevant_vectors) > 0 else np.zeros_like(query_vector)

        expanded_query = alpha * query_vector + beta * centroid_relevant - gamma * centroid_irrelevant
        
        # Normalize the expanded query
        norm = np.linalg.norm(expanded_query)
        if norm > 0:
            expanded_query = expanded_query / norm
        
        expanded_query = np.array(expanded_query)
        
        # Lấy ra top 10 từ có điểm cao nhất 
        feature_names = self.vectorizer.get_feature_names_out()
        top_term_indices = expanded_query.argsort()[-10:][::-1]  # Get indices of top 10 terms
        top_terms = [feature_names[i] for i in top_term_indices]

        # In xem kết quả câu new query
        print("Expanded Query Terms:")
        print(' '.join(top_terms))

        return expanded_query, ' '.join(top_terms)



    def search_with_feedback(self, query, relevant_docs, irrelevant_docs):
        # Bước 1: Mở rộng truy vấn
        expanded_query, expanded_query_terms = self.rocchio_expansion(query, relevant_docs, irrelevant_docs)
        
        # In câu truy vấn mở rộng
        print("Expanded Query Terms:")
        print(expanded_query_terms)
        
        # Kiểm tra và đảm bảo expanded_query là numpy array 1D
        if isinstance(expanded_query, tuple):
            raise TypeError("expanded_query should be a numpy array, but received a tuple.")
        
        if expanded_query.ndim == 2:
            expanded_query = expanded_query.flatten()
        
        # Bước 2: Tính toán sự tương tự
        similarities = cosine_similarity(expanded_query.reshape(1, -1), self.tfidf_matrix).flatten()
        
        # Bước 3: Sắp xếp các tài liệu
        sorted_indices = similarities.argsort()[::-1]
        results = [(self.documents[i], similarities[i]) for i in sorted_indices]
        
        return results
