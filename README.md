# Self-Hosted Blender API (Python)

This repository contains a simple API built with Flask, a lightweight WSGI web application framework in Python. The API is designed to be a starting point for processing 3D models (OBJ, FBX, STL, GLB).

## Features

* [Flask](https://flask.palletsprojects.com/en/3.0.x/) as the web framework
* [Python](https://www.python.org/)

## Getting Started

### Prerequisites

* Python
* pip

### Installation

1. Clone the repository:
```bash
git clone git@github.com:celestelayne/self_hosted_blender_api.git
cd self_hosted_blender_api
```
2. Create and activate the virtual environment:
```bash
# venv or pip3
```
3. Install dependencies:
```bash
pip3 install -r requirements.txt 
```

### Running the Project

1. Set up environment variables in a `.env` file in the root directory:
```makefile
FLASK_APP=app.py
FLASK_ENV=development
PORT=5000
```
2. Run the Flask development server:
```bash
flask run
```
The API will be running at http://localhost:5000

### Available Scripts

* `flask run`: Starts the Flask development server

### Project Structure

```bash
self_hosted_blender_api/
├── .env
├── .gitignore
├── api
    └── index.py
├── README.md
└── requirements.txt
```