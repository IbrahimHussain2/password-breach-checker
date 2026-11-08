import unittest
from unittest.mock import patch
from checker import hash_password, check_password


class TestHashPassword(unittest.TestCase):

    def test_known_hash(self):
        # SHA-1 of "password" is well known, so we can check against it
        self.assertEqual(
            hash_password("password"),
            "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
        )

    def test_hash_is_40_chars(self):
        self.assertEqual(len(hash_password("anything")), 40)

    def test_hash_is_uppercase(self):
        result = hash_password("abc")
        self.assertEqual(result, result.upper())

    def test_small_change_gives_different_hash(self):
        self.assertNotEqual(hash_password("password"), hash_password("Password"))
class TestCheckPassword(unittest.TestCase):

    # suffix of "password" is 1E4C9B93F3F0682250B6CF8331B7EE68FD8
    @patch("checker.get_suffixes")
    def test_found_returns_count(self, fake_get):
        fake_get.return_value = [
            "003CD215739D7C1B2218670D26F81408237:2",
            "1E4C9B93F3F0682250B6CF8331B7EE68FD8:500",
        ]
        self.assertEqual(check_password("password"), 500)

    @patch("checker.get_suffixes")
    def test_not_found_returns_zero(self, fake_get):
        fake_get.return_value = ["003CD215739D7C1B2218670D26F81408237:2"]
        self.assertEqual(check_password("password"), 0)

    @patch("checker.get_suffixes")
    def test_only_prefix_is_sent(self, fake_get):
        fake_get.return_value = []
        check_password("password")
        fake_get.assert_called_once_with("5BAA6")

if __name__ == "__main__":
    unittest.main()
