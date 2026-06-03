# AI Incident Response Assistant

![CI Pipeline](https://github.com/bagcibaris/ai-incident-assistant/actions/workflows/ci.yml/badge.svg)


AI Incident Response Assistant is a machine learning powered REST API that analyzes system log messages and predicts the most likely incident layer. It also provides estimated severity, probable cause, and suggested remediation actions.

This project demonstrates AI, backend API development, incident response logic, and Dockerized deployment.

## Features

- Predicts incident layer from log messages
- Returns confidence score
- Provides estimated severity
- Suggests probable cause
- Suggests remediation action
- Supports single log prediction
- Supports batch log prediction
- Provides Swagger API documentation
- Runs locally or with Docker

## Supported Layers

- Application Layer
- Database Layer
- Network Layer
- Infrastructure Layer
- Security Layer
- Cache Layer
- External Service Layer

## Tech Stack

- Python
- Pandas
- Scikit-learn
- Joblib
- FastAPI
- Uvicorn
- Docker

## Project Structure

```txt
ai-incident-assistant/
├── Dockerfile
├── README.md
├── logs_dataset.csv
├── main.py
├── predict_assistant.py
├── predict_cli.py
├── requirements.txt
├── test_model.py
├── train_model.py
└── models/
    └── layer_classifier_model.pkl
