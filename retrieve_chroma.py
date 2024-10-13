from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from lunarcalendar import Converter, Solar
from datetime import datetime

import os
from dotenv import load_dotenv
import chromadb
from llama_index.core import Settings

MODEL_NAME = "gpt-4o-mini"
MODEL_EMBEDDING_NAME = "text-embedding-3-small"

load_dotenv()  # take environment variables from .env.
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

embed_model = OpenAIEmbedding(model=MODEL_EMBEDDING_NAME, dimensions=1536)
llm = OpenAI(model=MODEL_NAME)

Settings.embed_model = embed_model

# Load from disk
db2 = chromadb.PersistentClient(path="./chroma_db")
chroma_collection = db2.get_or_create_collection("tuvi_index")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Create index from vector store
index = VectorStoreIndex.from_vector_store(
    vector_store,
    embed_model=embed_model,
)


# Create query engine
query_engine = index.as_query_engine()
