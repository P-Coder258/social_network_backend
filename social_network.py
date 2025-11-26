import logging

# Configure logging to show timestamps and error levels
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SocialNetwork:
    def __init__(self):
        # Initialize the in-memory data structures
        self.users = {}  # Stores user data: {username: {email, password, friends, posts}}
        self.posts = []  # Stores posts: [{post_id, user, content, likes}]
        self.comments = {}  # Stores comments: {post_id: [{user, content, likes}]}
        self.friend_requests = {}  # Stores friend requests: {username: [pending_friends]}

    def register_user(self, username, email, password):
        try:
            if not isinstance(username, str) or not isinstance(email, str):
                raise ValueError("Invalid data type for registration")

            if username in self.users:
                logging.warning(f"Registration Failed: Username '{username}' already taken.")
                return False
            
            self.users[username] = {
                'email': email,
                'password': password, 
                'friends': [],
                'posts': []
            }
            logging.info(f"User Registered: {username}")
            return True
        except Exception as e:
            logging.error(f"CRITICAL ERROR in register_user: {str(e)}")
            return False

    def send_friend_request(self, from_user, to_user):
        try:
            if to_user not in self.users or from_user not in self.users:
                logging.warning(f"Friend Request Failed: One or more users do not exist.")
                return False
            if from_user in self.users[to_user]['friends']:
                logging.info(f"Friend Request Skipped: {from_user} and {to_user} are already friends.")
                return False
                
            if to_user not in self.friend_requests:
                self.friend_requests[to_user] = []
            
            if from_user in self.friend_requests[to_user]:
                return False 
            
            self.friend_requests[to_user].append(from_user)
            logging.info(f"Friend Request Sent: {from_user} -> {to_user}")
            return True
        except Exception as e:
            logging.error(f"Error in send_friend_request: {e}")
            return False

    def accept_friend_request(self, to_user, from_user):
        try:
            # Check if request exists
            if to_user not in self.friend_requests or from_user not in self.friend_requests[to_user]:
                logging.warning(f"Accept Friend Failed: No request from {from_user} to {to_user}")
                return False 
            
            # Update friend lists
            self.users[to_user]['friends'].append(from_user)
            self.users[from_user]['friends'].append(to_user)
            self.friend_requests[to_user].remove(from_user)
            
            logging.info(f"Friend Request Accepted: {to_user} <-> {from_user}")
            return True
        except Exception as e:
            logging.error(f"CRITICAL ERROR in accept_friend_request: {e}")
            return False

    def get_friends(self, username, pending=False):
        try:
            if username not in self.users:
                logging.warning(f"Get Friends Failed: User '{username}' not found.")
                return []
            
            if pending:
                return self.friend_requests.get(username, [])
            return self.users[username]['friends']
        except Exception as e:
            logging.error(f"Error retrieving friends for {username}: {e}")
            return []

    def create_post(self, username, content):
        try:
            if username not in self.users:
                return False
            
            # Prevent empty posts to save storage/maintain quality
            if not content or len(content.strip()) == 0:
                logging.warning(f"Post Creation Failed: Empty content from {username}")
                return False

            post_id = len(self.posts) + 1
            post = {
                'post_id': post_id,
                'user': username,
                'content': content,
                'likes': set()
            }
            self.posts.append(post)
            self.users[username]['posts'].append(post)
            
            logging.info(f"Post Created: ID {post_id} by {username}")
            return True
        except Exception as e:
            logging.error(f"Error in create_post: {e}")
            return False

    def add_comment(self, username, post_id, content):
        try:
            # Validate inputs before processing
            if username not in self.users: 
                return False
            if post_id > len(self.posts) or post_id <= 0:
                logging.warning(f"Comment Failed: Invalid Post ID {post_id}")
                return False 
            
            if post_id not in self.comments:
                self.comments[post_id] = []
            
            comment = {
                'user': username, 
                'content': content, 
                'likes': set()
            }
            self.comments[post_id].append(comment)
            logging.info(f"Comment Added: User {username} on Post {post_id}")
            return True
        except Exception as e:
            logging.error(f"Error in add_comment: {e}")
            return False

    def like_post(self, username, post_id):
        try:
            if username not in self.users: 
                return False
            if post_id > len(self.posts) or post_id <= 0:
                return False 
            
            post = self.posts[post_id - 1] 
            if username in post['likes']:
                logging.info(f"Duplicate Like Ignored: {username} on Post {post_id}")
                return False 
            
            post['likes'].add(username)
            return True
        except Exception as e:
            logging.error(f"Error in like_post: {e}")
            return False

    def like_comment(self, username, post_id, comment_index):
        try:
            if username not in self.users or post_id not in self.comments:
                return False
            
            # Check index bounds to prevent crash
            if comment_index < 0 or comment_index >= len(self.comments[post_id]):
                logging.warning(f"Like Comment Failed: Invalid comment index {comment_index}")
                return False 
            
            comment = self.comments[post_id][comment_index] 
            if username in comment['likes']:
                return False 
            
            comment['likes'].add(username)
            return True
        except Exception as e:
            logging.error(f"Error in like_comment: {e}")
            return False
