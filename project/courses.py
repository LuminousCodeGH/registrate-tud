import pandas as pd
import numpy as np
import logging
import os
from course import Course


class Courses():
    def __init__(self, courses: list[Course]) -> None:
        self.courses: list[Course] = courses

    def __str__(self) -> str:
        _ = sum(f"{course.code}: {course.name} ({course.completed})\n" for course in self.courses)
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

    def save(self):
        course_array: np.ndarray = np.array([[course.code, course.name, course.completed] for course in self.courses])
        course_df: pd.DataFrame = pd.DataFrame(course_array)
        course_df.to_csv("./courses.csv")

    @staticmethod
    def _read_csv_to_array() -> np.ndarray:
        return pd.read_csv("./courses.csv").to_numpy()

    @staticmethod
    def create_courses_from_path(path="./courses.csv") -> 'Courses':
        if (not os.path.exists(path)):
            logging.warning("No data file found!")
            return Courses([])
        if (not path.endswith(".csv")):
            logging.warning("Course file must be a .csv!")
            return None
        arr: np.ndarray = Courses._read_csv_to_array()
        courses: list[Courses] = [Course(row[0], row[1], row[2]) for row in arr]
        print(courses)
        return Courses(courses)
