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

asyncio.run(main())