import random
import string

def generate_random_string():
    chars = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(chars) for _ in range(3))
    return random_string

print(generate_random_string())