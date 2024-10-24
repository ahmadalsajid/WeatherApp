from typing import Union
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import aiohttp
import asyncio

load_dotenv()

WEATHER_KEY = os.getenv('openweatherkey')
WEATHER_CITY = 'Dhaka'

app = FastAPI()


@app.get("/")
async def homepage():
    return {"Hello": f"{WEATHER_KEY}"}


@app.get("/weather")
async def weather(city: Union[str, None] = None):
    async with aiohttp.ClientSession() as session:
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}'
        try:
            async with session.get(weather_url) as response:
                print(response.status)
                result = await response.json()
                if response.status != 200:
                    raise HTTPException(status_code=404, detail=result)
                return result
        except Exception as e:
            return e
