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

3. If someone intentionally upload videos or upload images multiple times. This leads to security and data redundancy issues. So we have some solution
   1. Use File Hashing for Duplicate Detection
      - **Solution**: Generate a unique hash for each uploaded file (videos or images) using a cryptographic hash function like MD5, SHA-256, etc. Before saving a file, compare its hash with the existing file hashes in your database.
      - **How it works**:
        1. When a user uploads a file, compute the hash of the file.
        2. Check if the hash already exists in the database.
        3. If the hash exists, reject the upload as a duplicate; otherwise, allow the upload and store the hash.
      - **Pros**: Prevents data duplication and reduces storage usage.
      - **Cons**: Hashing large files may slightly increase processing time, but it's effective for duplicate detection.
   2. Set Upload Limits for Users
      - **Solution**: Implement a rate-limiting system that restricts the number of uploads a user can perform within a specific time period (e.g., no more than 5 uploads per hour).
      - **How it works**:
        1. Track the number of uploads per user within a certain time window (using Redis or a database).
        2. If a user exceeds the limit, block further uploads until the time window resets.
      - **Pros**: Prevents spam uploads and reduces the risk of malicious behavior.
      - **Cons**: Might frustrate users who need to upload multiple legitimate files in a short period
   3. Validate File Type and Size
      - **Solution**: Implement strict file type and size validation to prevent malicious uploads (e.g., someone uploading a large file multiple times to exhaust resources).
      - **How it works**:
        1. Before processing the upload, check the MIME type and ensure it matches the allowed types (e.g., images or videos).
        2. Set a maximum file size limit (e.g., no more than 50 MB for images, 500 MB for videos).
      - **Pros**: Improves security by restricting uploads to valid file types and sizes.
      - **Cons**: Might require manual updating of allowed types or sizes depending on the application’s use case.
   4. Implement User Reputation or Trust System
      - **Solution**: Use a reputation system to track user behavior and determine if they frequently upload duplicates or spam content.
      - **How it works**:
        1. Track user activities (e.g., number of uploads, duplicate uploads, etc.).
        2. If a user repeatedly uploads duplicates, flag their account and reduce their upload privileges (e.g., limit their daily upload quota).
      - **Pros**: Allows good users to upload freely while restricting users with suspicious behavior.
      - **Cons**: Requires monitoring and scoring algorithms.

**Additional Security Measures**:
- **CAPTCHA for Uploads**: Implement CAPTCHA to prevent automated bots from spamming your upload endpoints.
- **IP Rate Limiting**: Set IP-based rate limits to prevent mass uploads from a single IP address.
- **Audit Logs**: Keep an audit log of uploads to track suspicious behavior and identify malicious users.
      - 
### WebSocket Connection Issues
1. If WebSocket connections fail:
   - Ensure that your firewall or network settings are not blocking WebSocket connections.
   - Check if the WebSocket URL is correct and matches your server configuration. use `wss://` instead of `ws://`

2. For "Connection refused" errors:
   - Verify that the WebSocket server is running and listening on the correct port and firewall settings.

3. Lack of Message Acknowledgment and Handling of Failures
   - For critical messages, implement an acknowledgment mechanism. The server should send a confirmation that it received a message, and if the client doesn’t receive it within a timeout period, the message should be resent.

### Authentication Problems
1. If you're getting "Unauthorized" errors:
   - Ensure that you're including the JWT token in the Authorization header of your requests.
   - Check if the token has expired. You may need to refresh the token or log in again.

2. For "Invalid token" errors:
   - Verify that the `SECRET_KEY` in your `.env` file matches the one used to generate the token.
3. For **Authentication** websocket. Some solution
   1. Use wss:// for Secure WebSocket Connections
   - **Solution**: Always use `wss://` (WebSocket Secure) instead of ws:// to encrypt WebSocket traffic using SSL/TLS.
   - How it works:
     - `wss://` encrypts the communication between the client and the server, ensuring that no one can intercept or tamper with the messages being exchanged.
   - **Pros**: Protects against `man-in-the-middle` (MITM) attacks, ensures confidentiality, and prevents eavesdropping.
   - **Implementation**:
     - Obtain an SSL certificate for your domain and configure your WebSocket server to use TLS.
     - If using NGINX or Apache as `a reverse proxy`, ensure WebSocket traffic is properly proxied with SSL termination.
     
   2. Authenticate WebSocket Connections
   - **Solution**: Implement authentication before establishing WebSocket connections to ensure only authorized users can access the WebSocket service.
   - **How it works**:
     - Use `JWT tokens`, `API keys`, or `OAuth tokens` to authenticate the user during the WebSocket handshake.
     - Validate the token on the server side before allowing WebSocket communication.
   - **Pros**: Ensures that only authenticated users can initiate WebSocket communication, preventing unauthorized access.
   - **Implementation**:
     - Include the `JWT token` or API key in the WebSocket connection request header or query string.
     - Validate the token on the server side during the WebSocket handshake.

   3. Use Origin and Host Header Validation
      - **Solution**: Validate the Origin and Host headers to ensure WebSocket connections are coming from trusted sources.
      - **How it works**:
        - During the WebSocket handshake, check the Origin header to verify that the request is coming from a trusted domain.
        - Reject any requests with untrusted or missing origin headers.
      - **Pros**: Prevents `Cross-Site WebSocket Hijacking` (CSWSH) and ensures that connections are only established from legitimate clients.
      - **Implementation**:
        - Validate the `Origin` header during the WebSocket handshake in the server-side logic.

   4. Implement Rate Limiting
      - **Solution**: Implement rate limiting to prevent abuse or denial-of-service (DoS) attacks on the WebSocket endpoint.
      - **How it works**:
        - Limit the number of WebSocket connection attempts and messages sent within a specific time window from the same IP address or user.
      - **Pros**: Protects against brute-force attacks, spamming, and resource exhaustion due to excessive WebSocket connections or messages.
      - **Implementation**:
        - Use a rate-limiting service like Redis or tools like Nginx or AWS API Gateway to throttle connections and messages.
   
   5. Encrypt WebSocket Messages
      - **Solution**: Encrypt sensitive data within the WebSocket messages to ensure that even if the connection is intercepted, the data cannot be read.
      - **How it works:**:
        - Use client-side encryption (e.g., AES) to encrypt messages before sending them through the WebSocket connection.
        - Decrypt the messages server-side after they are received.
      - **Pros**: Adds an extra layer of security, especially if sensitive information (e.g., financial data) is being transmitted.
      - **Implementation**:
        - Use `symmetric encryption` (e.g., AES) or public-key encryption (RSA) to encrypt the WebSocket messages.

### General Troubleshooting Steps
1. Check the application logs for detailed error messages.
2. Ensure all required environment variables are set correctly in your `.env` file.
3. Verify that all dependencies are installed correctly by running `pip install -r requirements.txt`.
4. If running in Docker, try rebuilding the image with `docker-compose build` and then `docker-compose up`.

5. For more detailed information on the API endpoints and their usage, refer to the Swagger documentation at `/docs` when the application is running.

### Microservices Architecture: Updated Solutions (In this project):
1. WebSocket Connections Fail:
   - Ensure that your API Gateway (e.g.AWS API Gateway) or load balancer supports WebSocket traffic. Proper routing and session stickiness need to be configured.
   - If using Kubernetes, ensure WebSocket connections are correctly routed using Ingress Controllers (e.g., NGINX) that support WebSocket upgrades.
2. Lack of Message Acknowledgment and Handling of Failures:
   - Implement message acknowledgment using reliable messaging systems like Kafka or RabbitMQ in microservices. Use message queues to buffer WebSocket messages in case of a failure or downtime.
   - Use retry mechanisms at both client and server levels to resend messages in case of transmission failure.
3. Database Issues in Microservices:
 - "Database is locked" error:
   - Each service should use its own isolated database following the Database-per-Service pattern. This avoids issues like database locking by eliminating shared databases between services.
 - This project use SQLite. SQLite objects created in a thread can only be used in that same thread:
   - Move to a production-grade database like PostgreSQL or MySQL, which handle concurrent connections and are thread-safe.
   - Move to a more scalable database: AWS RDS, MongoDB Atlas. Use database replication and sharding
4. AWS S3 Upload Failures in Microservices:
   - Use S3 Event Notifications to trigger background jobs (via AWS Lambda or another service) when uploads complete.

## RUN Client and Server same time
1. Goto folder parent have code server and code client
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
