from unittest.mock import patch


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_image_jpg(mock_upload, auth_client, sample_image):
    mock_upload.return_value = "images/test_image.jpg"
    files = {"file": ("test_image.jpg", sample_image, "image/jpeg")}
    response = auth_client.post("/api/uploads/image", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Image uploaded successfully'
    assert response_json["url"] == "images/test_image.jpg"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_image_png(mock_upload, auth_client, sample_image):
    mock_upload.return_value = "images/test_image.png"
    files = {"file": ("test_image.png", sample_image, "image/jpeg")}
    response = auth_client.post("/api/uploads/image", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Image uploaded successfully'
    assert response_json["url"] == "images/test_image.png"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_image_jpg(mock_upload, auth_client, sample_image):
    mock_upload.return_value = "images/test_image.gif"
    files = {"file": ("test_image.gif", sample_image, "image/gif")}
    response = auth_client.post("/api/uploads/image", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Image uploaded successfully'
    assert response_json["url"] == "images/test_image.gif"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_image_jpeg(mock_upload, auth_client, sample_image):
    mock_upload.return_value = "images/test_image.jpeg"
    files = {"file": ("test_image.jpeg", sample_image, "image/jpeg")}
    response = auth_client.post("/api/uploads/image", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Image uploaded successfully'
    assert response_json["url"] == "images/test_image.jpeg"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_video_mp4(mock_upload, auth_client, sample_video):
    mock_upload.return_value = "videos/test_video.mp4"
    files = {"file": ("test_video.mp4", sample_video, "video/mp4")}
    response = auth_client.post("/api/uploads/video", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Video uploaded successfully'
    assert response_json["url"] == "videos/test_video.mp4"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_video_avi(mock_upload, auth_client, sample_video):
    mock_upload.return_value = "videos/test_video.avi"
    files = {"file": ("test_video.avi", sample_video, "video/avi")}
    response = auth_client.post("/api/uploads/video", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Video uploaded successfully'
    assert response_json["url"] == "videos/test_video.avi"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_video_mov(mock_upload, auth_client, sample_video):
    mock_upload.return_value = "videos/test_video.mov"
    files = {"file": ("test_video.mov", sample_video, "video/mov")}
    response = auth_client.post("/api/uploads/video", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Video uploaded successfully'
    assert response_json["url"] == "videos/test_video.mov"
    mock_upload.assert_called_once()


@patch('app.api.uploads.upload_file_to_s3')
def test_upload_video_wmv(mock_upload, auth_client, sample_video):
    mock_upload.return_value = "videos/test_video.wmv"
    files = {"file": ("test_video.wmv", sample_video, "video/wmv")}
    response = auth_client.post("/api/uploads/video", files=files)
    assert response.status_code == 200
    response_json = response.json()
    assert "url" in response_json
    assert response_json["message"] == 'Video uploaded successfully'
    assert response_json["url"] == "videos/test_video.wmv"
    mock_upload.assert_called_once()


def test_upload_image_unauthenticated(test_client, sample_image):
    files = {"file": ("test_image.jpg", sample_image, "image/jpeg")}
    response = test_client.post("/api/uploads/image", files=files)
    assert response.status_code == 401


def test_upload_video_unauthenticated(test_client, sample_video):
    files = {"file": ("test_video.mp4", sample_video, "video/mp4")}
    response = test_client.post("/api/uploads/video", files=files)
    assert response.status_code == 401


def test_upload_invalid_image_format(auth_client, sample_image):
    files = {"file": ("test_image.txt", sample_image, "text/plain")}
    response = auth_client.post("/api/uploads/image", files=files)
    assert response.status_code == 400
    assert "Invalid image file format" in response.json()["detail"]


def test_upload_invalid_video_format(auth_client, sample_video):
    files = {"file": ("test_video.txt", sample_video, "text/plain")}
    response = auth_client.post("/api/uploads/video", files=files)
    assert response.status_code == 400
    assert "Invalid video file format" in response.json()["detail"]
