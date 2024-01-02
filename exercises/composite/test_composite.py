from .composite import validate


def test_validate_empty():
    is_valid, error = validate({})
    assert not is_valid
    assert (
        error
        == """
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
""".strip()
    )
