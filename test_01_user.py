import pytest
import json
from my_requests import MyRequests
from basic_assertions import Response
from shemas.user_schema import user_schema
from shemas.error_schema import error_schema

error_message_str = "str type expected"
error_message_str_min_length = "ensure this value has at least 1 characters"
error_message_str_max_length = "ensure this value has at most 100 characters"
error_message_int = "value is not a valid integer"
error_message_int_min_value = "ensure this value is greater than or equal to 0"
error_message_int_max_value = "ensure this value is less than or equal to 100"
error_required_field = "field required"


class TestUser:

    name_create = [
        ("user_1"),
        (""),
        ("femjjddcsidtzsurnzucxzwrynyuecqrzazxgkwarantzxuunaysmotodaqatdumyhinncjxbuufzjtwmimmfmvnjrnzxjagzxyvl"),
        (123)
    ]

    age_create = [
        (31),
        ("31"),
        (-1),
        (101)
    ]

    name_update = [
        ("user_1_updated"),
        (""),
        ("femjjddcsidtzsurnzucxzwrynyuecqrzazxgkwarantzxuunaysmotodaqatdumyhinncjxbuufzjtwmimmfmvnjrnzxjagzxyvl"),
        (123)
    ]

    age_update = [
        (51),
        ("31_updated"),
        (-1),
        (101)
    ]

    def test_GET_get_all_users_without_params_start_200(self):
        response = MyRequests.get(f'/user')
        Response.check_json_schema_status_code_content_type(
            response, 200, user_schema)

    @pytest.mark.parametrize('name_create', name_create)
    def test_POST_create_user_check_name(self, name_create):
        data = json.dumps(
            {"name": name_create, "age": 18})
        response = MyRequests.post("/user/create", data=data)
        response_dict = response.json()
        if type(name_create) == int:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_str, "Wrong error message"
        elif len(name_create) == 0:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_str_min_length, "Wrong error message"
        elif len(name_create) > 100:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_str_max_length, "Wrong error message"
        else:
            # get global variable of first created user
            pytest.user_id_1 = response_dict["result"]
            Response.check_json_schema_status_code_content_type(
                response, 200, user_schema)
            assert TestUser.name_create[0] == response_dict["result"]["name"], "Wrong name in response"
            assert 18 == response_dict["result"]["age"], "Wrong age in response"

    @pytest.mark.parametrize('age_create', age_create)
    def test_POST_create_user_check_age(self, age_create):
        data = json.dumps(
            {"name": "user_2", "age": age_create})
        response = MyRequests.post("/user/create", data=data)
        response_dict = response.json()
        if type(age_create) == str:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_int, "Wrong error message"
        elif age_create < 0:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_int_min_value, "Wrong error message"
        elif age_create > 100:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_int_max_value, "Wrong error message"
        else:
            # get global variable of second created user
            pytest.user_id_2 = response_dict["result"]
            Response.check_json_schema_status_code_content_type(
                response, 200, user_schema)
            assert "user_2" == response_dict["result"]["name"], "Wrong name in response"
            assert TestUser.age_create[0] == response_dict["result"]["age"], "Wrong age in response"

    def test_POST_create_user_with_no_required_body_422(self):
        response = MyRequests.post("/user/create")
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_required_field, "Wrong error message"

    def test_POST_create_user_name_empty_key_422(self):
        data = json.dumps({"": "user_3", "age": 18})
        response = MyRequests.post("/user/create", data=data)
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_required_field, "Wrong error message"

    def test_POST_create_user_age_empty_key_422(self):
        data = json.dumps({"name": "user_3", "": 18})
        response = MyRequests.post("/user/create", data=data)
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_required_field, "Wrong error message"

    def test_POST_create_user_for_removing_200(self):
        data = json.dumps({"name": "user_3", "age": 18})
        response = MyRequests.post("/user/create", data=data)
        response_dict = response.json()
        pytest.user_id_3 = response_dict["result"]
        Response.check_json_schema_status_code_content_type(
            response, 200, user_schema)
        assert "user_3" == response_dict["result"]["name"], "Wrong name in response"
        assert 18 == response_dict["result"]["age"], "Wrong age in response"

    def test_DELETE_user_by_id_200(self):
        response = MyRequests.delete(f'/user/{pytest.user_id_3["id"]}')
        Response.check_json_schema_status_code_content_type(
            response, 200, user_schema)

    def test_DELETE_user_by_deleted_id_200(self):
        response = MyRequests.delete(f'/user/{pytest.user_id_3["id"]}')
        Response.check_json_schema_status_code_content_type(
            response, 404, error_schema)

    def test_DELETE_user_not_valid_user_id_path_422(self):
        response = MyRequests.delete(f'/user/text')
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_message_int, "Wrong error message"

    def test_GET_user_by_id_200(self):
        response = MyRequests.get(f'/user/{pytest.user_id_1["id"]}')
        Response.check_json_schema_status_code_content_type(
            response, 200, user_schema)

    def test_GET_user_by_deleted_id_200(self):
        response = MyRequests.get(f'/user/{pytest.user_id_3["id"]}')
        Response.check_json_schema_status_code_content_type(
            response, 404, error_schema)

    def test_GET_user_not_valid_user_id_path_422(self):
        response = MyRequests.get(f'/user/text')
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_message_int, "Wrong error message"

    @pytest.mark.parametrize('name_update', name_update)
    def test_PUT_update_user_check_name(self, name_update):
        data = json.dumps({"name": name_update, "age": 18})
        response = MyRequests.put(f'/user/{pytest.user_id_1["id"]}', data=data)
        response_dict = response.json()
        if type(name_update) == int:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_str, "Wrong error message"
        elif len(name_update) == 0:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_str_min_length, "Wrong error message"
        elif len(name_update) > 100:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_str_max_length, "Wrong error message"
        else:
            # get global variable of first updated user
            pytest.user_id_1 = response_dict["result"]
            Response.check_json_schema_status_code_content_type(
                response, 200, user_schema)
            assert TestUser.name_update[0] == response_dict["result"]["name"], "Wrong name in response"
            assert 18 == response_dict["result"]["age"], "Wrong age in response"

    @pytest.mark.parametrize('age_update', age_update)
    def test_PUT_update_user_check_age(self, age_update):
        data = json.dumps({"name": "user_2_updated", "age": age_update})
        response = MyRequests.put(f'/user/{pytest.user_id_2["id"]}', data=data)
        response_dict = response.json()
        if type(age_update) == str:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_int, "Wrong error message"
        elif age_update < 0:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_int_min_value, "Wrong error message"
        elif age_update > 100:
            Response.check_json_schema_status_code_content_type(
                response, 422, error_schema)
            assert response_dict["detail"][0]["msg"] == error_message_int_max_value, "Wrong error message"
        else:
            # get global variable of second updated user
            pytest.user_id_2 = response_dict["result"]
            Response.check_json_schema_status_code_content_type(
                response, 200, user_schema)
            assert "user_2_updated" == response_dict["result"]["name"], "Wrong name in response"
            assert TestUser.age_update[0] == response_dict["result"]["age"], "Wrong age in response"

    def test_PUT_update_user_with_no_required_body_422(self):
        response = MyRequests.put(f'/user/{pytest.user_id_2["id"]}')
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_required_field, "Wrong error message"

    def test_PUT_update_user_name_empty_key_422(self):
        data = json.dumps({"": "user_3", "age": 18})
        response = MyRequests.put(f'/user/{pytest.user_id_2["id"]}', data=data)
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_required_field, "Wrong error message"

    def test_PUT_update_user_age_empty_key_422(self):
        data = json.dumps({"name": "user_3", "": 18})
        response = MyRequests.put(f'/user/{pytest.user_id_2["id"]}', data=data)
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_required_field, "Wrong error message"

    def test_PUT_update_user_by_deleted_id_200(self):
        data = json.dumps({"name": "user_3_updated", "age": 18})
        response = MyRequests.put(f'/user/{pytest.user_id_3["id"]}', data=data)
        Response.check_json_schema_status_code_content_type(
            response, 404, error_schema)

    def test_PUT_update_user_not_valid_user_id_path_422(self):
        data = json.dumps({"name": "user_3_updated", "age": 18})
        response = MyRequests.put(f'/user/text', data=data)
        response_dict = response.json()
        Response.check_json_schema_status_code_content_type(
            response, 422, error_schema)
        assert response_dict["detail"][0]["msg"] == error_message_int, "Wrong error message"

    def test_GET_get_all_users_without_params_end_200(self):
        response = MyRequests.get(f'/user')
        Response.check_json_schema_status_code_content_type(
            response, 200, user_schema)
