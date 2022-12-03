import pandas as pd
import numpy as np
import logging
import os
from project.course import Course


class Courses:
    """
    This class keeps track of all the courses the user has input in a list filled with Course objects.
    """
    def __init__(self, courses: list[Course]) -> None:
        """
        The initialiser for the Courses class.

        Args:
            courses (list[Course]): A list of courses in the form of a Course object.
        """
        self.courses: list[Course] = courses

    def __str__(self) -> str:
        """
        Lists all Course objects in the list and appends their corresponding __str__() method to create
        readable string with all the courses.

        Returns:
            str: A readable format for all the Course object in the courses list.
        """
        _ = ""
        for course in self.courses:
            _ += f"{course.__str__()}\n"
        return _[:-1]

    def input_courses(self) -> None:
        """
        Prompt the user to input additional courses. This function is run when the '-i' or '-a' argument is passed.
        Creates a new course each cycle and adds it to the courses list.
        """
        while True:
            code = input("\nPlease input course code: ")
            if not code:
                print("The course code is not optional!")
                continue
            name = input("(Optional) Please input course name: ")
            completed_response = input("Is this course completed? (y/n, default=n): ")
            completed = False
            if completed_response.lower() == "y":
                completed = True
            new_course: Course = Course(code, name, completed)
            print(new_course)
            retry = input("Is this course correct? (y/n): ")
            if retry.lower() == "y":
                self.courses.append(new_course)
                add_another = input("Are these all the courses you want to add? (y/n): ")
                if add_another.lower() == "y":
                    break
    
    def add(self, course: Course) -> None:
        """
        A shortcut for self.courses.append(). Mostly used to avoid awkwardness in cases when appending to
        variables like all_courses, which would look like: all_courses.courses.append(course).

        Args:
            course (Course): The Course object to append to the courses list.

        Raises:
            ValueError: In case the course provided is not a Course object. This prevents everything from
                breaking, down the line.
        """
        if isinstance(course, Course):
            self.courses.append(course)
        else:
            raise ValueError(f"Course must be of class '{type(Course)}'")

    def save(self) -> None:
        """
        Converts the current courses in the list to a pandas DataFrame and saves it to a .csv.
        """
        course_array: np.ndarray = np.array([[course.code, course.name, course.completed] for course in self.courses])
        course_df: pd.DataFrame = pd.DataFrame(course_array, columns=["Code", "Name", "Completed"])
        course_df.to_csv("./project/courses.csv")

    def get_incomplete(self) -> 'Courses':
        """
        Generates a new Courses object with all courses in the list that are not set as completed
        and returns the new object.

        Returns:
            Courses: A new Courses instance derived from the main instance where all courses are not
                set as completed. 
        """
        incomplete_courses: list[Course] = [course for course in self.courses if course.completed == False]
        return Courses(incomplete_courses)

    @staticmethod
    def _read_csv_to_array() -> np.ndarray:
        """
        A static method that returns a numpy.ndarray with all of the course information. Should not be called
        directly since it is used when creating new Courses objects.

        Returns:
            np.ndarray: An array containing all saved course information.
        """
        return pd.read_csv("./project/courses.csv", names=["Code", "Name", "Completed"], header=0).to_numpy()

    @staticmethod
    def create_courses_from_path(path="./project/courses.csv") -> 'Courses':
        # TODO: Move the courses.csv to ./data/ and update the class to function appropriately.
        """
        Generates a new Courses instance by reading a file (default is courses.csv) and returns the instance. Should
        not be used in conjunction with save() every time to update an existing Courses instance, use add() for that.

        Args:
            path (str, optional): The path to the csv file with the course information. Defaults to "./courses.csv".

        Raises:
            ValueError: In case the file provided is not a .csv, raises a more to the point error.

        Returns:
            Courses: A new Courses instance based on the course information in the csv file.
        """
        if not path.endswith(".csv"):
            raise ValueError(f"Course file must be a .csv, is '.{path.split('.')[-1]}'")
        if not os.path.exists(path):
            logging.warning("No data file found! Creating empty object")
            return Courses([])
        arr: np.ndarray = Courses._read_csv_to_array()
        courses: list[Courses] = [Course(row[0], row[1], bool(row[2])) for row in arr]
        logging.info("Created courses from file")
        return Courses(courses)
