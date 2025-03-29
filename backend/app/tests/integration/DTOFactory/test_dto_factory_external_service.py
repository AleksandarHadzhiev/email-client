from app.src.DTOs.DTOFactory import DTOFactory
from app.src.DTOs.login_dto import ExternalServiceLogin, EmailAndPasswordLogin

def test_fail_empty_keys():
    dto_factory = DTOFactory({"": ""})
    response = dto_factory.get_dto_based_on_incoming_data()
    expected_output = {'fail': 'The incomind data is not supported format.'}
    assert response == expected_output


def test_fail_format_not_supported():
    dto_factory = DTOFactory({"meow": ""})
    response = dto_factory.get_dto_based_on_incoming_data()
    expected_output = {'fail': 'The incomind data is not supported format.'}
    assert response == expected_output


def test_success_for_external_service_login():
    dto_factory = DTOFactory({"email": ""})
    response = dto_factory.get_dto_based_on_incoming_data()
    assert type(response) == type(ExternalServiceLogin())



def test_success_for_external_service_login_with_password():
    dto_factory = DTOFactory({"email": "", "password": ""})
    response = dto_factory.get_dto_based_on_incoming_data()
    assert type(response) == type(EmailAndPasswordLogin())