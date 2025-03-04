import time


def validate_input(data: dict) -> dict:
    # The form of the incoming data:
    # {key: value} -> {email: "example@gmail.com", username: "example", password: "1103101103"}
    data = _check_if_its_full_data(data=data)
    if 'missing_keys' in data:
        return {"error": "Missing keys in incoming data", "missing_keys": data["missing_keys"]}

    data = _check_for_empty_input(data=data)
    if "empty_inputs" in data:
        return {"error": "There are empty fields in incoming data", "empty_inputs": data["empty_inputs"]}
    return "Stable"


def _check_if_its_full_data(data: dict)-> dict:
    expected_keys = ["email", "username", "password"]
    incoming_keys = list(data.keys())
    missing_keys = []
    for key in expected_keys:
        if key not in incoming_keys:
            missing_keys.append(key)
    if missing_keys.__len__() == 0:
        return data
    return {
        "missing_keys": missing_keys
    }


def _check_for_empty_input(data: dict) -> dict:
    incoming_keys = list(data.keys())
    empty_inputs = []
    for key in incoming_keys:
        if str(data[key]).strip() == "":
            empty_inputs.append(key)

    if empty_inputs.__len__() == 0:
        return data
    return {
        "empty_inputs": empty_inputs
    }



def test_validate_input_all_fields_missing():
    data = {"name": "Aleks"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["email","username", "password"]}
    assert response == expected_response


def test_validate_input_email_field_missing():
    data = {"username": "Aleks", "password": "1103"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["email"]}
    assert response == expected_response


def test_validate_input_username_field_missing():
    data = {"email": "Aleks", "password": "1103"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["username"]}
    assert response == expected_response


def test_validate_input_password_field_missing():
    data = {"email": "Aleks", "username": "Aleks"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["password"]}
    assert response == expected_response


def test_validate_input_username_and_pasword_fields_missing():
    data = {"email": "Aleks"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["username", "password"]}
    assert response == expected_response


def test_validate_input_email_and_pasword_fields_missing():
    data = {"username": "Aleks"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["email", "password"]}
    assert response == expected_response


def test_validate_input_email_and_username_fields_missing():
    data = {"password": "Aleks"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "Missing keys in incoming data", "missing_keys": ["email", "username"]}
    assert response == expected_response


def test_validate_input_empty_fields():
    data = {"username": "", "password": "", "email": ""}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["username", "password", "email"]}
    assert response == expected_response


def test_validate_input_email_empty_field():
    data = {"username": "s", "password": "s", "email": ""}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["email"]}
    assert response == expected_response


def test_validate_input_password_empty_field():
    data = {"username": "s", "password": "", "email": "s"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["password"]}
    assert response == expected_response


def test_validate_input_username_empty_field():
    data = {"username": "", "password": "s", "email": "s"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["username"]}
    assert response == expected_response



def test_validate_input_username_and_password_empty_fields():
    data = {"username": "", "password": "", "email": "s"}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["username", "password"]}
    assert response == expected_response


def test_validate_input_username_and_email_empty_fields():
    data = {"username": "", "password": "s", "email": ""}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["username", "email"]}
    assert response == expected_response



def test_validate_input_password_and_email_empty_fields():
    data = {"username": "s", "password": "", "email": ""}
    response = validate_input(data=data)
    time.sleep(10)
    expected_response = {"error": "There are empty fields in incoming data", "empty_inputs": ["password", "email"]}
    assert response == expected_response