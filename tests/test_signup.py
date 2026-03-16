from urllib.parse import quote


def test_signup_adds_new_participant(client, activity_name, encoded_activity_name):
    email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_email(
    client, activity_name, encoded_activity_name, existing_participant_email
):
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": existing_participant_email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_returns_404_for_unknown_activity(client):
    unknown_activity = quote("Unknown Activity", safe="")

    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
