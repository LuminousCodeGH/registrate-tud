class Course:
    """
    This class is stores various information about a course, such as the code, an optional name and whether it
    has been completed or not. Completion has as of now not been implemented.
    """
    def __init__(self, code: str, name="", completed=False):
        """
        The initialiser for the Course class.

        Args:
            code (str): The code of a course. This is used to look up the course on MyTUD.
            name (str, optional): An optional name for the course to help with recognition after
                the user has been notified of an open sign up. Defaults to "".
            completed (bool, optional): Whether or not the course has been completed. If it has,
                the program will not search for this course on MyTUD. Defaults to False.
        """
        self.code: str = code
        self.name: str = name
        self.completed: bool = completed

    def __str__(self) -> str:
        """
        Returns the course in a readable format. For example: 'EX1234: Example Course (False)'.

        Returns:
            str: A readable format for the Course object.
        """
        return f"{self.code}: {self.name} ({self.completed})"

    @property
    def completed(self) -> bool:
        return self.__completed

    @completed.setter
    def completed(self, value: bool) -> None:
        self.__completed = value

    def complete(self) -> None:
        """
        Sets completed to True, after which the Scraper will not search for it on MyTUD.
        """
        self.__completed = True
