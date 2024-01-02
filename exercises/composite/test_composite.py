import pytest
from .composite import validate


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            {},
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'user_id' must be between 8 and 12 characters long
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must be at least 8 characters long
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "federation_provider": "foo",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'user_id' must be between 8 and 12 characters long
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must be at least 8 characters long
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {"federation_provider": "baz", "federation_id": "XXXX"},
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\tAll of the following login errors must be fixed:
\t\tProperty 'user_id' must be between 8 and 12 characters long
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must be at least 8 characters long
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {"federation_provider": "bar", "federation_id": "XXXX"},
            (True, ""),
        ),
        (
            {
                "user_id": "XXXXXXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must be at least 8 characters long
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXXXXXXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'user_id' must be between 8 and 12 characters long
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must be at least 8 characters long
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'user_id' must be between 8 and 12 characters long
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must be at least 8 characters long
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must contain a digit
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAll of the following password errors must be fixed:
\t\t\tProperty 'password' must contain a special character
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "email": "foo@bar.com",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "1234",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "1234-abc",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be only digits
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXX!",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'username' must only contain alphanumerical characters or underscores
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXXXXXXXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'username' must be between 3 and 20 characters long
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {"user_id": "XXXXXXXXXX", "password": "XXXXXXXX1!", "phone": "123456789", "username": "XXXXXXXXXXXXXXX"},
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {"user_id": "XXXXXXXXXX", "password": "XXXXXXXX1!", "phone": "1234", "username": "XXXXXXXXXXXXXXX"},
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tAt least one of the following user contact errors must be fixed:
\t\t\tProperty 'email' must be a valid email address
\t\t\tAll of the following non-email login errors must be fixed:
\t\t\t\tProperty 'phone' must be between 8 and 10 characters long
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "firstname": "Xxx",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "firstname": "XXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "lastname": "Xxx",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "lastname": "XXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tAt least one of the following address errors must be fixed:
\t\t\tProperty 'address1' must be between 1 and 100 characters long
\t\t\tProperty 'address2' must be between 1 and 100 characters long
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "address1": "XXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "address2": "XXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'firstname' must be a valid name
\t\tProperty 'lastname' must be a valid name
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "firstname": "Xxx",
                "lastname": "Xxx",
                "address1": "XXXX",
            },
            (
                False,
                """
At least one of the following user errors must be fixed:
\tAll of the following federation errors must be fixed:
\t\tProperty 'federation_provider' must be one of 'foo' or 'bar'
\t\tProperty 'federation_id' must be between 1 and 100 characters long
\tAll of the following login errors must be fixed:
\t\tProperty 'postcode' must be between 1 and 10 characters long
""".strip(),
            ),
        ),
        (
            {
                "user_id": "XXXXXXXXXX",
                "password": "XXXXXXXX1!",
                "phone": "123456789",
                "username": "XXXXXXXXXXXXXXX",
                "firstname": "Xxx",
                "lastname": "Xxx",
                "address1": "XXXX",
                "postcode": "xxxx",
            },
            (True, ""),
        ),
    ],
)
def test_validate(test_input, expected):
    assert validate(test_input) == expected

# TODO: add tests for the individual components
