from typing import Union
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

WEATHER_KEY = os.getenv('openweatherkey')
WEATHER_CITY = 'Dhaka'

app = FastAPI()




@app.get("/")
async def homepage():
    return {"Hello": f"{WEATHER_KEY}"}


@app.get("/weather")
async def weather(city: Union[str, None] = None):
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_KEY}'
    return {
        "Hello": city,
    }
