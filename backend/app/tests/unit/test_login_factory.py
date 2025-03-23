from app.src.DTOs.login_dto import ExternalServiceLogin

def test_pass():
        ext_ser_login = ExternalServiceLogin()
        incoming_data = {"email": "aleks@gamil.com"}
        ext_ser_login.set_value(data=incoming_data)
        output_data = ext_ser_login.get_values_as_dict()
        expected_result = {"email": incoming_data["email"]}
        assert output_data == expected_result
