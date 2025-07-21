# S3 Vector Client

This project is a client application that integrates AWS S3 with a vector database. It vectorizes data stored in S3 and enables similarity and semantic search.

---

## Specification

- **Purpose**  
  This sample script generates text embeddings using Amazon Bedrock and registers them in S3 Vectors, then performs vector (similarity) search.

- **Main Features**
  1. Generate vector embeddings from text using Bedrock Titan Text Embeddings V2
  2. Register vectors and metadata to an index using S3 Vectors `put_vectors`
  3. Perform similarity search using S3 Vectors `query_vectors`
  4. Specify bucket name and index name via command-line arguments or environment variables (no default, required)

- **Required AWS Services**
  - Amazon Bedrock
  - S3 Vectors (supported in boto3 from July 2025)

- **Required Permissions**
  - `bedrock:InvokeModel`
  - `s3vectors:PutVectors`
  - `s3vectors:QueryVectors`

---

## Usage

### 1. Prerequisites

- Python 3.8 or later
- Latest boto3 (1.39.x or later)
- AWS credentials configured (e.g., via `aws configure`)
- Required IAM permissions

### 2. Installation

```bash
pip install --upgrade boto3
```

### 3. How to Run

#### Using command-line arguments

```bash
python s3vectors_example.py --bucket <bucket_name> --index <index_name>
```

Example:
```bash
python s3vectors_example.py --bucket my-vector-bucket --index my-index
```

#### Using environment variables

```bash
export S3_VECTOR_BUCKET=my-vector-bucket
export S3_VECTOR_INDEX=my-index
python s3vectors_example.py
```

### 4. Example Input/Output

- Vectorizes three movie descriptions and registers them in S3 Vectors
- Generates a vector for a query text (e.g., "List the movies about adventures in space") and performs similarity search
- Outputs the search results (list of vectors with similarity scores and metadata) to standard output

---

## Notes

- Both bucket name and index name are **required**. The script will exit with an error if not specified.
- S3 Vectors is supported in boto3 from July 2025.
- Using Bedrock and S3 Vectors requires an AWS account with appropriate permissions and, in some cases, service enablement.

---

## References

- [boto3 official documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Amazon S3 Vectors Preview Announcement (What's New)](https://aws.amazon.com/about-aws/whats-new/2025/07/amazon-s3-vectors-preview-native-support-storing-querying-vectors/)
- [Amazon S3 Vectors Features](https://aws.amazon.com/s3/features/vectors/)
- [Amazon S3 Vectors User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors.html)
- [AWS Blog: Introducing Amazon S3 Vectors](https://aws.amazon.com/blogs/aws/introducing-amazon-s3-vectors-first-cloud-storage-with-native-vector-support-at-scale/)
- [Amazon S3 Vectors Getting Started Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-getting-started.html)
- [s3vectors-embed-cli (GitHub)](https://github.com/awslabs/s3vectors-embed-cli)
