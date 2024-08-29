class SocialNetwork:
    def __init__(self):
        # Initialize the in-memory data structures
        self.users = {}  # Stores user data: {username: {email, password, friends, posts}}
        self.posts = []  # Stores posts: [{post_id, user, content, likes}]
        self.comments = {}  # Stores comments: {post_id: [{user, content, likes}]}
        self.friend_requests = {}  # Stores friend requests: {username: [pending_friends]}

    def register_user(self, username, email, password):
        # Register a new user
        if username in self.users:
            return False  # Username already exists
        self.users[username] = {
            'email': email,
            'password': password,  # In a real application, you would hash the password
            'friends': [],
            'posts': []
        }
        return True

    def send_friend_request(self, from_user, to_user):
        # Send a friend request
        if to_user not in self.users or from_user not in self.users:
            return False  # One of the users does not exist
        if from_user in self.users[to_user]['friends']:
            return False  # They are already friends

        if to_user not in self.friend_requests:
            self.friend_requests[to_user] = []
        if from_user in self.friend_requests[to_user]:
            return False  # Friend request already sent
        self.friend_requests[to_user].append(from_user)
        return True

    def accept_friend_request(self, to_user, from_user):
        # Accept a friend request
        if to_user not in self.friend_requests or from_user not in self.friend_requests[to_user]:
            return False  # No such friend request
        self.users[to_user]['friends'].append(from_user)
        self.users[from_user]['friends'].append(to_user)
        self.friend_requests[to_user].remove(from_user)
        return True

    def get_friends(self, username, pending=False):
        # Get the list of friends (or pending friend requests if pending=True)
        if username not in self.users:
            return []
        if pending:
            return self.friend_requests.get(username, [])
        return self.users[username]['friends']

    def create_post(self, username, content):
        # Create a post by a user
        if username not in self.users:
            return False  # User does not exist
        post_id = len(self.posts) + 1
        post = {
            'post_id': post_id,
            'user': username,
            'content': content,
            'likes': set()  # Using a set to prevent duplicate likes
        }
        self.posts.append(post)
        self.users[username]['posts'].append(post)
        return True

    def add_comment(self, username, post_id, content):
        # Add a comment to a post
        if username not in self.users or post_id > len(self.posts) or post_id <= 0:
            return False  # User or post does not exist
        if post_id not in self.comments:
            self.comments[post_id] = []
        comment = {
            'user': username,
            'content': content,
            'likes': set()
        }
        self.comments[post_id].append(comment)
        return True

    def like_post(self, username, post_id):
        # Like a post
        if username not in self.users or post_id > len(self.posts) or post_id <= 0:
            return False  # User or post does not exist
        post = self.posts[post_id - 1]  # Post IDs are 1-based index
        if username in post['likes']:
            return False  # User has already liked this post
        post['likes'].add(username)
        return True

    def like_comment(self, username, post_id, comment_index):
        # Like a comment on a post
        if username not in self.users or post_id not in self.comments or comment_index >= len(self.comments[post_id]):
            return False  # User, post, or comment does not exist
        comment = self.comments[post_id][comment_index]
        if username in comment['likes']:
            return False  # User has already liked this comment
        comment['
