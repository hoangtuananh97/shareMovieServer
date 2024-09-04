# ShareYTB - Video Sharing Platform

## Introduction
ShareYTB is a FastAPI-based video sharing platform that allows users to upload, share, and interact with video content. Key features include user authentication, video management, and real-time notifications via WebSockets.

## Prerequisites
- Python 3.11+
- pip
- SQLite
- AWS account (for S3 storage)

## Installation & Configuration

1. Clone the repository:
   ```
   https://github.com/hoangtuananh97/shareMovieServer.git
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add the following configurations:
   ```
   SECRET_KEY=your_secret_key
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_REGION=your_aws_region
   S3_BUCKET=your_s3_bucket_name
   ```

## Database Setup

The application uses SQLite by default. The database will be automatically created when you run the application for the first time.

## Running the Application

1. Start the development server:
   ```
   uvicorn app.main:app --reload
   ```

2. Access the application at `http://localhost:8000`

3. API documentation is available at `http://localhost:8000/docs`

## Docker Deployment
### Options 1:

1. Build the Docker image:
   ```
   docker build -t shareytb .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 -e SECRET_KEY=your_secret_key -e AWS_ACCESS_KEY_ID=your_aws_access_key -e AWS_SECRET_ACCESS_KEY=your_aws_secret_key -e AWS_REGION=your_aws_region -e S3_BUCKET=your_s3_bucket_name shareytb
   ```
### Options 2:
Only run docker-compose:
   ```
   docker-compose up --build -d
   ```
## Usage

1. Register a new user or log in with existing credentials.
2. Upload videos and images using the `/api/uploads` endpoints.
3. Create, view, update, and delete videos using the `/api/movies` endpoints.
4. Manage user accounts with the `/api/users` endpoints.
5. Connect to the WebSocket at `/ws` for real-time notifications.
6. Upload video using `/api/uploads/video` endpoints
7. Upload image using `/api/uploads/image` endpoints

## Test coverage
### Run testcase
```
pytest
```
Test Coverage: `90%`

## Troubleshooting

### Database Issues
1. If you encounter a "database is locked" error:
   - Ensure that you don't have multiple instances of the application trying to access the database simultaneously.
   - Check if you have proper permissions for the `shareytb.db` file.
   - Try deleting the existing database file and restarting the application to create a new one.

2. If you see "SQLite objects created in a thread can only be used in that same thread" error:
   - This is likely due to the SQLite database being accessed from multiple threads. Ensure that you're using the database connection within the same thread or use a thread-safe database engine.

3. You can move using other database:
   - MongoDB, Mysql, Postgresql,...

### AWS S3 Upload Failures
1. If you encounter S3 upload failures:
   - Double-check your AWS credentials in the `.env` file.
   - Ensure that your AWS IAM user has the necessary permissions to upload to the specified S3 bucket.
   - Verify that the S3 bucket name and region are correct in your configuration.

2. For "Access Denied" errors:
   - Check the bucket policy and ensure it allows uploads from your application.

### WebSocket Connection Issues
1. If WebSocket connections fail:
   - Ensure that your firewall or network settings are not blocking WebSocket connections.
   - Check if the WebSocket URL is correct and matches your server configuration.

2. For "Connection refused" errors:
   - Verify that the WebSocket server is running and listening on the correct port.

### Authentication Problems
1. If you're getting "Unauthorized" errors:
   - Ensure that you're including the JWT token in the Authorization header of your requests.
   - Check if the token has expired. You may need to refresh the token or log in again.

2. For "Invalid token" errors:
   - Verify that the `SECRET_KEY` in your `.env` file matches the one used to generate the token.

### General Troubleshooting Steps
1. Check the application logs for detailed error messages.
2. Ensure all required environment variables are set correctly in your `.env` file.
3. Verify that all dependencies are installed correctly by running `pip install -r requirements.txt`.
4. If running in Docker, try rebuilding the image with `docker-compose build` and then `docker-compose up`.

5. For more detailed information on the API endpoints and their usage, refer to the Swagger documentation at `/docs` when the application is running.


## RUN Client and Server
1. Goto folder parent
2. Create `sh file`. Ex: `run_server.sh`
3. Add permission for `sh file`: ` chmod +x run_server.sh`
4. Add content to file:
```
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Build the Docker images and start the containers
echo "Server: Building Docker images and starting containers..."
docker-compose -f <Folder Server>/docker-compose.yml up --build -d

echo "Client: Building Docker images and starting containers..."
docker-compose -f <Folder Client>/docker-compose.yml up --build -d

# Wait for a few seconds to ensure that services are up and running
echo "Waiting for services to start..."
sleep 5

echo "RUNNING..."
```
5. Run `./run_server.sh`