**API - Qto Categorizer API**

- **Description**: Expose machine learning system designed to automatically categorize financial transactions

## Table of Content (ToC)

- [Table of Content (ToC)](#table-of-content-toc)
- [Quickstart](#quickstart)
- [Endpoints](#endpoints)
  - [Health](#health)
  - [Info](#info)
  - [Predict](#predict)
  - [Test](#test)
  - [Documentation](#documentation)
- [Project Structure](#project-structure)
- [Kafka](#kafka)
  - [Start Kafka broker](#start-kafka-broker)
- [Contributions](#contributions)

## Quickstart

```bash
$ poetry install
[...]
Package operations: 44 installs, 0 updates, 0 removals
[...]
$ poetry run api-example
[\2024-05-28 15:58:59,332] {\root} \INFO - \[API] Starting service with version 0.1.0...
[\2024-05-28 15:58:59,332] {\root} \INFO - \[API] Log level set to DEBUG
[\2024-05-28 15:58:59,332] {\api_example.cli} \INFO - \[API] Log level set to DEBUG
[\2024-05-28 15:58:59,332] {\api_example.cli} \INFO - \[API] API service starting on 0.0.0.0:80
[\2024-05-28 15:59:15,529] {\uvicorn.error} \INFO - \Started server process [98569]
[\2024-05-28 15:59:15,529] {\uvicorn.error} \INFO - \Waiting for application startup.
[\2024-05-28 15:59:15,529] {\uvicorn.error} \INFO - \Application startup complete.
[\2024-05-28 15:59:15,534] {\uvicorn.error} \INFO - \Uvicorn running on http://0.0.0.0:80 (Press CTRL+C to quit)
```

## Endpoints

### Health
A simple endpoint to check the health of the application.
```http
GET /health
```
Returns a status message indicating the service is up and running.

### Info
Provides information about the application.
```http
GET /info
```
Returns metadata such as version, author, and other relevant details (cf. `data/info.txt`)

### Predict
Endpoint for making predictions based on input data.
```http
POST /predict
```
Accepts a JSON payload with the necessary input data and returns the prediction results.

### Test
Endpoint for testing purposes.
```http
GET /test
```
Returns a test response, useful for debugging and ensuring the endpoint is reachable.

### Documentation
FastAPI provides interactive API documentation.
```http
GET /docs
```
Access the Swagger UI for a user-friendly interface to interact with your API.

```http
GET /redoc
```
Access the ReDoc interface for an alternative documentation style.

## Project Structure

    ├── qto-categorizer-api
    │   ├── .github                                         <- Github Actions CICD
    │   ├── data
    │   ├── docs                                            <- Sphinx documentation
    │   ├── src   
    │       └── qto_categorizer_api   <- Core of project
    │   │       ├── endpoints                               <- API endpoints definition
    │   │       ├── settings                                <- settings
    │   │       ├── __init__.py      
    │   │       ├── app.py           
    │   │       ├── cli.py           
    │   │       ├── errors           
    │   │       ├── load_model.py    
    │   │       └── setup_logging.py 
    │   ├── tasks                                           <- Makefile tasks
    │   ├── tests                                           <- tests (units tests, data tests)
    │   ├── .gitignore          
    │   ├── .mypy.ini   
    │   ├── Makefile   
    │   ├── poetry.toml                       
    │   ├── pyproject.toml   
        └── README.md    


## Kafka

I've created a complete Kafka-based prediction system with:

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
python -m qto_categorizer_api.kafka.consumer
```

4. Run the producer in another terminal:

```bash
python -m qto_categorizer_api.kafka.producer
```

The producer will send a sample prediction request, and the consumer will process it and store the result in the database.

### Start Kafka broker

To start the Kafka broker:
1 .Make sure you have Docker and Docker Compose installed on your system.
2. Start the Kafka broker and Zookeeper:

```bash
docker-compose up -d
docker-compose ps
docker-compose logs -f kafka
docker-compose down
```

The configuration I've provided:
- Uses Confluent's Kafka image which is well-maintained
- Sets up a single-node Kafka broker
- Configures Zookeeper (required for Kafka)
- Exposes Kafka on port 9092 (matching our application settings)
- Enables auto-creation of topics
- Sets up a single replica (suitable for development)

Once the broker is running, you can test it with our producer and consumer:

To verify messages are being sent and received, you can use the Kafka console consumer:
```bash
docker-compose exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic prediction-requests --from-beginning
```

## Contributions

Your contributions are valued! Please feel free to open issues or submit pull requests.

Let me know if you'd like any other sections added!