from flask import Flask, request, jsonify
from flask_cors import CORS

from process import process_files, query_collection, UploadException, allowed_file
import chromadb
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/process', methods=['POST'])
def process():
    documents = request.files.getlist('documents')
    if not documents:
        return jsonify({'error': 'No documents provided'}), 400
    try:
        for file in documents:
            if file and allowed_file(file.filename):
                extension = os.path.splitext(file.filename)[1]
                process_files(extension, file)
            else:
                raise UploadException(f"File type not supported: {file.filename}")
          
        response = {'success': True}
        return jsonify(response)

    except UploadException as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        return jsonify({'error upload': str(e.args)}), 500

@app.route('/query', methods=['GET'])
def query():
    query = request.args.get('text')
    results = query_collection(query)
    return jsonify(results)

@app.route('/refresh', methods=['GET'])
def refresh_db():
    try:
        client = chromadb.PersistentClient()
        client.delete_collection("my_collection")
        response = {'success': True}
    except:
        response = {'success': False}
    return jsonify(response)


@app.route('/health', methods=['GET'])
def health():
    response = {'success': 'Toy on Fayaaaaaaaar'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
