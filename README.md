# WeatherApp

This is a simple weather API service using FastAPI that fetches weather
data from an external public API (openweathermap).

## Docker

First, clone this repository to your local machine, and create a `.env` file
from [sample.env](./app/sample.env) in the [app](./app) directory. Put your
own API key to make the app work.

You can use the [docker-compose.yaml](./docker-compose.yaml) to spin up a
container to test the application.

Let's spin up the application by

```
docker compose up -d
```

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

Once done with testing, remove with

```
docker compose down --rmi local
```
