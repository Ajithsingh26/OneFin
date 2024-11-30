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
```
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

```

### Create Collection

**POST** `/collections/`

This endpoint allows a user to create a new collection of movies. The collection can optionally include a list of movies.

#### Request Body:

```json
{
  "title": "My Favorite Movies",
  "description": "A collection of my all-time favorite movies.",
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
    }
  ]
}
```

### List Collections

**GET** `/collections/`

This endpoint retrieves a list of collections belonging to the authenticated user.

#### Request Parameters:

- `page` (optional): The page number to fetch. Defaults to 1 if not provided.

#### Response:

```json
{
  "is_success": true,
  "data": {
    "collections": [
      {
        "uuid": "collection_uuid_1",
        "title": "My Favorite Movies",
        "description": "A collection of my all-time favorite movies."
      },
      {
        "uuid": "collection_uuid_2",
        "title": "Action Movies",
        "description": "A collection of the best action movies."
      }
    ],
    "favourite_genres": "Action, Adventure, Drama"
  }
}
```

### Update Collection

**PUT** `/collections/{uuid}/`

This endpoint allows a user to update an existing movie collection.

#### Request:

```json
{
  "title": "Updated Movie Collection",
  "description": "Updated description of the collection.",
  "movies": [
    {
      "uuid": "movie_uuid_3",
      "title": "New Movie Title",
      "description": "New Movie Description",
      "genres": "Comedy, Drama"
    }
  ]
}
```

### Delete Collection

**DELETE** `/collections/{uuid}/`

This endpoint allows a user to delete an existing movie collection.

#### Request:

No request body is required.

#### Response:

```json
{
  "message": "Collection with UUID {collection_uuid} has been deleted."
}
```

### Get Request Counter

**GET** `/request-count/`

This endpoint returns the total number of requests served by the server so far.

#### Request:

No request body is required.

#### Response:

```json
{
  "requests": 1500
}
```

### Reset Request Counter

**POST** `/request-count/reset/`

This endpoint resets the request counter back to 0.

#### Request:

No request body is required.

#### Response:

```json
{
  "message": "Request count reset successfully"
}
```

