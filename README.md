# Movie Collection API

This is a Django-based API that manages movie collections, where users can register, create collections, and manage movies in their collections. The API also includes scalable request counting and the ability to reset the count.

## Prerequisites

- Python 3.x installed
- Redis server (for caching and request counting)
- PostgreSQL database server (for Django's default database)
- Python virtual environment (optional but recommended)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/movie-collection-api.git
    cd movie-collection-api
    ```

2. Create and activate a virtual environment (optional):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the Redis server:

    - Install Redis and run it locally. You can download Redis from [here](https://redis.io/download).
    - To run Redis locally, use the following command:

    ```bash
    redis-server
    ```

5. Set up environment variables:

    You can either add your environment variables in a `.env` file or manually configure them in `settings.py`.

    Example `.env` file:

    ```ini
    REDIS_URL=redis://127.0.0.1:6379
    EXTERNAL_MOVIES_API_URL=https://example.com/movies-api
    API_USERNAME=your_api_username
    API_PASSWORD=your_api_password
    ```

    Ensure to install `python-dotenv` if you're using a `.env` file:

    ```bash
    pip install python-dotenv
    ```

6. Set up the database:

    ```bash
    python manage.py migrate
    ```

7. Run the server:

    ```bash
    python manage.py runserver
    ```

Your API should now be available at `http://127.0.0.1:8000`.

## API Endpoints

### User Registration

**POST** `/register/`

This endpoint allows a user to register a new account.

#### Request Body:

```json
{
  "username": "testuser",
  "password": "Password123!"
}

### Movie List

**GET** `/movies/`

This endpoint retrieves a list of movies, optionally paginated.

#### Request Parameters:

- `page` (optional): The page number to fetch. Defaults to `1` if not provided.

#### Response:

```json
{
  "count": 100,
  "page": 1,
  "movies": [
    {
      "uuid": "movie_uuid_1",
      "title": "Movie Title",
      "description": "Movie Description",
      "genres": "Action, Adventure"
    },
    {
      "uuid": "movie_uuid_2",
      "title": "Another Movie",
      "description": "Another Description",
      "genres": "Drama, Thriller"
    },
    ...
  ]
}


