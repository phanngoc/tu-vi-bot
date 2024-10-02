from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
from llama_index.core.node_parser import (
    SemanticDoubleMergingSplitterNodeParser,
    LanguageConfig,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
import chromadb
import json
from llama_index.core import SimpleDirectoryReader
import os
import spacy
from typing import Dict, List
import pickle

# Load the Vietnamese spaCy model
nlp = spacy.load('vi_core_news_lg')

documents = SimpleDirectoryReader(input_dir="./data").load_data()

LANGUAGE_MODELS: Dict[str, List[str]] = {
    "english": ["en_core_web_md", "en_core_web_lg"],
    "german": ["de_core_news_md", "de_core_news_lg"],
    "spanish": ["es_core_news_md", "es_core_news_lg"],
    "vietnamese": ["vi_core_news_lg"],  # Add Vietnamese language models
}

class VietnameseLanguageConfig(LanguageConfig):
    def __init__(
        self,
        language: str = "english",
        spacy_model: str = "en_core_web_md",
        model_validation: bool = True,
    ):
        if language not in LANGUAGE_MODELS:
            raise ValueError(
                f"{language} language is not supported yet! Available languages: {list(LANGUAGE_MODELS.keys())}"
            )
        self.language = language
        self.spacy_model = spacy_model
        self.model_validation = model_validation
        if self.model_validation:
            self.validate_model()

    def validate_model(self):
        if self.spacy_model not in LANGUAGE_MODELS[self.language]:
            raise ValueError(
                f"{self.spacy_model} is not a valid model for {self.language}. Available models: {LANGUAGE_MODELS[self.language]}"
            )

config = VietnameseLanguageConfig(language="vietnamese", spacy_model="vi_core_news_lg")

splitter = SemanticDoubleMergingSplitterNodeParser(
    language_config=config,
    initial_threshold=0.4,
    appending_threshold=0.5,
    merging_threshold=0.5,
    max_chunk_size=5000,
)

nodes = splitter.get_nodes_from_documents(documents)
print(len(nodes))

results = []
for node in nodes:
    results.append({"info": node.get_node_info(), "text": node.get_content()})

# Step 6: Save chunks to a JSON file
with open("./output/chunks.json", "w") as outfile:
    json.dump(results, outfile, indent=2)


# Save nodes to disk
with open('./nodes.pkl', 'wb') as f:
    pickle.dump(nodes, f)

# vector_index = VectorStoreIndex(nodes)
# query_engine = vector_index.as_query_engine()


# db = chromadb.PersistentClient(path="./chroma_db")
# chroma_collection = db.get_or_create_collection("tu-vi")
# vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
# storage_context = StorageContext.from_defaults(vector_store=vector_store)

# # define embedding function
# embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

# index = VectorStoreIndex.from_documents(
#     documents, storage_context=storage_context, embed_model=embed_model
# )