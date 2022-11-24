import pandas as pd
import numpy as np
import logging
import os
from course import Course


class Courses():
    def __init__(self, courses: list[Course]) -> None:
        self.courses: list[Course] = courses

    def __str__(self) -> str:
        _ = ""
        for course in self.courses:
            _ += f"{course.__str__()}\n"
        return _[:-1]

    def add_courses(self) -> None:
        while (True):
            code = input("\nPlease input course code: ")
            if (not code):
                print("The course code is not optional!")
                continue
            name = input("(Optional) Please input course name: ")
            completed_response = input("Is this course completed? (y/n, default=n): ")
            completed = False
            if (completed_response.lower() == "y"):
                completed = True
            new_course: Course = Course(code, name, completed)
            print(new_course)
            retry = input("Is this course correct? (y/n): ")
            if (retry.lower() == "y"):
                self.courses.append(new_course)
                add_another = input("Are these all the courses you want to add? (y/n): ")
                if (add_another.lower() == "y"):
                    break

    def save(self) -> None:
        course_array: np.ndarray = np.array([[course.code, course.name, course.completed] for course in self.courses])
        course_df: pd.DataFrame = pd.DataFrame(course_array, columns=["Code", "Name", "Completed"])
        course_df.to_csv("./courses.csv")

    def get_incomplete(self) -> 'Courses':
        incomplete_courses: list[Course] = [course for course in self.courses if course.completed == False]
        return Courses(incomplete_courses)

    @staticmethod
    def _read_csv_to_array() -> np.ndarray:
        return pd.read_csv("./courses.csv", names=["Code", "Name", "Completed"], header=0).to_numpy()

    @staticmethod
    def create_courses_from_path(path="./courses.csv") -> 'Courses':
        if (not path.endswith(".csv")):
            raise ValueError(f"Course file must be a .csv, is '.{path.split('.')[-1]}'")
        if (not os.path.exists(path)):
            logging.warning("No data file found! Creating empty object")
            return Courses([])
        arr: np.ndarray = Courses._read_csv_to_array()
        print(arr)
        courses: list[Courses] = [Course(row[0], row[1], bool(row[2])) for row in arr]
        logging.info("Created courses from file")
        return Courses(courses)
