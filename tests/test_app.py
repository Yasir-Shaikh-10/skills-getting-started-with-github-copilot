from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email():
    # Arrange
    activities["Chess Club"]["participants"] = ["student@example.com", "other@example.com"]

    # Act
    response = client.delete("/activities/Chess Club/participants?email=student@example.com")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered student@example.com from Chess Club"
    assert "student@example.com" not in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_404_when_missing():
    # Arrange
    activities["Chess Club"]["participants"] = ["student@example.com"]

    # Act
    response = client.delete("/activities/Chess Club/participants?email=missing@example.com")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
