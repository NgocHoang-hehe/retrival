from flask_cors import CORS
from flask import Flask, request, jsonify, render_template
from SearchSystem import SearchSystem
import json

app = Flask(__name__)
CORS(app)

# Initialize the search system with your documents
# Đọc dữ liệu từ file JSON
with open('documents.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

documents = [doc['content'] for doc in data]
# topics = [doc['topic'] for doc in data]
# urls = [doc['url'] for doc in data]
search_system = SearchSystem(documents)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    if request.is_json:
        data = request.get_json()
        query = data.get('query')
    else:
        query = request.form.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = search_system.search(query)
    return jsonify([{'document': doc, 'score': float(score)} for doc, score in results[:20]])


@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        query = data.get('query')
        relevant_docs = data.get('relevant_docs', [])
        irrelevant_docs = data.get('irrelevant_docs', [])
        # Tạo mảng chứa dữ liệu để tiếp tục xử lý
        relevant_docs_list = []
        irrelevant_docs_list = []

        # Thêm dữ liệu vào mảng relevant_docs_list
        for doc in relevant_docs:
            relevant_docs_list.append(doc)

        # Thêm dữ liệu vào mảng irrelevant_docs_list
        for doc in irrelevant_docs:
            irrelevant_docs_list.append(doc)

        if not query:
            return jsonify({"error": "No query provided"}), 400

        results = search_system.search_with_feedback(query, relevant_docs_list, irrelevant_docs_list)
        return jsonify([{'document': doc, 'score': float(score)} for doc, score in results[:20]])
    except Exception as e:
        print(f"Error in feedback route: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)