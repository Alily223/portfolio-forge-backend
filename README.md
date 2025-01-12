# FastAPI S3 String Storage API

This project provides a FastAPI application for storing, retrieving, and deleting strings in an AWS S3 bucket. It offers a simple and efficient way to manage string data using S3 as a backend storage solution.

The API is built using FastAPI, a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints. It integrates with AWS S3 using the boto3 library, allowing for seamless interaction with S3 buckets.

Key features of this API include:
- Saving strings to an S3 bucket with a specified key
- Retrieving strings from an S3 bucket using a key
- Deleting strings from an S3 bucket using a key
- Error handling for various S3 operations
- Environment-based configuration using the decouple library

## Repository Structure

```
.
└── main.py
```

- `main.py`: The main entry point of the application. It contains the FastAPI app definition and all the API endpoints.

## Usage Instructions

### Installation

1. Ensure you have Python 3.6+ installed.
2. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```
3. Install the required dependencies:
   ```
   pip install fastapi boto3 python-decouple
   ```

### Configuration

Before running the application, you need to set up the following environment variables:

- `AWS_BUCKET_NAME`: The name of your S3 bucket
- `AWS_REGION`: The AWS region where your S3 bucket is located
- `AWS_ACCESS_KEY`: Your AWS access key
- `AWS_SECRET_KEY`: Your AWS secret key

You can set these variables in a `.env` file in the project root or export them in your shell.

### Running the Application

To run the application, use the following command:

```
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoints

1. Save a string to S3:
   ```
   POST /save?key=<key>&value=<value>
   ```

2. Retrieve a string from S3:
   ```
   GET /retrieve?key=<key>
   ```

3. Delete a string from S3:
   ```
   DELETE /delete?key=<key>
   ```

### Example Usage

Here's an example of how to use the API with curl:

1. Save a string:
   ```
   curl -X POST "http://localhost:8000/save?key=example&value=Hello%20World"
   ```

2. Retrieve a string:
   ```
   curl "http://localhost:8000/retrieve?key=example"
   ```

3. Delete a string:
   ```
   curl -X DELETE "http://localhost:8000/delete?key=example"
   ```

### Error Handling

The API includes error handling for common issues:

- 404 Not Found: Returned when trying to retrieve or delete a non-existent key
- 500 Internal Server Error: Returned for AWS credential configuration issues or other unexpected errors

### Troubleshooting

1. AWS Credential Issues:
   - Problem: You receive a 500 error with the message "AWS credentials are not configured properly."
   - Solution: 
     1. Check that your AWS credentials are correctly set in your environment variables.
     2. Verify that the IAM user or role associated with these credentials has the necessary permissions for S3 operations.
     3. If using a `.env` file, ensure it's in the correct location and formatted properly.

2. S3 Bucket Access Issues:
   - Problem: You receive a 500 error when trying to perform S3 operations.
   - Solution:
     1. Verify that the specified S3 bucket exists in your AWS account.
     2. Check that the bucket is in the correct AWS region as specified in your configuration.
     3. Ensure that your IAM user or role has the necessary permissions to perform actions on this specific bucket.

3. Key Not Found:
   - Problem: You receive a 404 error when trying to retrieve or delete a key.
   - Solution:
     1. Double-check that you're using the correct key in your request.
     2. Verify that the key exists in the S3 bucket using the AWS S3 console or CLI.

For further debugging:
- Enable debug logging in FastAPI by adding `log_level="debug"` to the `FastAPI()` constructor in `main.py`.
- Check the application logs for more detailed error messages and stack traces.
- Use AWS CloudTrail to audit API calls made to your S3 bucket for additional insights into potential issues.

## Data Flow

The application handles data flow through the following steps:

1. The client sends an HTTP request to one of the API endpoints.
2. FastAPI processes the request and extracts the necessary parameters (key and value for save operations).
3. The application uses the boto3 S3 client to interact with the specified S3 bucket.
4. For save operations, the string is uploaded to S3 as an object with the specified key.
5. For retrieve operations, the object is fetched from S3 using the provided key and returned to the client.
6. For delete operations, the object with the specified key is removed from the S3 bucket.
7. The API returns an appropriate response to the client, including success messages or error details.

```
[Client] <-> [FastAPI App] <-> [boto3 S3 Client] <-> [AWS S3 Bucket]
```

Note: Ensure that your network allows outbound connections to AWS S3 endpoints for the application to function correctly.