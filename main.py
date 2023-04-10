import time as t
import random2 as rnd
import asyncio
import requests
import numpy as np

writeApiKey = '3A2OW4JDZ43TPLL6'
readApiKey = 'J9X5G5JXIA81IGQH'
channelId = '2081022'
backgrounds = ['']

writingSemaphore = False
nivel_agua = 0
sismo_anterior = None

async def temp():
    global writingSemaphore

    while writingSemaphore:
        t.sleep(1)

    writingSemaphore = True

    temp = rnd.randint(0, 50)

    params = {
        'api_key': writeApiKey,
        'field1': temp
    }

    r = requests.post("https://api.thingspeak.com/update", params=params)

    if temp > 35:
        asyncio.create_task(twitterMessage("Temperatura demasiado alta En el Sensor 1, la medida tomada fue: " + str(temp) + " grados"))

    if r.status_code == 200:
        print("Temp Update successful ", temp, r.status_code, r.reason)
    else:
        print("Temp 1 Update failed", r.status_code, r.reason)

    writingSemaphore = False

    t.sleep(17)

async def temp2():
    global writingSemaphore

    while writingSemaphore:
        t.sleep(1)

    writingSemaphore = True

    temp = rnd.randint(0, 50)

    params = {
        'api_key': writeApiKey,
        'field2': temp
    }

    r = requests.post("https://api.thingspeak.com/update", params=params)

    if temp > 35:
        asyncio.create_task(twitterMessage("Temperatura demasiado alta En el Sensor 2, la medida tomada fue: " + str(temp) + " grados"))

    if r.status_code == 200:
        print("Temp 2 Update successful ", temp, r.status_code, r.reason)
    else:
        print("Temp 2 Update failed", r.status_code, r.reason)

    writingSemaphore = False

    t.sleep(17)

async def sismografoYBoya():
    global writingSemaphore

    while writingSemaphore:
        t.sleep(1)

    writingSemaphore = True

    escalaSismo = rnd.uniform(0, 10)

    params = {
        'api_key': writeApiKey,
        'field5': escalaSismo
    }

    r = requests.post("https://api.thingspeak.com/update", params=params)

    asyncio.create_task(ajustar_nivel_agua(escalaSismo))

    writingSemaphore = False

    t.sleep(17)

async def ajustar_nivel_agua(sismo):
    global writingSemaphore, nivel_agua, sismo_anterior

    while writingSemaphore:
        t.sleep(1)

    writingSemaphore = True

    if sismo_anterior is not None:
        diferencia = sismo - sismo_anterior
        nivel_agua += diferencia / 10

    sismo_anterior = sismo

    params = {
        'api_key': writeApiKey,
        'field6': nivel_agua
    }

    r = requests.post("https://api.thingspeak.com/update", params=params)

    writingSemaphore = False

    t.sleep(17)

async def twitterMessage(reason):
    url = 'https://api.thingspeak.com/apps/thingtweet/1/statuses/update'

    params = {
        'api_key': 'QZD7KNAT4AXMAUTN',
        'status': reason
    }

    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("Message sent successfully", response.status_code, response.reason)
    else:
        print("Message sent failed", response.status_code, response.reason)

    t.sleep(17)

def generate_data():
    datos = np.random.randint(0, 51, size=(4, 6))
    datos = datos + 1
    return datos

async def phGenerator():

    data = generate_data()

    payload = {
        'api_key': writeApiKey,
        'field7': data
    }

    response = requests.post('https://api.thingspeak.com/update', params=payload)
    print(response.status_code, response.reason)

    t.sleep(17)
async def main():
    while True:
        #task1 = asyncio.create_task(temp())
        #task2 = asyncio.create_task(temp2())
        #task3 = asyncio.create_task(sismografoYBoya())
        task4 = asyncio.create_task(phGenerator())
        await asyncio.gather(task4)

asyncio.run(main())