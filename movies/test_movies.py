from fastapi.testclient import TestClient


def test_create_movie_with_stock_pass(client: TestClient):
    """
    Test the creation of a movie with a specified stock.
    This test verifies that a movie can be successfully created with the given
    attributes, including a specified stock count. It checks the following:
    - The HTTP response status code is 200 (success).
    - The returned movie data matches the input data (e.g., title, director).
    - The number of copies created matches the specified stock count.
    Args:
        client (TestClient): The test client used to simulate HTTP requests.
    """

    response = client.post(
        "/movies/with_stock",
        json={
            "title": "The Lion King",
            "director": "Rob Minkoff · Roger Allers",
            "year": 2024,
            "description": "The Lion King movie",
            "genre_id": 1,
            "stock": 5,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "The Lion King"
    assert data["director"] == "Rob Minkoff · Roger Allers"
    assert len(data["copies"]) == 5


def test_create_movie_with_stock_fail(client: TestClient):
    """
    Test case for creating a movie with stock but missing the required 'title' field.
    This test ensures that the API returns a 422 Unprocessable Entity status code
    when the 'title' field is not provided in the request payload. It also verifies
    that the error message specifies the missing 'title' field and indicates that
    it is required.
    Args:
        client (TestClient): The test client used to simulate API requests.
    Assertions:
        - The response status code is 422.
        - The error details in the response indicate that the 'title' field is missing.
        - The error message specifies that the 'title' field is required.
    """

    response = client.post(
        "/movies/with_stock",
        json={
            "director": "Rob Minkoff · Roger Allers",
            "year": 2024,
            "description": "The Lion King movie",
            "genre_id": 1,
            "stock": 5,
        },
    )
    data = response.json()
    assert response.status_code == 422
    assert "title" in data["detail"][0]["loc"]
    assert "Field required" == data["detail"][0]["msg"]


def test_update_movie_with_stock_pass(client: TestClient):
    """
    Test the functionality of updating a movie's stock and verifying the changes.
    This test performs the following steps:
    1. Creates a new movie with an initial stock value.
    2. Updates the movie's stock to a lower value and verifies:
       - The movie's title and description are updated correctly.
       - The number of copies is reduced to match the updated stock value.
    3. Updates the movie's stock to a higher value and verifies:
       - The number of copies is increased to match the updated stock value.
    Args:
        client (TestClient): The test client used to make HTTP requests.
    Assertions:
        - The response status code is 200 for all requests.
        - The movie's title and description are updated correctly.
        - The number of copies matches the updated stock value after each update.
    """

    response = client.post(
        "/movies/with_stock",
        json={
            "title": "The Lion King",
            "director": "Rob Minkoff · Roger Allers",
            "year": 2024,
            "description": "The Lion King movie",
            "genre_id": 1,
            "stock": 5,
        },
    )
    data = response.json()
    assert response.status_code == 200

    response = client.put(
        f"/movies/{data['id']}/with_stock",
        json={
            "id": data["id"],
            "title": "The Lion King 2",
            "director": "Rob Minkoff · Roger Allers",
            "year": 2024,
            "description": "The Lion King 2 movie",
            "genre_id": 1,
            "stock": 2,
        },
    )
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "The Lion King 2"
    assert data["description"] == "The Lion King 2 movie"

    # the number of movie copies should decrease from 5 to 2
    assert len(data["copies"]) == 2

    response = client.put(
        f"/movies/{data['id']}/with_stock",
        json={
            "id": data["id"],
            "title": "The Lion King 2",
            "director": "Rob Minkoff · Roger Allers",
            "year": 2024,
            "description": "The Lion King 2 movie",
            "genre_id": 1,
            "stock": 10,
        },
    )
    assert response.status_code == 200
    data = response.json()
    # the number of movie copies should increase from 2 to 10
    assert len(data["copies"]) == 10


def test_update_movie_with_stock_fail(client: TestClient):
    """
    Test case for updating a movie with stock when the movie does not exist.
    This test simulates a PUT request to update a movie with stock details
    for a movie ID that does not exist in the database. It verifies that the
    response status code is 404 (Not Found) and the response contains the
    appropriate error message.
    Args:
        client (TestClient): The test client used to simulate HTTP requests.
    Assertions:
        - The response status code is 404.
        - The response JSON contains a "detail" field with the value "Movie not found".
    """

    response = client.put(
        "/movies/1000/with_stock",
        json={
            "id": 1000,
            "title": "The Lion King 2",
            "director": "Rob Minkoff · Roger Allers",
            "year": 2024,
            "description": "The Lion King 2 movie",
            "genre_id": 1,
            "stock": 2,
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Movie not found"


def test_list_movies_by_name(client: TestClient):
    """
    Test the endpoint for listing movies by title.
    This test sends a GET request to the `/movies` endpoint with a query parameter
    for the movie title "Slam Dunk". It verifies that the response status code is 200
    and that the returned data contains exactly 4 items.
    Args:
        client (TestClient): The test client used to simulate HTTP requests.
    Assertions:
        - The response status code is 200.
        - The length of the returned data is 4.
    """

    response = client.get("/movies?title=Slam Dunk")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 4
