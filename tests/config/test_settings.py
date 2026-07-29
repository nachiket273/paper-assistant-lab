from src.config.settings import settings


def test_settings():
    assert settings.chunk_size == 1000
    assert settings.chunk_overlap == 200


def test_settings_env_override(monkeypatch):
    monkeypatch.setenv("PAL_CHUNK_SIZE", "1500")
    monkeypatch.setenv("PAL_CHUNK_OVERLAP", "300")

    # Re-initialize settings to pick up the environment variables
    new_settings = settings.__class__()

    assert new_settings.chunk_size == 1500
    assert new_settings.chunk_overlap == 300


def test_settings_invalid_values(monkeypatch):
    monkeypatch.setenv("PAL_CHUNK_SIZE", "-100")  # Invalid negative value
    monkeypatch.setenv("PAL_CHUNK_OVERLAP", "-50")  # Invalid negative value

    try:
        _ = settings.__class__()
        assert False, "Expected ValueError for invalid settings"
    except ValueError as e:
        assert "chunk_size" in str(e) or "chunk_overlap" in str(e)
