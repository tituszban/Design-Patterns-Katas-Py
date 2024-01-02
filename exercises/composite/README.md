# Composit Pattern

The Composit Pattern is a Structural pattern first published in the Gang of Four book _Design Patterns: Elements of Reusable Object-Oriented Software_.

TODO: Write about the use cases of this pattern

## Composite pattern exercise

In this exercise, you are validating a user registration into your system. There are multiple different ways the user can register, and you must not only validate that the registration is valid, but also provide verbose information to the user if it is not, including each of the fields that are incorrect, and which of them the user must complete.

### Requirements

There are two core ways the user can register. Either using their own details, or via a federated provider.

If registering via a federation, all you need 2 fields:
 - `federation_provider` must be one of `foo` or `bar`
 - `federation_id` is a string that is between 1 and 100 characters long (inclusive)

If both of these fields are valid, the login is valid.

Otherwise, the user is registering with a login. In this case, you must have the following fields:

 - `user_id` is a string between 8 and 12 characters long (inclusive)
 - `password` must be at least 8 characters long, contain a digit and a special character
 - some kind of user contact and display name. This may be either email or username and phone number. If the user provides all, that is also valid.
    - `email` must be a valid email address as validated by a basic regex
    - `phone` must be between 8 and 10 characters long (inclusive) and contain only digits
    - `username` must be between 3 and 20 characters long (inclusive) and contain only alphanumeric characters and underscores
 - `firstname` and `lastname` must both be valid names of letters a-z, with the first one capitalised
 - The address must contain at least one line of address (`address1` or `address2`) longer than 1 character (and at most 100 characters) and a `postcode`.

When requirements allow multiple different fields (such as federated and login) user details are valid if both are present. A different system is tasked with picking which one to use for the user, which is not part of the exercise.

### Your goals are

You have to add a new requirement for the login path, where the user can log in not just with email or username and phone number, but also a Fediverse id, which looks like an email address, but has a leading `@` symbol. Such as `@foo@bar.com`.
Furthermore, to support international shipping, another valid field combination for address is instead of `postcode`, the user may have `state` (4-10 characters long), `city` (3-100 characters long) and `zipcode` (4-10 characters long and only contains digits)

Refactor the code (ideally using the Composite Pattern) to make it easier to test in multiple components, and to make the requirements easier to read.

Then add the new requirements.

If you are struggling to match it one-to-one, try matching only the outcome, and the text description, which may differ slighly after the refactoring.

### Hints

<details>
  <summary>Hint 1</summary>

  Try describing each condition as a class, such as this one:
```py
class PropertyMinLength:
    def __init__(self, property_name: str, min_length: int):
        self._property_name = property_name
        self._min_length = min_length

    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        if self._property_name not in user_data or len(user_data[self._property_name]) < self._min_length:
            return False, f"Property '{self._property_name}' must be at least {self._min_length} characters long"
        return True
```
</details>

<details>
  <summary>Hint 2</summary>

  Now think about how you could could create a condition, with the same `validate` method signature, but one that combines multiple other conditions. Such as all conditions must be valid:
```py
class CombineAnd:
    def __init__(self, condition1, condition2):
        self._condition1 = condition1
        self._condition2 = condition2

    def validate(self, user_data: dict[str, str]) -> tuple[bool, str]:
        result1, error1 = condition1.validate(user_data)
        result2, error2 = condition2.validate(user_data)

        return result1 and result2, '\n'.join([error1, error2])

CombineAnd(
    PropertyMinLength("password", 8),
    PropertyContainsDigit("password"),  # You would also need to create this other condition
)
```
</details>

TODO: Add more hints