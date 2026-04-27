"""
Tests for Flask routes and view count persistence (app.py).
"""

import json
import pytest
import app as app_module
from app import app, load_view_count, save_view_count


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolate_view_count(tmp_path, monkeypatch):
    """Point VIEW_COUNT_FILE at a temp file and reset the in-memory counter."""
    test_file = tmp_path / "view_count.json"
    test_file.write_text(json.dumps({"views": 10}))
    monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", test_file)
    monkeypatch.setattr(app_module, "page_view_count", 10)
    return test_file


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Route tests
# ---------------------------------------------------------------------------

class TestHomeRoute:
    def test_returns_200(self, client):
        assert client.get("/").status_code == 200

    def test_contains_portfolio_name(self, client):
        assert b"Hariharan Natarajan" in client.get("/").data

    def test_contains_view_count_element(self, client):
        assert b"hero-views" in client.get("/").data


class TestViewsAPI:
    def test_get_returns_200(self, client):
        assert client.get("/api/views").status_code == 200

    def test_get_returns_json(self, client):
        response = client.get("/api/views")
        assert response.content_type == "application/json"

    def test_get_returns_views_key(self, client):
        data = json.loads(client.get("/api/views").data)
        assert "views" in data

    def test_get_returns_integer_count(self, client):
        data = json.loads(client.get("/api/views").data)
        assert isinstance(data["views"], int)

    def test_post_returns_200(self, client):
        assert client.post("/api/views").status_code == 200

    def test_post_increments_by_one(self, client):
        before = json.loads(client.get("/api/views").data)["views"]
        after = json.loads(client.post("/api/views").data)["views"]
        assert after == before + 1

    def test_post_persists_to_file(self, client, isolate_view_count):
        client.post("/api/views")
        saved = json.loads(isolate_view_count.read_text())
        assert saved["views"] == 11  # started at 10

    def test_multiple_posts_increment_correctly(self, client):
        for _ in range(3):
            client.post("/api/views")
        data = json.loads(client.get("/api/views").data)
        assert data["views"] == 13  # started at 10


class TestPortfolioAPI:
    def test_returns_200(self, client):
        assert client.get("/api/portfolio").status_code == 200

    def test_returns_json(self, client):
        assert client.get("/api/portfolio").content_type == "application/json"

    def test_contains_name(self, client):
        data = json.loads(client.get("/api/portfolio").data)
        assert data["name"] == "Hariharan Natarajan"

    def test_contains_required_sections(self, client):
        data = json.loads(client.get("/api/portfolio").data)
        for key in ("experience", "certifications", "expertise", "projects", "services", "contact"):
            assert key in data, f"Missing section: {key}"

    def test_experience_is_non_empty_list(self, client):
        data = json.loads(client.get("/api/portfolio").data)
        assert isinstance(data["experience"], list)
        assert len(data["experience"]) > 0

    def test_certifications_count_matches_data(self, client):
        data = json.loads(client.get("/api/portfolio").data)
        assert len(data["certifications"]) == 20


# ---------------------------------------------------------------------------
# View count persistence unit tests
# ---------------------------------------------------------------------------

class TestLoadViewCount:
    def test_reads_value_from_file(self, tmp_path, monkeypatch):
        f = tmp_path / "vc.json"
        f.write_text(json.dumps({"views": 99}))
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", f)
        assert load_view_count() == 99

    def test_returns_zero_when_file_missing(self, tmp_path, monkeypatch):
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", tmp_path / "missing.json")
        assert load_view_count() == 0

    def test_returns_zero_on_corrupt_json(self, tmp_path, monkeypatch):
        f = tmp_path / "vc.json"
        f.write_text("not valid json {{")
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", f)
        assert load_view_count() == 0

    def test_returns_zero_on_missing_views_key(self, tmp_path, monkeypatch):
        f = tmp_path / "vc.json"
        f.write_text(json.dumps({"other": 5}))
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", f)
        assert load_view_count() == 0


class TestSaveViewCount:
    def test_writes_views_key(self, tmp_path, monkeypatch):
        f = tmp_path / "vc.json"
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", f)
        save_view_count(77)
        assert json.loads(f.read_text())["views"] == 77

    def test_overwrites_existing_value(self, tmp_path, monkeypatch):
        f = tmp_path / "vc.json"
        f.write_text(json.dumps({"views": 1}))
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", f)
        save_view_count(999)
        assert json.loads(f.read_text())["views"] == 999

    def test_roundtrip_save_and_load(self, tmp_path, monkeypatch):
        f = tmp_path / "vc.json"
        monkeypatch.setattr(app_module, "VIEW_COUNT_FILE", f)
        save_view_count(123)
        assert load_view_count() == 123
