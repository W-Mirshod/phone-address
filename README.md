# Phone-Address Service

A microservice for storing and managing phone-address pairs using FastAPI and Redis.

## Features

- RESTful API for managing phone-address pairs
- Fast data storage using Redis
- Dockerized setup for easy deployment
- Comprehensive test coverage

## Endpoints

### 1. Get Address by Phone
**GET** `/phones/{phone}`

Retrieves the address associated with the specified phone number.

- **Success (200)**: Returns the phone-address pair in JSON format
- **Not Found (404)**: Phone number does not exist

**Example:**
```bash
curl http://localhost:8000/phones/+1234567890
```

### 2. Create Phone-Address Pair
**POST** `/phones`

Creates a new phone-address pair in the system.

**Request Body:**
```json
{
  "phone": "+1234567890",
  "address": "123 Main St, City, Country"
}
```

- **Success (201)**: Record created successfully
- **Conflict (409)**: Phone number already exists

**Example:**
```bash
curl -X POST http://localhost:8000/phones \
  -H "Content-Type: application/json" \
  -d '{"phone": "+1234567890", "address": "123 Main St"}'
```

### 3. Update Address
**PUT** `/phones/{phone}`

Updates the address for an existing phone number.

**Request Body:**
```json
{
  "address": "456 Oak Ave, City, Country"
}
```

- **Success (200)**: Address updated successfully
- **Not Found (404)**: Phone number does not exist

**Example:**
```bash
curl -X PUT http://localhost:8000/phones/+1234567890 \
  -H "Content-Type: application/json" \
  -d '{"address": "456 Oak Ave"}'
```

### 4. Delete Phone-Address Pair
**DELETE** `/phones/{phone}`

Removes a phone-address pair from the system.

- **Success (204)**: Record deleted successfully
- **Not Found (404)**: Phone number does not exist

**Example:**
```bash
curl -X DELETE http://localhost:8000/phones/+1234567890
```

## Running with Docker Compose

1. Build and start the services:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`
3. Redis will be available at `localhost:6379`

4. View API documentation at `http://localhost:8000/docs`

## Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start Redis (if not using Docker):
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

3. Set environment variable (optional, defaults to `redis://localhost:6379/0`):
```bash
export REDIS_URL=redis://localhost:6379/0
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

## Running Tests

```bash
pytest tests/
```

## Environment Variables

- `REDIS_URL`: Redis connection URL (default: `redis://localhost:6379/0`)

## Project Structure

```
phone-address/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── api.py           # API routes
│   ├── schemas.py       # Pydantic models
│   ├── config.py        # Redis configuration
│   └── deps.py          # Dependencies
├── tests/
│   ├── __init__.py
│   └── test_api.py      # API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

