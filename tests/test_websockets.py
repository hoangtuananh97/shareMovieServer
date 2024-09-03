def test_websocket_connection(websocket_client):
    with websocket_client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "Connection established"
