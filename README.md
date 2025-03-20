# Movie Rental Backend

This project is a backend system for managing a movie rental service. It provides a set of RESTful APIs built with **FastAPI** to handle operations such as managing movies, clients, and movie rentals. The system is designed with a focus on transactional APIs to ensure data consistency and reliability.

## Key Features

### 1. **Transactional APIs**
The project includes robust transactional APIs to handle critical operations:

#### **Add Movie Rent**
- **Endpoint**: `POST /movie_rents`
- **Description**: Allows clients to rent movies by creating a new movie rental record along with its details.
- **Workflow**:
  - Validates the input data using the `MovieRentCreate` model.
  - Persists the `MovieRent` record in the database.
  - Optionally processes and persists associated `MovieRentDetail` records for each rented movie copy.
  - Ensures all operations are committed as a single transaction to maintain data integrity.
- **Sequence Diagram**: Refer to [seq_diag_rent_movies.mmd](seq_diag_rent_movies.mmd) for a detailed workflow.

#### **Add Movie with Stock**
- **Endpoint**: `POST /movies/with_stock`
- **Description**: Adds a new movie to the catalog along with its stock of movie copies.
- **Workflow**:
  - Validates the input data using the `MovieCreate` model.
  - Creates a new `Movie` record in the database.
  - Generates and persists multiple `MovieCopy` records based on the specified stock.
  - Ensures all operations are committed as a single transaction to maintain consistency.
- **Sequence Diagram**: Refer to [seq_diag_add_movie_with_stock.mmd](seq_diag_add_movie_with_stock.mmd) for a detailed workflow.

### 2. **Movie Management**
- Add, update, delete, and retrieve movies.
- Support for managing movie genres and their associations.

### 3. **Client Management**
- Add, update, delete, and retrieve client information.

### 4. **Movie Rental Management**
- Retrieve, update, and delete movie rental records.
- Close active rentals and mark them as completed.

### 5. **Database Integration**
- Built using **SQLModel** for seamless integration with a relational database.
- Supports SQLite as the default database.

### 6. **Data Validation**
- Uses **Pydantic** models for input validation and serialization.

### 7. **Testing**
- Includes unit tests for critical APIs using **pytest** and **FastAPI TestClient**.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- SQLite (default database)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
