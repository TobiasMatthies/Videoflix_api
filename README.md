# Videoflix API

This is the backend API for the Videoflix application, a video streaming service. It is built with Django and Django REST Framework.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- Pip
- Docker (optional)

### Installing

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/videoflix-api.git
   cd videoflix-api
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the migrations:
   ```bash
   python manage.py migrate
   ```
5. Start the development server:
    ```bash
    python manage.py runserver
    ```

The API will be available at `http://127.0.0.1:8000/`.
