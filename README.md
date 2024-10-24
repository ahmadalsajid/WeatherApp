# WeatherApp

This is a simple weather API service using FastAPI that fetches weather
data from an external public API (openweathermap).

## Setup

First, clone this repository to your local machine, and create a `.env` file
from [sample.env](./app/sample.env) in the [app](./app) directory. Put your
own API key to make the app work.

Make sure the below tools are installed on your computer

* `Docker Desktop`: Download and configure from this [link](https://docs.docker.com/get-started/get-docker/)
* `localstack-cli`:
    * Visit [localstack/localstack-cli](https://github.com/localstack/localstack-cli/releases/latest) and download the
      latest release for your platform.
    * Extract the downloaded archive to a directory included in your PATH variable: For macOS/Linux, use the command:
      `sudo tar xvzf ~/Downloads/localstack-cli-*.tar.gz -C /usr/local/bin`

Now, you can use the [docker-compose.yaml](./docker-compose.yaml) to spin up a
container to test the application.

Let's spin up the application by

```
docker compose up -d --build
```

This will set up the `localstack` to mock AWS services locally. Once the
containers are up, check the localstack availability by

```
$ localstack status services
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ Service                  ┃ Status      ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
..........................................
│ dynamodb                 │ ✔ available │
..........................................
│ lambda                   │ ✔ available │
..........................................
│ s3                       │ ✔ available │
..........................................
└──────────────────────────┴─────────────┘

```

## Usage

It has only 1 API,

```
GET http://localhost:8000/weather
Content-Type: application/json
```

which returns the below response, with default `city` to `Dhaka`

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "coord": {
        "lon": 90.4074,
        "lat": 23.7104
    },
    "weather": [
        {
            "id": 721,
            "main": "Haze",
            "description": "haze",
            "icon": "50d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 300.14,
        "feels_like": 303.15,
        "temp_min": 300.14,
        "temp_max": 300.14,
        "pressure": 1008,
        "humidity": 83,
        "sea_level": 1008,
        "grnd_level": 1006
    },
    "visibility": 4000,
    "wind": {
        "speed": 4.63,
        "deg": 50
    },
    "clouds": {
        "all": 75
    },
    "dt": 1729754562,
    "sys": {
        "type": 1,
        "id": 9145,
        "country": "BD",
        "sunrise": 1729727986,
        "sunset": 1729769103
    },
    "timezone": 21600,
    "id": 1185241,
    "name": "Dhaka",
    "cod": 200
}
```

Or, you can pass a city name as a `city` query parameter, i.e.

```
GET http://localhost:8000/weather?city=london
Content-Type: application/json
```

which returns the below response,

```
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
{
    "coord": {
        "lon": -0.1257,
        "lat": 51.5085
    },
    "weather": [
        {
            "id": 800,
            "main": "Clear",
            "description": "clear sky",
            "icon": "01d"
        }
    ],
    "base": "stations",
    "main": {
        "temp": 282.11,
        "feels_like": 280.69,
        "temp_min": 280.53,
        "temp_max": 283.29,
        "pressure": 1021,
        "humidity": 93,
        "sea_level": 1021,
        "grnd_level": 1018
    },
    "visibility": 10000,
    "wind": {
        "speed": 2.57,
        "deg": 90
    },
    "clouds": {
        "all": 0
    },
    "dt": 1729755106,
    "sys": {
        "type": 2,
        "id": 2075535,
        "country": "GB",
        "sunrise": 1729752021,
        "sunset": 1729788521
    },
    "timezone": 3600,
    "id": 2643743,
    "name": "London",
    "cod": 200
}
```

If you pass a wrong city name, i.e.

```
GET http://localhost:8000/weather?city=londoiin
Content-Type: application/json
```

It returns the below error response,

```
HTTP/1.1 404 Not Found
Content-Type: application/json; charset=utf-8
{
    "detail": {
        "cod": "404",
        "message": "city not found"
    }
}
```

## Tools / Language / Framework
* Python
* FastAPI
* Docker Desktop
* Localstack
  * S3
  * DynamoDB

Once done with testing, remove with

## Tasks

1. FastAPI Setup: `DONE`
   - Create a FastAPI application with a single endpoint `/weather`.
   - The endpoint should accept a `GET` request with a `city` query parameter.
2. Asynchronous Data Fetching: `DONE`
   - Use Python's `asyncio` to asynchronously fetch the current weather data from the external API based on the `city` parameter.
   - Implement proper error handling to manage potential API failures or invalid city names.
3. AWS S3 (or Local equivalent) Integration: `DONE`
   - Store each fetched weather response as a JSON file in an S3 bucket or a local equivalent.
   - The filename should be structured as `{city}_{timestamp}.json`.
   - Use asynchronous methods to upload the data to the S3 or local equivalent.
4. AWS DynamoDB (or Local equivalent) Integration: `Contains bug`
   - After storing the json file, log the event (with city name, timestamp, and S3 URL/local path) into a DynamoDB table or a local equivalent asynchronously.
   - Ensure that database interactions are performed using async methods.
5. Caching with S3/Local Equivalent:
   - Before fetching the weather data from the external API, check if the data for the requested city (fetched within the last 5 minutes) already exists in S3 or the local equivalent.
   - If it exists, retrieve it directly without calling the external API.
   - Implement a mechanism to expire the cache after 5 minutes.
6. Deployment: `DONE`
   - Provide deployment scripts (like `Dockerfile`, `docker-compose.yml` etc.) in the repository.

```
docker compose down --rmi local -v
```
