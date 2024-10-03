class DepartmentNotFoundError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__(f"|Department| with the given {id} doesn't exists")


class MunicipalityNotFoundError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__(f"|Municipality| with the given {id} does not exists")


class HighschoolNotFoundError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__(f"|Institution| with the given {id} does not exists")


class CollegeNotFoundError(Exception):

    def __init__(self, id: str) -> None:
        super().__init__(f"""|College| with the given {id} does not exists""")

class PeriodNotFoundError(Exception):
    def __init__(self, id: str) -> None:
        super().__init__(f"""|Period| with the given {id} does not exists""")
