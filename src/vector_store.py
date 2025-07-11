from dotenv import load_dotenv

from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from config.config import settings

load_dotenv()

client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, api_key=settings.QDRANT_API_KEY)
embeddings = OpenAIEmbeddings()

def get_vector_store():
    return Qdrant(client=client, collection_name="danson", embeddings=embeddings)
