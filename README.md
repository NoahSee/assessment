# Project Setup

## Introduction

This project is a Flask-based API for managing applicants, schemes, and applications. It includes functionality for registering and logging in administrators, adding and retrieving applicants, managing schemes, and handling applications.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- Python 3.8 or higher
- `pip` (Python package installer)
- `jq` (command-line JSON processor)

## Installation

### Clone the Repository

```bash
gh repo clone NoahSee/assessment
cd assessment
```

### Set Up the Virtual Environment
Create and activate a virtual environment for Python:

```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
brew install jq
```

### Run
This will automatically reset the database and populate some applicants and schemes:

```
python app.py
```

## Usage

### Authentication
Register a New User:
```
curl -X POST http://localhost:8000/api/register \
     -H "Content-Type: application/json" \
     -d '{"username": "newuser", "password": "password123"}'
```
Login
(copy the JWT)
```
curl -X POST http://localhost:8000/api/login \
     -H "Content-Type: application/json" \
     -d '{"username": "existinguser", "password": "password123"}'
```

Example - Get all applicants
```
curl -X GET http://localhost:8000/api/applicants/ \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
