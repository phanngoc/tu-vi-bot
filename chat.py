from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding

import os
from dotenv import load_dotenv
import chromadb
from llama_index.core import Settings

load_dotenv()  # take environment variables from .env.
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=1536)
Settings.embed_model = embed_model

# Load from disk
db2 = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db2.get_or_create_collection("tu-vi")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Create index from vector store
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)

# Create query engine
query_engine = index.as_query_engine()

# Query the index
# response = query_engine.query("các tuổi xông đất tốt ?")
# print(str(response))

# reply from user

def prompt_to_predict(questionMessage = ''):
    response = query_engine.query(questionMessage)
    print(str(response))
    return response

# def prompt_to_predict(questionMessage = ''):
#     system_message = "Hãy nhập ngày sinh của bạn và năm bạn muốn xem."
#     response = query_engine.query("What did the author do growing up?")

#     response = client.beta.chat.completions.parse(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": system_message},
#             {
#                 "role": "user",
#                 "content": [
#                 {
#                     "type": "text",
#                     "text": questionMessage,
#                 },
#             ]
#             },
#         ],
#         max_tokens=300,
#         response_format=MathResponse,
#     )
#     math_response = response.choices[0].message
#     if math_response.parsed:
#         return math_response.to_dict()
#     elif math_response.refusal:
#         return math_response.to_dict()