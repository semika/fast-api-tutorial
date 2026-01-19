from fastapi import FastAPI
from typing import Dict, Any, List
from pydantic import BaseModel
from config import settings
import boto3
import json
import logging
from opensearchpy import OpenSearch

logger = logging.getLogger(__name__)

# OpenSearch client setup
auth = (settings.opensearch_user, settings.opensearch_password) # For testing only. Don't store credentials in code.

open_search_client = OpenSearch(
    hosts=[{"host": settings.opensearch_host, "port": 443}],
    http_auth=auth,
    http_compress=True,  # enables gzip compression for request bodies
    use_ssl=True,
    verify_certs=True,
    ssl_assert_hostname=False,
    ssl_show_warn=False,
)


# Initialize AWS Bedrock client for Claude
bedrock_runtime = None
if settings.aws_region:
    _bedrock_kwargs = {
        'service_name': 'bedrock-runtime',
        'region_name': settings.aws_region
    }
    _ak = settings.aws_access_key_id
    _sk = settings.aws_secret_access_key
    _st = settings.aws_session_token
    if _ak and _sk:
        _bedrock_kwargs['aws_access_key_id'] = _ak
        _bedrock_kwargs['aws_secret_access_key'] = _sk
        if _st:
            _bedrock_kwargs['aws_session_token'] = _st
    bedrock_runtime = boto3.client(**_bedrock_kwargs)

class OpenSearchRequest(BaseModel):
    query: str
    filters: Dict[str, Any]
    size: int

class OpenSearchResponse(BaseModel):
    output: Dict[str, Any]

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/open-search")
async def open_search(request: OpenSearchRequest) -> OpenSearchResponse:

    """
    Handle cannabis product search with faceted search.
    
    Expected JSON payload:
    {
        "query": "I need something for anxiety",
        "filters": {
            "brand": ["Brand1", "Brand2"],
            "product_type": ["Edibles"],
            "effects": ["RELAXATION"],
            "price_range": "20-50"
        },
        "size": 10
    }
    """
     
    user_query = request.query.strip()
    if not user_query:
        return OpenSearchResponse(output = {'error': 'Query is required', 'status' : 400 })
    
    filters = request.filters;
    result_size = request.size;

     # Generate embedding and search
    query_embedding = get_text_embedding_bedrock(user_query)
    
    # Here you would add the logic to interact with OpenSearch
    # For demonstration, we will just echo back the input data
    # Perform the search
    
    #q = 'cherry'
    query = {
    'size': 5,
    'query': {
        'multi_match': {
        'query': user_query,
        'fields': ['title^2', 'director']
        }
    }
    }

    response = open_search_client.search(
        body = query,
        index = 'products-mg'
    )

    output_data = {"query_embedding": response}
    return OpenSearchResponse(output=output_data)

def get_text_embedding_bedrock(text: str) -> List[float]:
    """
    Generate a text embedding using AWS Bedrock Titan Text Embeddings v2.
    
    Args:
        text: Input text to embed.
        
    Returns:
        List[float]: Embedding vector.
    """
    if not bedrock_runtime:
        raise RuntimeError("Bedrock runtime client is not configured")

    try:
        body = json.dumps({"inputText": text})
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=body
        )
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding")
        
        if embedding is None:
            embeddings = response_body.get("embeddings")
            if isinstance(embeddings, list) and embeddings:
                first = embeddings[0]
                embedding = first.get("embedding") if isinstance(first, dict) else None

        if not embedding:
            raise ValueError("No embedding returned from Titan model response")

        return embedding
    except Exception as e:
        logger.error(f"Failed to get Titan embedding: {e}")
        raise