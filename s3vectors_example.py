import boto3 
import json 
import os
import sys

# コマンドライン引数をハイフン付きで受け入れる
bucket_name = None
index_name = None

args = sys.argv[1:]

# 引数が3つ未満ならエラー
if len(args) < 2:
    print("Usage: python s3vectors_example.py --bucket <bucket_name> --index <index_name>")
    print("または環境変数 S3_VECTOR_BUCKET, S3_VECTOR_INDEX を設定してください。")
    sys.exit(1)

# ハイフン付き引数のパース
for i in range(len(args)):
    if args[i] == "--bucket" and i + 1 < len(args):
        bucket_name = args[i + 1]
    if args[i] == "--index" and i + 1 < len(args):
        index_name = args[i + 1]

# 環境変数 fallback
if not bucket_name:
    bucket_name = os.environ.get("S3_VECTOR_BUCKET")
if not index_name:
    index_name = os.environ.get("S3_VECTOR_INDEX")

# どちらかでも未設定ならエラー
if not bucket_name or not index_name:
    print("Error: bucket_nameとindex_nameは必須です。コマンドライン引数または環境変数で指定してください。")
    sys.exit(1)

# 以降は bucket_name, index_name をそのまま使う

# Create a Bedrock Runtime client in the AWS Region of your choice. 
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2") 

# The text strings to convert to embeddings.
texts = [
"Star Wars: A farm boy joins rebels to fight an evil empire in space", 
"Jurassic Park: Scientists create dinosaurs in a theme park that goes wrong",
"Finding Nemo: A father fish searches the ocean to find his lost son"]

embeddings=[]
#Generate vector embeddings for the input texts
for text in texts:
        body = json.dumps({
            "inputText": text
        })    
        # Call Bedrock's embedding API
        response = bedrock.invoke_model(
        modelId='amazon.titan-embed-text-v2:0',  # Titan embedding model 
        body=body)   
        # Parse response
        response_body = json.loads(response['body'].read())
        embedding = response_body['embedding']
        embeddings.append(embedding)

# Print results
for i, (text, embedding) in enumerate(zip(texts, embeddings)):
    print(f"Text {i+1}: {text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 5 elements: {embedding[:5]}")
    print()


# Create S3Vectors client
s3vectors = boto3.client('s3vectors', region_name='us-west-2')

# Insert vector embedding
s3vectors.put_vectors( vectorBucketName=bucket_name,
  indexName=index_name,
  vectors=[
{"key": "v1", "data": {"float32": embeddings[0]}, "metadata": {"id": "key1", "source_text": texts[0], "genre":"scifi"}},
{"key": "v2", "data": {"float32": embeddings[1]}, "metadata": {"id": "key2", "source_text": texts[1], "genre":"scifi"}},
{"key": "v3", "data": {"float32": embeddings[2]}, "metadata": {"id": "key3", "source_text":  texts[2], "genre":"family"}}
],
)

#Create an embedding for your query input text
# The text to convert to an embedding.
input_text = "List the movies about adventures in space"

# Create the JSON request for the model.
request = json.dumps({"inputText": input_text})

# Invoke the model with the request and the model ID, e.g., Titan Text Embeddings V2. 
response = bedrock.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=request)

# Decode the model's native response body.
model_response = json.loads(response["body"].read())

# Extract and print the generated embedding and the input text token count.
embedding = model_response["embedding"]

# Performa a similarity query. You can also optionally use a filter in your query
query = s3vectors.query_vectors( vectorBucketName=bucket_name,
  indexName=index_name,
  queryVector={"float32":embedding},
  topK=3, 
  filter={"genre":"scifi"},
  returnDistance=True,
  returnMetadata=True
  )
results = query["vectors"]
print(results)
