def test_hello_default(test_client):
    res = test_client.get("/")
    assert res.status_code == 200
    assert res.get_data() == b"Hello, World!"


def test_hello_custom(test_client):
    res = test_client.get("/", query_string={"name": "Dave"})
    assert res.status_code == 200
    assert res.get_data() == b"Hello, Dave!"
