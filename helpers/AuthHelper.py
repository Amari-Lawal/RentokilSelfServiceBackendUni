from blustorymicroservices.BluStoryAccounts.settings.config import get_settings
import string
import secrets
import random


class AuthHelper:
    @staticmethod
    def create_random_username(length: int = 10) -> str:
        settings = get_settings()
        alphabet = string.ascii_lowercase + string.digits
        return settings.operator.prefix + "".join(
            secrets.choice(alphabet) for _ in range(length)
        )

    @staticmethod
    def create_random_password(length: int = 20) -> str:
        if length < 8:
            raise ValueError("Password length should be at least 8")

        lowercase = secrets.choice(string.ascii_lowercase)
        uppercase = secrets.choice(string.ascii_uppercase)
        digit = secrets.choice(string.digits)
        symbol = secrets.choice("!@#$%^&*()-+")

        remaining_length = length - 4
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-+"

        remaining = [secrets.choice(alphabet) for _ in range(remaining_length)]

        password_list = [lowercase, uppercase, digit, symbol] + remaining

        random.SystemRandom().shuffle(password_list)

        return "".join(password_list)
