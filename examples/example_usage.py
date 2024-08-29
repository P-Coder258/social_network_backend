from social_network import SocialNetwork

# Create a new social network instance
network = SocialNetwork()

# Register users
network.register_user("alice", "alice@example.com", "password123")
network.register_user("bob", "bob@example.com", "password456")

# Send a friend request
network.send_friend_request("alice", "bob")

# Alice makes a post
network.create_post("alice", "Hello, world!")

# Bob likes Alice's post
network.like_post("bob", 1)
