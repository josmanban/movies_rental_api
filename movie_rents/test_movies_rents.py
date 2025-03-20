from fastapi.testclient import TestClient


def test_rent_movies_pass(client: TestClient):
    """
    Test case for successfully renting movies.
    This test verifies that the API endpoint for renting movies works as expected
    when provided with valid input data. It checks the following:
    - The response status code is 200 (OK).
    - The returned client ID matches the input client ID.
    - The number of rented movie details matches the input.
    - The rental is marked as not closed (`is_closed` is False).
    - The `closed_datetime` field is None, indicating the rental is still open.
    Args:
        client (TestClient): The test client used to simulate API requests.
    """

    response = client.post(
        "/movie_rents",
        json={"client_id": 1, "details": [{"movie_copy_id": 2}, {"movie_copy_id": 11}]},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["client_id"] == 1
    assert len(data["details"]) == 2
    assert data["is_closed"] is False
    assert data["closed_datetime"] is None


def test_rent_movies_update_pass(client: TestClient):
    """
    Test the update functionality of the movie rental system.
    This test verifies that a movie rental can be successfully updated by adding
    additional movie copies to the rental details.
    Steps:
    1. Create a new movie rental using a POST request with initial rental details.
    2. Update the created rental using a PUT request to include an additional movie copy.
    3. Assert that the response status code is 200 for both requests.
    4. Assert that the updated rental contains the correct number of movie copies.
    Args:
        client (TestClient): The test client used to simulate API requests.
    """

    response = client.post(
        "/movie_rents",
        json={"client_id": 1, "details": [{"movie_copy_id": 2}, {"movie_copy_id": 11}]},
    )
    data = response.json()
    assert response.status_code == 200

    response = client.put(
        f"/movie_rents/{data['id']}",
        json={
            "client_id": 1,
            "details": [
                {"movie_copy_id": 2},
                {"movie_copy_id": 11},
                {"movie_copy_id": 12},
            ],
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data["details"]) == 3


def test_close_movie_rent_pass(client: TestClient):
    """
    Test the successful closure of a movie rent.
    This test simulates the process of creating a movie rent and then closing it.
    It verifies that the API endpoints for creating and closing a movie rent work
    as expected, and ensures the rent is marked as closed with a valid closure timestamp.
    Steps:
    1. Send a POST request to create a new movie rent with a client ID and movie copy details.
    2. Verify the response status code is 200 and retrieve the rent ID.
    3. Send a PUT request to close the movie rent using the retrieved rent ID.
    4. Verify the response status code is 200.
    5. Assert that the rent is marked as closed (`is_closed` is True).
    6. Assert that the `closed_datetime` field is not None, indicating the closure timestamp.
    Args:
        client (TestClient): The test client used to simulate API requests.
    """

    response = client.post(
        "/movie_rents",
        json={"client_id": 1, "details": [{"movie_copy_id": 2}, {"movie_copy_id": 11}]},
    )
    data = response.json()
    assert response.status_code == 200

    response = client.put(f"/movie_rents/{data['id']}/close")
    data = response.json()
    assert response.status_code == 200
    assert data["is_closed"] is True
    assert data["closed_datetime"] is not None
