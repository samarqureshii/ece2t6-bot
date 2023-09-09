import json
from json.decoder import JSONDecodeError
import datetime
import calendar
import sys
from dataclasses import dataclass

import aiohttp
import asyncio


@dataclass
class CourseSection:
    instructors: list[str]
    name: str
    type: str
    number: str
    building: str
    weekday: str
    start_time: datetime.time
    end_time: datetime.time


@dataclass
class Course:
    name: str
    code: str
    sections: list[CourseSection]


def set_payload(payload_file: str) -> dict:
    try:
        with open(payload_file, "r") as payload:
            data = json.load(payload)
    except JSONDecodeError as e:
        print(f"{payload_file} isn't formatted correctly: {e}")
        print("Exiting!")
        sys.exit(-1)

    return data


def organize_data(data_file: str) -> list[Course]:
    with open(data_file, "r") as f:
        data = json.load(f)

    dummy_timestamp = datetime.datetime.fromtimestamp(0)

    courses = []
    for course_data in data["payload"]["pageableCourse"]["courses"]:
        course = Course(
            name=course_data["name"],
            code=course_data["code"],
            sections=[]
        )

        for section_data in course_data["sections"]:
            # preprocessing
            instructors = [' '.join(name_data.values()) for name_data in section_data["instructors"]]
            weekday = calendar.day_name[section_data["meetingTimes"][0]["start"]["day"]]
            start_time = (dummy_timestamp + datetime.timedelta(milliseconds=section_data["meetingTimes"][0]["start"]["millisofday"])).time()
            end_time = (dummy_timestamp + datetime.timedelta(milliseconds=section_data["meetingTimes"][0]["end"]["millisofday"])).time()

            section = CourseSection(
                instructors=instructors,
                name=section_data["name"],
                type=section_data["type"],
                number=section_data["sectionNumber"],
                building=section_data["meetingTimes"][0]["building"]["buildingCode"],
                weekday=weekday,
                start_time=start_time,
                end_time=end_time
            )

            course.sections.append(section)

        courses.append(course)

    return courses


def print_data(courses: list[Course]) -> None:
    for course in courses:
        print(f"NAME: {course.name}, CODE: {course.code}, SECTIONS: {len(course.sections)}")

        for section in course.sections:
            print(f"{', '.join(section.instructors)} {section.name} {section.type} {section.number} {section.building} {section.weekday} {section.start_time} {section.end_time}")


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

    courses = organize_data("data.json")

    print("Data organized.")

    print("Printing!")

    print_data(courses)

asyncio.run(main())
