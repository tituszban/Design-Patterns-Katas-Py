import re
from abc import ABC, abstractmethod


class ConditionABC(ABC):
    def _success(self) -> tuple[bool, str]:
        return True, ""

    def _fail(self, message: str) -> tuple[bool, str]:
        return False, message

    @abstractmethod
    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        raise NotImplementedError


class PropertyMinLength(ConditionABC):
    def __init__(self, property_name: str, min_length: int):
        self._property_name = property_name
        self._min_length = min_length

    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        if self._property_name not in user_data or len(user_data[self._property_name]) < self._min_length:
            return self._fail(f"Property '{self._property_name}' must be at least {self._min_length} characters long")
        return self._success()


class PropertyLengthRange(ConditionABC):
    def __init__(self, property_name: str, min_length: int, max_length: int):
        self._property_name = property_name
        self._min_length = min_length
        self._max_length = max_length

    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        length = None
        if self._property_name in user_data:
            length = len(user_data[self._property_name])

        if length is None or length < self._min_length or length > self._max_length:
            return self._fail(
                f"Property '{self._property_name}' must be between {self._min_length} and {self._max_length} characters long"
            )
        return self._success()


class PropertyMatchPattern(ConditionABC):
    def __init__(self, property_name: str, pattern: str, requirement: str):
        self._property_name = property_name
        self._pattern = re.compile(pattern)
        self._requirement = requirement

    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        if self._property_name not in user_data or not self._pattern.match(user_data[self._property_name]):
            return self._fail(f"Property '{self._property_name}' must {self._requirement}")
        return self._success()


class PropertyIsName(PropertyMatchPattern):
    def __init__(self, property_name: str):
        super().__init__(property_name, r"^[A-Z][a-z]+$", "be a valid name")


class CompositeCondition(ConditionABC):
    def __init__(self, name: str, *conditions: ConditionABC):
        self._name = name
        self._conditions = conditions

    def _indent_lines(self, errors: str) -> str:
        return "\n".join(["\t" + line for line in errors.split("\n")])

    def _get_validate_errors(self, user_data: dict[str, str]) -> list[str]:
        return [result[1] for condition in self._conditions if not (result := condition.validate(user_data))[0]]

    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        raise NotImplementedError


class ConditionAnd(CompositeCondition):
    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        errors = self._get_validate_errors(user_data)
        if not errors:
            return self._success()
        return self._fail(
            "\n".join(
                [
                    f"All of the following {self._name} errors must be fixed:",
                    *[self._indent_lines(error) for error in errors],
                ]
            )
        )


class ConditionOr(CompositeCondition):
    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        errors = self._get_validate_errors(user_data)
        if len(errors) < len(self._conditions):
            return self._success()
        return self._fail(
            "\n".join(
                [
                    f"At least one of the following {self._name} errors must be fixed:",
                    *[self._indent_lines(error) for error in errors],
                ]
            )
        )


def validate(user_data: dict[str, str]):
    conditions = ConditionOr(
        "user",
        ConditionAnd(
            "federation",
            PropertyMatchPattern("federation_provider", r"(foo)|(bar)", "be one of 'foo' or 'bar'"),
            PropertyLengthRange("federation_id", 1, 100),
        ),
        ConditionAnd(
            "login",
            PropertyLengthRange("user_id", 8, 12),
            ConditionAnd(
                "password",
                PropertyMinLength("password", 8),
                PropertyMatchPattern("password", r"^.*[0-9].*$", "contain a digit"),
                PropertyMatchPattern(
                    "password", r"^.*[!\"£$%^&*()_+\-=`¬|{}\[\]'#@~<>?,\./\\].*$", "contain a special character"
                ),
            ),
            ConditionOr(
                "user contact",
                PropertyMatchPattern(
                    "email", r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$", "be a valid email address"
                ),
                ConditionAnd(
                    "non-email login",
                    PropertyLengthRange("phone", 8, 10),
                    PropertyMatchPattern("phone", r"^[0-9]+$", "be only digits"),
                    PropertyLengthRange("username", 3, 20),
                    PropertyMatchPattern(
                        "username",
                        r"^[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_]+$",
                        "only contain alphanumerical characters or underscores",
                    ),
                ),
            ),
            PropertyIsName("firstname"),
            PropertyIsName("lastname"),
            ConditionOr(
                "address",
                PropertyLengthRange("address1", 1, 100),
                PropertyLengthRange("address2", 1, 100),
            ),
            PropertyLengthRange("postcode", 1, 10),
        ),
    )   # TODO: add actual exercise goals

    return conditions.validate(user_data)


def run_example():
    example = {}

    print(f"Example: {example}")
    valid, errors = validate(example)
    print(f"Valid: {valid}")
    if not valid:
        print("Errors:")
        print(errors)


if __name__ == "__main__":
    run_example()
