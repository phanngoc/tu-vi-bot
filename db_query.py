import chromadb
import os
from llama_index.embeddings.openai import OpenAIEmbedding

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=1536)

db = chromadb.PersistentClient(path="./chroma_db")

# Assuming you're using a custom embedding model
def embed_text(text):
    # Your custom embedding logic here, ensuring that the embedding dimension is 1536
    return embed_model(text)

collection = db.get_or_create_collection("tu-vi")
results = collection.query(
    query_embeddings=[],
)

print(results)

# db.delete_collection(name="tu-vi")

# switch `add` to `upsert` to avoid adding the same documents every time
# collection.upsert(
#     documents=[
#         "This is a document about pineapple",
#         "This is a document about oranges"
#     ],
#     ids=["id1", "id2"]
# )

