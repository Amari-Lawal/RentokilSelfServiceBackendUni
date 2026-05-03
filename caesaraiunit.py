import unittest

import requests

uri = (
    "http://127.0.0.1:8080"  # "https://blacktechdivisionreward-hrjw5cc7pa-uc.a.run.app"
)


class CaesarAIUnittest(unittest.TestCase):
    def test_message(self):
        response = requests.get(
            f"{uri}/sendmessage", params={"message": "hello world"}, timeout=10
        )
        self.assertEqual(response.json().get("error"), None)
        self.assertNotEqual(
            response.json().get("error"),
            "you have already done this action can't gain tokens.",
        )


if __name__ == "__main__":
    unittest.main()
