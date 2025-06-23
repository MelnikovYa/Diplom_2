import random
import string

def generate_random_user():
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@example.com"
    return {
        "email": email,
        "password": "password123",
        "name": "Test User"
    }