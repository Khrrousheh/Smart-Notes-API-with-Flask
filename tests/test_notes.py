# tests/test_notes.py

def test_create_note(client):
    response = client.post("/notes", json={
        "title": "Flask Test",
        "content": "Testing note creation",
        "tags": ["flask", "Test"]
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data


def test_get_notes(client):
    client.post("/notes", json={"title": "Sample 1", "tags": ["work"]})
    client.post("/notes", json={"title": "Sample 2", "tags": ["personal"]})

    response = client.get("/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_search_notes(client):
    client.post("/notes", json={"title": "Unique Search Term", "content": "sample"})
    response = client.get("/notes?search=Unique")
    data = response.get_json()
    assert any("Unique Search Term" in n["title"] for n in data)


def test_tag_filter(client):
    client.post("/notes", json={"title": "Filterable", "tags": ["projectx"]})
    response = client.get("/notes?tag=projectx")
    data = response.get_json()
    assert all("Projectx" in [t.capitalize() for t in n["tags"]] for n in data)


def test_update_note(client):
    create_res = client.post("/notes", json={"title": "To Update", "tags": ["old"]})
    note_id = create_res.get_json()["id"]

    update_res = client.put(f"/notes/{note_id}", json={
        "title": "Updated Title",
        "tags": ["new"]
    })

    assert update_res.status_code == 200
    get_res = client.get(f"/notes/{note_id}")
    updated_note = get_res.get_json()
    assert updated_note["title"] == "Updated Title"
    assert "new" in updated_note["tags"]


def test_delete_note(client):
    res = client.post("/notes", json={"title": "To Delete"})
    note_id = res.get_json()["id"]

    del_res = client.delete(f"/notes/{note_id}")
    assert del_res.status_code == 200

    get_res = client.get(f"/notes/{note_id}")
    assert get_res.status_code == 404
