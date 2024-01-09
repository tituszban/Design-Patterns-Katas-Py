import re


def validate(user_data: dict[str, str]) -> tuple[bool, str]:
    federation_errors: list[str] = []
    if "federation_provider" not in user_data or user_data["federation_provider"] not in ["foo", "bar"]:
        federation_errors.append("Property 'federation_provider' must be one of 'foo' or 'bar'")
    if "federation_id" not in user_data or len(user_data["federation_id"]) < 1 or len(user_data["federation_id"]) > 100:
        federation_errors.append("Property 'federation_id' must be between 1 and 100 characters long")
    federation_valid = len(federation_errors) == 0

    userid_errors: list[str] = []
    if "user_id" not in user_data or len(user_data["user_id"]) < 8 or len(user_data["user_id"]) > 12:
        userid_errors.append("Property 'user_id' must be between 8 and 12 characters long")
    userid_valid = len(userid_errors) == 0

    password_errors: list[str] = []
    if "password" not in user_data or len(user_data["password"]) < 8:
        password_errors.append("Property 'password' must be at least 8 characters long")
    if "password" not in user_data or not any(c.isdigit() for c in user_data["password"]):
        password_errors.append("Property 'password' must contain a digit")
    if "password" not in user_data or not any(c in "!\"£$%^&*()_+-=`¬|{}[]'#@~<>?,./]" for c in user_data["password"]):
        password_errors.append("Property 'password' must contain a special character")
    password_valid = len(password_errors) == 0

    email_errors: list[str] = []
    if "email" not in user_data or not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$", user_data["email"]):
        email_errors.append("Property 'email' must be a valid email address")
    email_valid = len(email_errors) == 0

    phone_errors: list[str] = []
    if "phone" not in user_data or len(user_data["phone"]) < 8 or len(user_data["phone"]) > 10:
        phone_errors.append("Property 'phone' must be between 8 and 10 characters long")
    if "phone" not in user_data or not user_data["phone"].isdigit():
        phone_errors.append("Property 'phone' must be only digits")
    phone_valid = len(phone_errors) == 0

    username_errors: list[str] = []
    if "username" not in user_data or len(user_data["username"]) < 3 or len(user_data["username"]) > 20:
        username_errors.append("Property 'username' must be between 3 and 20 characters long")
    if "username" not in user_data or not all(
        c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_" for c in user_data["username"]
    ):
        username_errors.append("Property 'username' must only contain alphanumerical characters or underscores")
    username_valid = len(username_errors) == 0

    firstname_errors: list[str] = []
    if (
        "firstname" not in user_data
        or len(user_data["firstname"]) < 2
        or not user_data["firstname"][0].isupper()
        or not user_data["firstname"][1:].islower()
    ):
        firstname_errors.append("Property 'firstname' must be a valid name")
    firstname_valid = len(firstname_errors) == 0

    lastname_errors: list[str] = []
    if (
        "lastname" not in user_data
        or len(user_data["lastname"]) < 2
        or not user_data["lastname"][0].isupper()
        or not user_data["lastname"][1:].islower()
    ):
        lastname_errors.append("Property 'lastname' must be a valid name")
    lastname_valid = len(lastname_errors) == 0

    address_errors: list[str] = []
    if "address1" not in user_data or len(user_data["address1"]) < 1 or len(user_data["address1"]) > 100:
        address_errors.append("Property 'address1' must be between 1 and 100 characters long")
    if "address2" not in user_data or len(user_data["address2"]) < 1 or len(user_data["address2"]) > 100:
        address_errors.append("Property 'address2' must be between 1 and 100 characters long")
    address_valid = len(address_errors) < 2

    postcode_errors: list[str] = []
    if "postcode" not in user_data or len(user_data["postcode"]) < 1 or len(user_data["postcode"]) > 10:
        postcode_errors.append("Property 'postcode' must be between 1 and 10 characters long")
    postcode_valid = len(postcode_errors) == 0

    user_contact_valid = email_valid or (phone_valid and username_valid)
    login_valid = (
        userid_valid
        and password_valid
        and user_contact_valid
        and firstname_valid
        and lastname_valid
        and address_valid
        and postcode_valid
    )

    is_valid = federation_valid or login_valid

    if is_valid:
        return True, ""

    line_and_indent: list[tuple[int, str]] = [
        (0, "At least one of the following user errors must be fixed:"),
    ]
    if not federation_valid:
        line_and_indent.append((1, "All of the following federation errors must be fixed:"))
        line_and_indent.extend([(2, error) for error in federation_errors])
    if not login_valid:
        line_and_indent.append((1, "All of the following login errors must be fixed:"))
        line_and_indent.extend([(2, error) for error in userid_errors])
        if not password_valid:
            line_and_indent.append((2, "All of the following password errors must be fixed:"))
            line_and_indent.extend([(3, error) for error in password_errors])
        if not user_contact_valid:
            line_and_indent.append((2, "At least one of the following user contact errors must be fixed:"))
            line_and_indent.extend([(3, error) for error in email_errors])
            if not phone_valid or not username_valid:
                line_and_indent.append((3, "All of the following non-email login errors must be fixed:"))
                line_and_indent.extend([(4, error) for error in phone_errors])
                line_and_indent.extend([(4, error) for error in username_errors])
        line_and_indent.extend([(2, error) for error in firstname_errors])
        line_and_indent.extend([(2, error) for error in lastname_errors])
        if not address_valid:
            line_and_indent.append((2, "At least one of the following address errors must be fixed:"))
            line_and_indent.extend([(3, error) for error in address_errors])
        line_and_indent.extend([(2, error) for error in postcode_errors])

    error_combined = "\n".join([f"{'\t' * indent}{error}" for indent, error in line_and_indent])

    return False, error_combined


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
