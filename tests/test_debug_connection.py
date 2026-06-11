def test_debug_workspace_status(client):
    response = client.get_workspace_status()

    print("Final URL:", response.url)
    print("Status Code:", response.status_code)
    print("Response Body:", response.text)

    assert response.status_code == 200