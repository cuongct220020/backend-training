from pydantic import SecretStr, model_validator
from app.schemas import BaseSchema
from app.schemas.custom_types import PasswordStr
from app.exceptions import BadRequest

class ChangePasswordRequest(BaseSchema):
    old_password: SecretStr
    new_password: PasswordStr

    @model_validator(mode='after')
    def check_passwords_not_same(self) -> 'ChangePasswordRequest':
        if self.old_password.get_secret_value() == self.new_password.get_secret_value():
            raise BadRequest("New password cannot be the same as the old password.")
        return self