from typing import Union
import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import aiohttp
import asyncio
from pprint import pprint

load_dotenv()

WEATHER_KEY = os.getenv('openweatherkey')

app = FastAPI()


@app.get("/")
async def homepage():
    return {"Hello": f"{WEATHER_KEY}"}


@app.get("/weather")
async def weather(city: Union[str, None] = None):
    async with aiohttp.ClientSession() as session:
        city = city or 'Dhaka'
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}'
        async with session.get(weather_url) as response:
            result = await response.json()
            pprint(result)
            if response.status != 200:
                raise HTTPException(status_code=404, detail=result)
            return result

