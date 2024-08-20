from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Ví dụ danh sách stopwords cho tiếng Việt
def load_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return set(f.read().splitlines())

stopwords = load_stopwords('vietnamese-stopwords.txt')

# Ví dụ danh sách các văn bản
# Dữ liệu mẫu (đã tiền xử lý và tách từ)
import numpy as np
from underthesea import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Dữ liệu mẫu (đã tiền xử lý và tách từ)
documents = [
    "Thị trường chứng khoán Việt Nam tăng trưởng mạnh.",
    "Giá dầu tăng khiến nhiều ngành công nghiệp gặp khó khăn.",
    "Công nghệ AI đang phát triển mạnh mẽ trên toàn thế giới."
]

# Truy vấn từ người dùng
query = "Thị trường chứng khoán và công nghệ"

# Bước 1: Tiền xử lý truy vấn
tokens = word_tokenize(query, format='text').split()

filtered_tokens = [token for token in tokens if token not in stopwords]
processed_query = " ".join(filtered_tokens)


print("Từ trong câu query: " + processed_query)
processed_docs = []
for doc in documents:
    # Tách từ
    tokens = word_tokenize(doc, format='text').split()
    # Loại bỏ stopwords
    filtered_tokens = [token for token in tokens if token not in stopwords]
    processed_docs.append(" ".join(filtered_tokens))

# Kiểm tra từ sau khi tách và loại bỏ stopwords
print(f"Từ trong truy vấn: {filtered_tokens}")

# Bước 2: Tính toán vector TF-IDF cho tập dữ liệu và truy vấn
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(processed_docs)
query_vector = vectorizer.transform([processed_query])

# Kiểm tra từ điển được tạo bởi TfidfVectorizer
print(f"Từ vựng trong tài liệu: {vectorizer.get_feature_names_out()}")

# Bước 3: Tính toán độ tương đồng cosine
cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

# Bước 4: Sắp xếp kết quả theo độ tương đồng
most_similar_indices = cosine_similarities.argsort()[::-1]
sorted_similarities = cosine_similarities[most_similar_indices]

print(vectorizer.get_feature_names_out())
print(tfidf_matrix.toarray())
print(query_vector.toarray())
# Hiển thị kết quả
for index in most_similar_indices:
    print(f"Bài báo: {documents[index]} - Độ tương đồng: {sorted_similarities[index]}")

# In các giá trị TF-IDF cho từng từ trong truy vấn và tài liệu
feature_names = vectorizer.get_feature_names_out()
query_tfidf = query_vector.toarray().flatten()
doc_tfidf = tfidf_matrix.toarray()

print("TF-IDF của truy vấn:")
for word, score in zip(feature_names, query_tfidf):
    if score > 0:
        print(f"{word}: {score}")

for i, doc in enumerate(documents):
    print(f"\nTF-IDF của tài liệu {i+1}: {doc}")
    for word, score in zip(feature_names, doc_tfidf[i]):
        if score > 0:
            print(f"{word}: {score}")

