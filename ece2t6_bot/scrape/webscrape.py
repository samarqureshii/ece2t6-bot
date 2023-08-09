import aiohttp
import asyncio
import json

def set_payload(payload_file: str) -> dict:
    try:
        with open(payload_file, "r") as payload:
            data = json.load(payload)
    except:
        print(f"{payload_file} isn't formatted correctly.")

    return data

def organize_data(data_file: str) -> dict:
    with open(data_file, "r") as f:
        data = json.load(f)

    for course in data["payload"]["pageableCourse"]["courses"]:
        id = course["id"]
        name = course["name"]
        code = course["code"]

        print(f"ID: {id}, NAME: {name}, CODE: {code}")

async def main():

    url = 'https://api.easi.utoronto.ca/ttb/getPageableCourses'
    headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    

    print("Getting payload...")

    payload = set_payload("payload.json")

    print("Payload recieved.")

    async with aiohttp.ClientSession() as session:

        print("Sending POST request to server.")

        async with session.post(url, headers=headers, json=payload) as response:

            print(f"Server status: {response.status}")

            if response.status > 400:
                print("Something went wrong. Try again later.")
                return
            else:
                print("Server's up.")

            print("Fetching data.")

            data = await response.json()

            print("Data fetched.")

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)

    print("Organizing data.")
    
    organize_data("data.json")

    print("Data organized.")

asyncio.run(main())