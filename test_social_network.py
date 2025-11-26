import unittest
from social_network import SocialNetwork

class TestSocialNetwork(unittest.TestCase):

    def setUp(self):
        # Set up the Social Network and add some initial users
        self.network = SocialNetwork()
        self.network.register_user("alice", "alice@example.com", "password123")
        self.network.register_user("bob", "bob@example.com", "password456")
        self.network.register_user("charlie", "charlie@example.com", "password789")

    def test_register_user(self):
        # Test user registration
        result = self.network.register_user("dave", "dave@example.com", "password012")
        self.assertTrue(result)
        self.assertIn("dave", self.network.users)

    def test_duplicate_user_registration(self):
        # Test duplicate user registration (should fail)
        result = self.network.register_user("alice", "alice@example.com", "password123")
        self.assertFalse(result)  # Expecting False because "alice" already exists

    def test_send_and_accept_friend_request(self):
        self.network.send_friend_request("alice", "bob")
        result = self.network.accept_friend_request("bob", "alice")
        self.assertTrue(result)
        self.assertIn("bob", self.network.get_friends("alice"))

    def test_registration_invalid_types(self):
        # Passing an integer instead of a username string
        result = self.network.register_user(12345, "fail@example.com", "pass")
        self.assertFalse(result) # Should fail gracefully, not raise Python error

    def test_empty_post_content(self):
        # Verify validation logic rejects empty posts
        result = self.network.create_post("alice", "")
        self.assertFalse(result)

    def test_friend_request_non_existent_user(self):
        # Verify logic handles requests to missing users
        result = self.network.send_friend_request("alice", "GHOST_USER")
        self.assertFalse(result)

    
if __name__ == "__main__":
    unittest.main()
