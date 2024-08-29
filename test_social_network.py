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

    def test_send_friend_request(self):
        # Test sending a friend request
        result = self.network.send_friend_request("alice", "bob")
        self.assertTrue(result)
        self.assertIn("bob", self.network.get_friends("alice", pending=True))

    def test_accept_friend_request(self):
        # Test accepting a friend request
        self.network.send_friend_request("alice", "bob")
        result = self.network.accept_friend_request("bob", "alice")
        self.assertTrue(result)
        self.assertIn("bob", self.network.get_friends("alice"))
        self.assertIn("alice", self.network.get_friends("bob"))

    def test_create_post(self):
        # Test creating a post
        result = self.network.create_post("alice", "This is a test post")
        self.assertTrue(result)
        self.assertEqual(len(self.network.posts), 1)
        self.assertEqual(self.network.posts[0]['content'], "This is a test post")

    def test_add_comment(self):
        # Test adding a comment to a post
        self.network.create_post("alice", "This is a test post")
        result = self.network.add_comment("bob", 1, "Nice post, Alice!")
        self.assertTrue(result)
        self.assertEqual(len(self.network.comments[1]), 1)
        self.assertEqual(self.network.comments[1][0]['content'], "Nice post, Alice!")

    def test_like_post(self):
        # Test liking a post
        self.network.create_post("alice", "This is a test post")
        result = self.network.like_post("bob", 1)
        self.assertTrue(result)
        self.assertEqual(len(self.network.posts[0]['likes']), 1)
        self.assertIn("bob", self.network.posts[0]['likes'])

    def test_like_comment(self):
        # Test liking a comment
        self.network.create_post("alice", "This is a test post")
        self.network.add_comment("bob", 1, "Nice post, Alice!")
        result = self.network.like_comment("alice", 1, 1)
        self.assertTrue(result)
        self.assertEqual(len(self.network.comments[1][0]['likes']), 1)
        self.assertIn("alice", self.network.comments[1][0]['likes'])

    def test_get_friends(self):
        # Test retrieving the list of friends
        self.network.send_friend_request("alice", "bob")
        self.network.accept_friend_request("bob", "alice")
        friends = self.network.get_friends("alice")
        self.assertEqual(friends, ["bob"])

    def test_no_duplicate_friends(self):
        # Test that accepting a friend request twice does not create duplicate friends
        self.network.send_friend_request("alice", "bob")
        self.network.accept_friend_request("bob", "alice")
        self.network.accept_friend_request("bob", "alice")  # Try accepting again
        friends = self.network.get_friends("alice")
        self.assertEqual(friends, ["bob"])  # Should still only be one friend

if __name__ == "__main__":
    unittest.main()
