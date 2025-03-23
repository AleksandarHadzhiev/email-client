from app.src.DTOs.login_dto import ExternalServiceLogin, EmailAndPasswordLogin

def test_pass_email():
        ext_ser_login = ExternalServiceLogin()
        incoming_data = {"email": "aleks@gamil.com"}
        ext_ser_login.set_value(data=incoming_data)
        output_data = ext_ser_login.get_values_as_dict()
        expected_result = {"email": incoming_data["email"]}
        assert output_data == expected_result


def test_pass_email_and_password():
        ext_ser_login = EmailAndPasswordLogin()
        incoming_data = {"email": "aleks@gamil.com", "password": "123"}
        ext_ser_login.set_value(data=incoming_data)
        output_data = ext_ser_login.get_values_as_dict()
        expected_result = {"email": incoming_data["email"], "password": incoming_data["password"]}
        assert output_data == expected_result


def test_wrong_email_key():
        ext_ser_login = ExternalServiceLogin()
        incoming_data = {"em": "aleks@gamil.com"}
        ext_ser_login.set_value(data=incoming_data)
        output_data = ext_ser_login.get_values_as_dict()
        expected_result = {"email": ""}
        assert output_data == expected_result


def test_wrong_password_key():
        ext_ser_login = EmailAndPasswordLogin()
        incoming_data = {"email": "aleks@gamil.com", "pass": "123"}
        ext_ser_login.set_value(data=incoming_data)
        output_data = ext_ser_login.get_values_as_dict()
        expected_result = {"email": incoming_data["email"], "password": ""}
        assert output_data == expected_result