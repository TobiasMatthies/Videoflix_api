# Videoflix API

This is the backend API for the Videoflix application, a video streaming service. It is built with Django and Django REST Framework.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes using Docker.

### Prerequisites

-   Docker
-   Docker Compose

### Installing

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/videoflix-api.git
    cd videoflix-api
    ```
2.  **Set up the environment file:**
    Create a `.env` file by copying the template and fill in your details.
    ```bash
    cp env.template .env
    ```
3.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```

The API will be available at `http://127.0.0.1:8000/`.

## Features

-   **User Authentication:** User registration, activation via email, login, logout, and password reset.
-   **JWT Authentication:** Secure API endpoints using JSON Web Tokens (JWT).
-   **Video Streaming:** HLS-based video streaming with multiple resolutions.
-   **Video Processing:** Asynchronous video conversion to different resolutions (1080p, 720p, 480p) using FFmpeg and Redis Queue (RQ).
-   **Video Management:** API endpoints to list and retrieve video details.

## API Endpoints

All endpoints are prefixed with `/api/`.

### Authentication

-   `POST /register/`: Register a new user.
-   `GET /activate/<uid>/<token>/`: Activate a user account.
-   `POST /login/`: Log in a user and receive JWT tokens.
-   `POST /logout/`: Log out a user and blacklist the refresh token.
-   `POST /token/refresh/`: Refresh an expired access token.
-   `POST /password_reset/`: Request a password reset email.
-   `POST /password_confirm/<uid>/<token>/`: Confirm and set a new password.

### Videos

-   `GET /video/`: Get a list of all available videos.
-   `GET /video/<movie_id>/<resolution>/index.m3u8`: Get the HLS playlist for a specific video and resolution.
-   `GET /video/<movie_id>/<resolution>/<segment>`: Get a specific video segment for HLS streaming.
