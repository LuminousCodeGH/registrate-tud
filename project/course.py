class Course:
    def __init__(self, code: str, name="", completed=False):
        self.code: str = code
        self.name: str = name
        self.completed: bool = completed

    def __str__(self) -> str:
        return f"{self.code}: {self.name} ({self.completed})"

    @property
    def completed(self) -> bool:
        return self.__completed

    @completed.setter
    def completed(self, value: bool) -> None:
        self.__completed = value

    def complete(self) -> None:
        self.__completed = True
