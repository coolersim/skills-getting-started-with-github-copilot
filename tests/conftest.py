from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    original_state = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_state)


@pytest.fixture
def activity_name():
    return "Chess Club"


@pytest.fixture
def encoded_activity_name(activity_name):
    return quote(activity_name, safe="")


@pytest.fixture
def existing_participant_email(activity_name):
    return activities[activity_name]["participants"][0]
