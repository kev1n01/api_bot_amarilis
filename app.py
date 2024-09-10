from flask import Flask, request, jsonify
from flask_cors import CORS

from process import process_files, query_collection
import chromadb

app = Flask(__name__)
CORS(app)


@app.route('/process', methods=['POST'])
def process():
    documents = request.files.getlist('documents')
    process_files(documents)
    response = {'success': True}
    return jsonify(response)


@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('text')
    results = query_collection(query)
    return jsonify(results)

@app.route('/refresh', methods=['GET'])
def refresh_db():
    client = chromadb.PersistentClient()
    client.delete_collection("my_collection")
    response = {'success': True}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
