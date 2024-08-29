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
git clone https://github.com/yourusername/yourproject.git
cd yourproject
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
```
python app.py
```