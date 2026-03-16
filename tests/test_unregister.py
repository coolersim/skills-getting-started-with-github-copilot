from urllib.parse import quote


def test_unregister_removes_existing_participant(
    client, activity_name, encoded_activity_name, existing_participant_email
):
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": existing_participant_email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_participant_email} from {activity_name}"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert existing_participant_email not in participants


def test_unregister_returns_404_for_missing_participant(client, encoded_activity_name):
    response = client.delete(
        f"/activities/{encoded_activity_name}/participants",
        params={"email": "missing.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Participant not found in this activity"
    }


def test_unregister_returns_404_for_unknown_activity(client):
    unknown_activity = quote("Unknown Activity", safe="")

    response = client.delete(
        f"/activities/{unknown_activity}/participants",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
