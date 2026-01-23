### Run locally
> uvicorn main:app --host 0.0.0.0 --port 8000

### Build Docker image
> docker build -t fast-api-tutorial:1.0 .

### Run docker image
> docker run --name fast-api-tutorial -p 8000:8000 fast-api-tutorial:1.0

### Remove docker container
> docker container rm e106980b5830

### Deploying in K8s cluster
> kubectl apply -f quartz-scheduler-deployment.yml

### Undeploying
> kubectl delete -f quartz-scheduler-deployment.yml
> 
### Checkout the code

> git clone git@github.com-personal:semika/quartz-on-k8s.git

### Sharing code into git

.gitignore file should be as follows.

```
/.venv/*
.venv
__pycache__/

```

When you switch between two git accounts, you can set the origin URL as follows 

> git remote set-url origin git@github.com-personal:semika/aws-cognito.git

> git push origin master

### References
1. Python client library

   https://docs.opensearch.org/latest/clients/python-low-level/

2. Open search Symentic search tutorial

   https://docs.opensearch.org/latest/vector-search/ai-search/semantic-search/#manual-setup

3. How to create a vector index

   https://docs.opensearch.org/latest/vector-search/creating-vector-index/

4. How to prepare embeddings (vector) in open search

   https://docs.opensearch.org/latest/vector-search/getting-started/vector-search-options/

5. KNN query API documentation

   https://docs.opensearch.org/latest/query-dsl/specialized/k-nn/index/

6. Developer guide

   https://github.com/opensearch-project/opensearch-py/blob/main/guides/index_lifecycle.md

7. How to set an index analyzer when creating an index.

   https://docs.opensearch.org/latest/analyzers/index-analyzers/

   When creating index mappings, you can supply the analyzer parameter for each text field. For example, the following request specifies the simple analyzer for the text_entry field:

   ```json
   PUT testindex
   {
      "mappings": {
         "properties": {
            "brand_name": {
            "type": "text",
            "analyzer": "autocomplete_index"
            }
         }
      },
      "settings": {
                "index": {
                    //....
                    "analysis": {
                        "filter": {
                            "edge_ngram_filter": {
                                "type": "edge_ngram",
                                "min_gram": "2",
                                "max_gram": "15"
                            }
                        },
                        "analyzer": {
                            "autocomplete_index": {
                                "filter": [
                                    "lowercase",
                                    "asciifolding",
                                    "edge_ngram_filter"
                                ],
                                "type": "custom",
                                "tokenizer": "standard"
                            }
                        }
                    }
                    // ......
                }
   }
   ```
8. Complete API documentation

   https://docs.opensearch.org/latest/api-reference/analyze-apis/
   
   