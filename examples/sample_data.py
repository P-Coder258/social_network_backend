from social_network import SocialNetwork

def load_sample_data(network):
    # Register users
    network.register_user("alice", "alice@example.com", "password123")
    network.register_user("bob", "bob@example.com", "password456")
    network.register_user("charlie", "charlie@example.com", "password789")
    network.register_user("dave", "dave@example.com", "password012")

    # Establish friendships
    network.send_friend_request("alice", "bob")
    network.accept_friend_request("bob", "alice")
    network.send_friend_request("charlie", "alice")
    network.accept_friend_request("alice", "charlie")

    # Create posts
    network.create_post("alice", "Hello, this is Alice!")
    network.create_post("bob", "Hey everyone, Bob here!")
    network.create_post("charlie", "Good day to all!")

    # Add comments to posts
    network.add_comment("bob", 1, "Nice to see you here, Alice!")
    network.add_comment("alice", 2, "Hi Bob, welcome!")
    network.add_comment("dave", 3, "Hi Charlie, good day to you too!")

    # Like posts
    network.like_post("charlie", 1)  # Charlie likes Alice's post
    network.like_post("alice", 2)    # Alice likes Bob's post
    network.like_post("bob", 3)      # Bob likes Charlie's post

    # Like comments
    network.like_comment("alice", 1, 1)  # Alice likes Bob's comment on her post
    network.like_comment("charlie", 2, 1)  # Charlie likes Alice's comment on Bob's post

if __name__ == "__main__":
    # Create a new social network instance
    network = SocialNetwork()

    # Load sample data into the network
    load_sample_data(network)

    # Display the users and their friends
    print("\nUsers and their friends:")
    for user in network.users:
        print(f"{user}: {network.get_friends(user)}")

