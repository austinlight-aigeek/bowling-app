# Bowling Game APP with FastAPI and React

This project is a full-stack bowling game management system, utilizing a Python backend with a RESTful API and a React frontend. The backend includes game logic to manage and record bowling scores, and integrates with a large language model (LLM) to generate natural language summaries of the game state. The frontend provides a user interface to interact with the system.

![Bowling Game Demo](demo.gif)

## Features

- Create and manage bowling games
- Record rolls and calculate scores according to bowling rules
- Retrieve game scores, statistial summaries and historical graph
- Integration with OpenAI's GPT-4 for natural language summaries
- Dockerized setup for easy deployment

## Prerequisites

- Python 3.12.X
- Docker and Docker Compose installed
- OpenAI API Key for LLM integration

### 1. Clone the Repository

Clone the project from GitHub using the following command:

```bash
git clone https://github.com/austinlight-aigeek/bowling-app
cd bowling-app
```

### 2. Set Up Environment Variables

You will need to set up two `.env` files—one in the project root directory and one in the backend/ directory.

**Root** `.env` **File**

Create an `.env` file in the root directory and set your OpenAI API key and postgresql credentials:

```
OPENAI_API_KEY=your_openai_api_key

POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
POSTGRES_SERVER = localhost
POSTGRES_PORT = 5432
POSTGRES_DB = bowling
```

Refer to `env.development` for the structure.

**Backend** `.env` **File**

Copy the provided `.env.mock` from `backend/` file into the `backend/` directory and rename it to `.env`. This file contains the necessary environment variables for the backend services.

### 3. Set Up Backend

#### a. Create a Virtual Environment

Navigate to the backend folder and create a virtual environment:

```
cd backend
python -m venv venv
```

#### b. Activate the Virtual Environment

- For Windows:

```bash
source venv/Scripts/activate
```

- For macOS/Linux:

```bash
source venv/bin/activate
```

#### c. Install Dependencies

Install the necessary Python packages by running:

```bash
pip install -r requirements.txt
```

### 4. Build and Run the Docker Containers

Navigate back to the project root and build the Docker containers:

```bash
docker-compose up --build
```

### 5. Apply Database Migrations

After the Docker containers are running, navigate to the backend/ directory and run the following command to apply database migrations:

```bash
alembic upgrade head
```

### 6. Verify the Application

Ensure that all services (backend, frontend, PostgreSQL) are running correctly in Docker.

Open your browser and navigate to:

```
http://localhost:3000
```

## Running Tests

You can run unit and integration tests to verify the functionality of the backend.

- **Unit tests** are located in backend/tests/unit/
- **Integration** tests are located in backend/tests/integration/

To run the tests, use:

```
pytest
```

## More Information

For additional details, you can refer to the project documentation and video instructions:

- Project Documentation: []
- Video Instructions: []

## Troubleshooting

- Ensure Docker is running and all services are up using `docker ps`.
- Verify that the OpenAI API key is correctly set in the root `.env` file.
- Check if the virtual environment is activated before running backend commands.
