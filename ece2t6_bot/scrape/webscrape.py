import json
from json.decoder import JSONDecodeError
import datetime
import calendar
import sys

import aiohttp
import asyncio


def set_payload(payload_file: str) -> dict:
    try:
        with open(payload_file, "r") as payload:
            data = json.load(payload)
    except JSONDecodeError as e:
        print(f"{payload_file} isn't formatted correctly: {e}")
        print("Exiting!")
        sys.exit(-1)

    return data


def organize_data(data_file: str) -> dict:
    with open(data_file, "r") as f:
        data = json.load(f)

    dummy_timestamp = datetime.datetime.fromtimestamp(0)

    for course in data["payload"]["pageableCourse"]["courses"]:
        id = course["id"]
        name = course["name"]
        code = course["code"]
        section_count = len(course["sections"])

        print(f"ID: {id}, NAME: {name}, CODE: {code}, SECTIONS: {section_count}")

        for section in course["sections"]:
            # change up indicies
            instructors = f'{section["instructors"]}'
            section_name = section["name"]
            section_type = section["type"]
            section_number = section["sectionNumber"]
            # change up indicies
            datetime.datetime.fromtimestamp(0)
            location = f'{section["meetingTimes"][0]["building"]["buildingCode"]}'
            meeting_day = calendar.day_name[section["meetingTimes"][0]["start"]["day"]]
            start_time = (dummy_timestamp + datetime.timedelta(milliseconds=section["meetingTimes"][0]["start"]["millisofday"])).time()
            end_time = (dummy_timestamp + datetime.timedelta(milliseconds=section["meetingTimes"][0]["end"]["millisofday"])).time()

            print(f"{instructors} {section_name} {section_type} {section_number} {location} {meeting_day} {start_time} {end_time}")


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
