# API - Qto Categorizer API

- **Description**: Expose machine learning system designed to automatically categorize financial transactions
- **Purpose**: This API serves as an interface for a machine learning model that helps categorize financial transactions automatically, making it easier to organize and analyze financial data.

## Table of Content (ToC)

- [API - Qto Categorizer API](#api---qto-categorizer-api)
  - [Table of Content (ToC)](#table-of-content-toc)
  - [Quickstart](#quickstart)
    - [Locally](#locally)
    - [MLFlow model registry](#mlflow-model-registry)
  - [Endpoints](#endpoints)
    - [Health](#health)
    - [Info](#info)
    - [Predict](#predict)
    - [Test](#test)
    - [Documentation](#documentation)
  - [Project Structure](#project-structure)
  - [Bruno collections](#bruno-collections)
    - [Quick Start](#quick-start)
    - [Collections Overview](#collections-overview)
  - [Kafka (not tested!)](#kafka-not-tested)
    - [Start Kafka broker](#start-kafka-broker)

## Quickstart
### Locally

Install all required dependencies using Poetry and start the API server on all network interfaces (0.0.0.0) on port 88.

Note: Since qto-categorized-ml is not stored in an artifact registry, manually copy the wheel file to install the Python model using: `cp -r ../qto-categorizer-ml/dist ./data/dist` before running the installation.

```bash
$ poetry install
[...]
Package operations: 44 installs, 0 updates, 0 removals
[...]
$ poetry run qto-categorizer-api --host 0.0.0.0 --port 88
[\2024-05-28 15:58:59,332] {\root} \INFO - \[API] Starting service with version 0.1.0...
[\2024-05-28 15:58:59,332] {\root} \INFO - \[API] Log level set to DEBUG
[\2024-05-28 15:58:59,332] {\api_example.cli} \INFO - \[API] Log level set to DEBUG
[\2024-05-28 15:58:59,332] {\api_example.cli} \INFO - \[API] API service starting on 0.0.0.0:80
[\2024-05-28 15:59:15,529] {\uvicorn.error} \INFO - \Started server process [98569]
[\2024-05-28 15:59:15,529] {\uvicorn.error} \INFO - \Waiting for application startup.
[\2024-05-28 15:59:15,529] {\uvicorn.error} \INFO - \Application startup complete.
[\2024-05-28 15:59:15,534] {\uvicorn.error} \INFO - \Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

### MLFlow model registry

Start the API with a specific MLFlow model version (version 2)

```bash
$ export MLFLOW_TRACKING_URI=http://127.0.0.1:5000 # local usage
$ poetry run qto-categorizer-api --host 0.0.0.0 --port 88 -m models:/qto-categorizer-ml/2
[\2025-06-13 23:35:10,015] {\root} \INFO - \[API] Starting service with version 0.1.0...
[\2025-06-13 23:35:10,015] {\root} \INFO - \[API] Log level set to DEBUG
[\2025-06-13 23:35:10,015] {\qto_categorizer_api.cli} \INFO - \[API] Log level set to {'DEBUG'}
[\2025-06-13 23:35:10,015] {\qto_categorizer_api.cli} \INFO - \[API] API service starting on 0.0.0.
[\2025-06-13 23:35:11,569] {\uvicorn.error} \INFO - \Started server process [34990]
[\2025-06-13 23:35:11,569] {\uvicorn.error} \INFO - \Waiting for application startup.
[\2025-06-13 23:35:11,569] {\uvicorn.error} \INFO - \Application startup complete.
[\2025-06-13 23:35:11,569] {\uvicorn.error} \INFO - \Uvicorn running on http://0.0.0.0:88 (Press CTRL+C to quit)
[\2025-06-13 23:35:11,918] {\qto_categorizer_api.endpoints.predict} \INFO - \[API::predict] Request data AMOUNT=1.97 TYPE_OF_PAYMENT='Transfer' MERCHANT_NAME='GA CONSEIL' DESCRIPTION='VIREMENT SEPA EMIS    YCO8 0027 SYNACK  GA CONSEIL AFFOUDJI GERARD   GACONSEIL AFFOUDJI-FACT-2024-01 GACONSEIL AFFOUDJI-FACT-2024-01 EPC30B5XR5'
```

## Endpoints

### Health

A simple endpoint to check the health of the application.
```http
GET /health
```
Returns a status message indicating the service is up and running.
- **Use Case**: Useful for monitoring systems and load balancers to verify service availability
- **Response**: Returns HTTP 200 if service is healthy

### Info
Provides information about the application.
```http
GET /info
```
Returns metadata such as version, author, and other relevant details (cf. `data/info.txt`)
- **Use Case**: Useful for version checking and debugging
- **Response**: JSON containing application metadata

### Predict
Endpoint for making predictions based on input data.
```http
POST /predict
```
Accepts a JSON payload with the necessary input data and returns the prediction results.
- **Use Case**: Main endpoint for transaction categorization
- **Input**: JSON containing transaction details
- **Response**: JSON containing prediction results

### Test
Endpoint for testing purposes.
```http
GET /test
```
Returns a test response, useful for debugging and ensuring the endpoint is reachable.
- **Use Case**: Quick verification of API accessibility
- **Response**: Simple test message

### Documentation
FastAPI provides interactive API documentation.
```http
GET /docs
```
Access the Swagger UI for a user-friendly interface to interact with your API.
- **Features**: Interactive API testing, request/response schemas, authentication details

```http
GET /redoc
```
Access the ReDoc interface for an alternative documentation style.
- **Features**: Clean, responsive documentation with search capabilities

## Project Structure

    ├── qto-categorizer-api
    │   ├── .github                                        <- Github Actions CICD
    │   ├── data                                           <- Data files and configurations
    │   ├── docs                                           <- Sphinx documentation
    │   ├── src   
    │       └── qto_categorizer_api   <- Core of project
    │   │       ├── endpoints                               <- API endpoints definition
    │   │       ├── settings                                <- Application settings
    │   │       ├── __init__.py                            <- Package initialization
    │   │       ├── app.py                                 <- Main application setup
    │   │       ├── cli.py                                 <- Command line interface
    │   │       ├── errors                                 <- Error handling
    │   │       ├── load_model.py                          <- Model loading utilities
    │   │       └── setup_logging.py                       <- Logging configuration
    │   ├── tasks                                          <- Makefile tasks
    │   ├── tests                                          <- tests (units tests, data tests)
    │   ├── .gitignore                                     <- Git ignore rules
    │   ├── .mypy.ini                                      <- MyPy configuration
    │   ├── Makefile                                       <- Build and development tasks
    │   ├── poetry.toml                                    <- Poetry configuration
    │   ├── pyproject.toml                                 <- Project dependencies
        └── README.md                                      <- Project documentation

## Bruno collections

The API can be used using Bruno collections located in `qto-categorizer-api-collections`. These collections include ready-to-use requests for all endpoints.

### Quick Start

1. Install Bruno:
```bash
# macOS
brew install bruno
```

2. Import collections:
- Open Bruno
- Import `qto-categorizer-api-collections`
- Set base URL to `http://localhost:88`

### Collections Overview

| Collection | Purpose | Endpoint |
|------------|---------|----------|
| Health Check | API availability | `/health` |
| Info | API metadata | `/info` |
| Predict | Transaction categorization | `/predict` |
| Test | Basic connectivity | `/test` |

Example predict request:
```bruno
post {
  url: {{base_url}}/predict
  body: json {
    "transaction": {
      "description": "GROCERY STORE PURCHASE",
      "amount": 45.99,
      "date": "2024-03-15"
    }
  }
}
```

## Kafka (not tested!)

The system implements a Kafka-based prediction pipeline for handling asynchronous prediction requests:

1. A producer (producer.py) that:
   - Sends prediction requests to Kafka
   - Uses the same data model as the API
   - Includes error handling and logging

2. A consumer (consumer.py) that:
   - Consumes prediction requests from Kafka
   - Uses the same prediction logic as the API
   - Stores results in the database
   - Includes error handling and logging

3. Updated settings with Kafka configuration:
   - Bootstrap servers
   - Topic name
   - Default values for local development

To use this system:

1. Install the new dependencies:
```bash
poetry install --all-extras
```

2. Start a Kafka broker (if not already running)

3. Run the consumer in one terminal:

```bash
# Start the Kafka consumer service
qto-categorizer-kafka-consumer
```

4. Run the producer in another terminal:
```bash
# Start the Kafka producer service
qto-categorizer-kafka-producer
```

The producer will send a sample prediction request, and the consumer will process it and store the result in the database.

### Start Kafka broker

To start the Kafka broker:
1. Make sure you have Docker and Docker Compose installed on your system.
2. Start the Kafka broker and Zookeeper:

```bash
# Start Kafka and Zookeeper containers
docker-compose up -d
# Check container status
docker-compose ps
# View Kafka logs
docker-compose logs -f kafka
# Stop containers
docker-compose down
```

To verify messages are being sent and received, you can use the Kafka console consumer:
```bash
# Monitor Kafka messages in real-time
docker-compose exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic prediction-requests --from-beginning
```
