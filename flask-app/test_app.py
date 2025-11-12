import pytest
from unittest.mock import patch
from app import app, images


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route_exists(client):
    """Test that the root URL (/) returns a 200 response."""
    response = client.get("/")
    assert response.status_code == 200


@patch("app.render_template")
@patch("app.random.choice")
def test_index_renders_random_image(mock_choice, mock_render_template, client):
    """Test that the index route renders a template with a random image."""
    fake_url = "https://tenor.com/view/cat-smile-happy-happy-cat-smile-cat-gif-18259408098481512759"
    mock_choice.return_value = fake_url

    client.get("/")

    # Check random.choice was called on images list
    mock_choice.assert_called_once_with(images)

    # Check render_template was called with the expected arguments
    mock_render_template.assert_called_once_with("index.html", url=fake_url)


def test_images_list_not_empty():
    """Ensure the images list is not empty and contains valid URLs."""
    assert isinstance(images, list)
    assert len(images) > 0
    assert all(img.startswith("https://") for img in images)


def test_flask_app_config():
    """Confirm that Flask app has the expected basic configuration."""
    assert app.name == "app"
    assert isinstance(app.url_map._rules_by_endpoint, dict)

