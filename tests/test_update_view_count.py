"""
Tests for update_view_count.py — the script called by GitHub Actions hourly.
"""

import json
import pytest
from update_view_count import update_view_count


@pytest.fixture
def view_file(tmp_path):
    """A temp view_count.json pre-seeded with 50 views."""
    f = tmp_path / "view_count.json"
    f.write_text(json.dumps({"views": 50, "last_updated": "2026-01-01T00:00:00"}))
    return f


# ---------------------------------------------------------------------------
# Increment logic
# ---------------------------------------------------------------------------

class TestIncrement:
    def test_increments_by_one(self, view_file):
        update_view_count(view_count_file=view_file, regenerate=False)
        assert json.loads(view_file.read_text())["views"] == 51

    def test_returns_new_count(self, view_file):
        result = update_view_count(view_count_file=view_file, regenerate=False)
        assert result == 51

    def test_multiple_calls_accumulate(self, view_file):
        for _ in range(5):
            update_view_count(view_count_file=view_file, regenerate=False)
        assert json.loads(view_file.read_text())["views"] == 55

    def test_updates_last_updated_timestamp(self, view_file):
        update_view_count(view_count_file=view_file, regenerate=False)
        data = json.loads(view_file.read_text())
        assert "last_updated" in data
        assert data["last_updated"] != "2026-01-01T00:00:00"


# ---------------------------------------------------------------------------
# File handling edge cases
# ---------------------------------------------------------------------------

class TestFileHandling:
    def test_creates_file_if_missing(self, tmp_path):
        f = tmp_path / "new_count.json"
        assert not f.exists()
        update_view_count(view_count_file=f, regenerate=False)
        assert f.exists()

    def test_starts_from_150_when_file_missing(self, tmp_path):
        f = tmp_path / "new_count.json"
        result = update_view_count(view_count_file=f, regenerate=False)
        assert result == 151  # default 150 + 1

    def test_recovers_from_corrupt_file(self, tmp_path):
        f = tmp_path / "bad.json"
        f.write_text("corrupted data {{{")
        result = update_view_count(view_count_file=f, regenerate=False)
        assert result == 151  # falls back to 150 default + 1

    def test_writes_valid_json(self, view_file):
        update_view_count(view_count_file=view_file, regenerate=False)
        data = json.loads(view_file.read_text())
        assert isinstance(data["views"], int)
        assert isinstance(data["last_updated"], str)
