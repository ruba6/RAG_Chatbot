from flask import Flask, request, jsonify
from flask import render_template
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os
from groq import Groq
import time


api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

app = Flask(__name__)

# Paths
CHROMA_PATH = "chroma_db"
DATA_PATH = "data"

# Embeddings + Vector DB
embeddings_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name="example_collections",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

retriever = vector_store.as_retriever(search_kwargs={'k': 5})

# LLM Client
# client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")

# CHAT API (IMPORTANT)
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message")

        print("User:", message)

        # Retrieve docs
        docs = retriever.invoke(message)
        print("Docs:", len(docs))

        if not docs:
            # return jsonify({"response": "No data found. Upload a PDF first."})
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": message
                    }
                ],
            )

            answer = response.choices[0].message.content

            return jsonify({"response": answer})

        # Limit size (VERY IMPORTANT)
        knowledge = "\n\n".join([doc.page_content[:300] for doc in docs[:2]])

        prompt = f"""
        Answer based only on this knowledge:

        {knowledge}

        Question: {message}
        """

        # LLM call
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
        )

        answer = response.choices[0].message.content

        return jsonify({"response": answer})

    except Exception as e:
        print("CHAT ERROR:", str(e))
        return jsonify({"response": "Error generating response"}), 500

@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files["file"]

    if file.filename == "":
        return {"error": "No file"}, 400
        
    DATA_PATH = "data"
    os.makedirs(DATA_PATH, exist_ok=True)

    file_path = os.path.join(DATA_PATH, file.filename)
    
    file.save(file_path)

    #Run ingestion ONLY for this file
    from database_ingest import ingest_single_file
    ingest_single_file(file_path)

    return {"message": "File uploaded and indexed successfully"}

@app.route("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug = True)
