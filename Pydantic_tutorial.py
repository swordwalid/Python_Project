from pydantic import BaseModel, EmailStr, field_validator

class User(BaseModel):
    name: str
    email: EmailStr  # instead of str we can set EmailStr to validate valid email
    account_id: int


user = User(name="jack", email="jackpot@pod.io", account_id=123)

print(user)
# result: name='jack' email='jackpot@pod.io' account_id=123

# Pydantic shows auto typehints

print(user.name)  # jack
print(user.email)  # jackpot@pod.io
print(user.account_id)  # 123

# Data validation using pydantic

user = User(name="jack", email="jackpot@pod.io", account_id="Hi")
print(user)
"""
result:  Input should be a valid integer,
unable to parse string as an integer [type=int_parsing, input_value='Hello', input_type=str]
"""

# Now we will validate email address!


user = User(name="Karl", email="abcd", account_id=123)

"""
result:  value is not a valid email address: The email address is not valid. 
It must have exactly one @-sign. [type=value_error, input_value='abcd', input_type=str]
"""


# Building a Custom Validator

class User(BaseModel):
    name: str
    email: EmailStr  # instead of str we can set EmailStr to validate valid email
    account_id: int

    # now will apply some conditions to validate account_id

    @field_validator("account_id")
    def validate_account_id(cls, value):
        if not (10030 < value < 20000):
            raise ValueError(f"account_id must be in between  10030 and 20000:{value}")
        return value


user = User(name="Karl", email="john.smith@example.com", account_id=11303)
"""
result:  1 validation error for User
account_id Value error, 
account_id must be in between  10030 and 20000:123 [type=value_error, input_value=123, input_type=int]
"""

# JSON Serialization using pydantic

user_json_str = user.json()
print(user_json_str)

"""
result:  {"name":"Karl","email":"john.smith@example.com","account_id":11303}
"""
# if we wanna get in form of dictionary

user_dict_obj=user.dict()
print(user_dict_obj)

"""
result:  {'name': 'Karl', 'email': 'john.smith@example.com', 'account_id': 11303}
"""

# so now if we have data in  json and we wanna get back in pydantic model:
json_format = '{"name":"Karl","email":"john.smith@example.com","account_id":11303}'
user = User.parse_raw(json_format)
print(user)

"""
result:  name='Karl' email='john.smith@example.com' account_id=11303
"""
