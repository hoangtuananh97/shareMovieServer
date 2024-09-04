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

- If you encounter database-related issues, ensure that the `shareytb.db` file has the correct permissions.
- For S3 upload failures, verify your AWS credentials and bucket configurations.
- If WebSocket connections fail, check your firewall settings and ensure the port is open.

For more detailed information on the API endpoints and their usage, refer to the Swagger documentation at `/docs` when the application is running.