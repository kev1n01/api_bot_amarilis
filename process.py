import re
import chromadb

document_id = 1
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md'}

def allowed_file(filename):             
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class UploadException(Exception):
    pass

def process_files(extension, file):  
    client = chromadb.PersistentClient()

    collection = client.get_or_create_collection(name="my_collection")

    if extension == '.txt' or extension == '.md':
        markdown_text = file.read().decode()
        chunks = split_text(markdown_text)
        document_title = get_title(markdown_text)
        generate_embeddings(chunks, document_title, file.filename, collection)
    if(extension == '.pdf'):
        print("pdf aqui no she que achel")
        pass
    

def generate_embeddings(chunks, document_title, file_name, collection):
    global document_id
    for chunk in chunks:
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": file_name
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        document_id = document_id + 1


def get_title(file):
    match = re.search(r"title:\s+(.+)\s+", file)
    if match:
        title = match.group(1)
        return title
    else:
        " "


def split_text(file):
    separator = "\n### "
    return file.split(separator)


def query_collection(query):
    client = chromadb.PersistentClient()

    collection = client.get_or_create_collection(name="my_collection")
    return collection.query(
        query_texts=[query],
        n_results=10,
    )
