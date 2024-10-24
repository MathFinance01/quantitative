

class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner) -> object:
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < 0 | (not isinstance(value, int) or not isinstance(value, float)):
            raise ValueError("value should be a positive number")
        instance.__dict__[self.name] = value


class Number:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner) -> object:
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, int) or not isinstance(value, float):
            raise ValueError("value should be a number")
        instance.__dict__[self.name] = value

class FutureDate:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner) -> object:
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value < ql.Date.todaysDate() or not isinstance(ql.Date):
            raise ValueError("date should be in the future")
        instance.__dict__[self.name] = value