# Bowling Game API with FastAPI and React

This project is an API to manage a bowling game, including recording and retrieving scores. It integrates a large language model (LLM) to provide natural language summaries of the current game state.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [API Endpoints](#api-endpoints)

---

## Overview

The project consists of:

- **FastAPI Backend**: Handles game logic and API endpoints.
- **React Frontend**: Allows users to interact with the game via a web interface.
- **LLM Integration**: Provides natural language summaries of game states using OpenAI's API.

## Project Structure

```bash
bowling-app/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── endpoints.py     # API endpoints
│   │   ├── core/
│   │   │   └── config.py        # Configuration and environment variables
│   │   ├── models/
│   │   │   └── game.py          # Game logic and models
│   │   └── main.py              # Entry point for FastAPI
│   ├── tests/
│   │   ├── unit/
│   │   │   └── test_game_logic.py    # Unit tests for game logic
│   │   ├── integration/
│   │   │   └── test_endpoints.py     # Integration tests for API endpoints
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/austinlight-aigeek/bowling-app
cd bowling-app
```

### 2. Environment Setup
