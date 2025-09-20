import hashlib
from langchain_core.caches import BaseCache
from gptcache import Cache
from gptcache.adapter.api import init_similar_cache, manager_factory
from langchain_community.cache import GPTCache
from gptcache.similarity_evaluation import SearchDistanceEvaluation
from gptcache.embedding.huggingface import Huggingface
from gptcache.processor.pre import get_prompt
import app.core.config as cfg
from transformers import AutoConfig

def get_hashed_name(name: str):
    return hashlib.sha256(name.encode()).hexdigest()

def init_gptcache(cache_obj: Cache, llm: str) -> None:
    """
    Initialize GPTCache with ChromaDB + HuggingFace embeddings.

    Args:
        cache_obj (Cache): GPTCache instance
        llm (str): LLM identifier (used to namespace cache)
    """
    hashed_llm = get_hashed_name(llm)
    model_name = cfg.EMBEDDING_MODEL
    
    # HuggingFace embedding model
    embedding = Huggingface(model=model_name)

    # Chroma as vector store backend
    manager = manager_factory(
        "sqlite,chromadb",
        data_dir=f"similar_cache_{hashed_llm}",
        vector_params={"dimension": 384, 'host': cfg.CHROMA_HOST, 'port': cfg.CHROMA_PORT},
    )

    cache_obj.init(
        pre_embedding_func=get_prompt,
        embedding_func=embedding.to_embeddings,
        data_manager=manager,
        similarity_evaluation=SearchDistanceEvaluation(),
        
    )

def get_cache() -> BaseCache:
    return GPTCache(init_gptcache)