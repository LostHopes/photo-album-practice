def test_not_found_page(client):
    response = client.get("/bob/")
    assert "Error 404" in response.get_data(as_text=True)
