from fastapi.testclient import TestClient

from app import main


def test_upload_list_ask_and_delete(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "test.db")
    client = TestClient(main.app)
    content = (
        "A motor bearing should be inspected when vibration increases. "
        "Misalignment and worn bearings are common causes of elevated vibration. "
        "Record readings during routine maintenance and compare them with baseline values."
    )
    upload = client.post(
        "/documents/upload",
        files={"file": ("motor-notes.txt", content.encode("utf-8"), "text/plain")},
    )
    assert upload.status_code == 200
    assert upload.json()["source"] == "motor-notes.txt"

    docs = client.get("/documents")
    assert docs.status_code == 200
    assert docs.json()["documents"][0]["source"] == "motor-notes.txt"

    answer = client.post("/ask", json={"question": "What causes elevated vibration?"})
    assert answer.status_code == 200
    assert answer.json()["sources"]
    assert answer.json()["sources"][0]["title"] == "motor-notes.txt"

    deleted = client.delete("/documents/motor-notes.txt")
    assert deleted.status_code == 200
    assert client.get("/documents").json()["documents"] == []


def test_upload_rejects_unsupported_file(tmp_path, monkeypatch):
    monkeypatch.setattr(main, "DB_PATH", tmp_path / "test.db")
    client = TestClient(main.app)
    response = client.post(
        "/documents/upload",
        files={"file": ("manual.pdf", b"not a pdf", "application/pdf")},
    )
    assert response.status_code == 415


def test_home_serves_web_app():
    response = TestClient(main.app).get("/")
    assert response.status_code == 200
    assert "Knowledge Desk" in response.text
