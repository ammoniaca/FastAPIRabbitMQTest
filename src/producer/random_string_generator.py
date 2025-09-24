import string
from random import randint, choice

def random_string_generator(min_length: int, max_length: int):
    letters_and_digits = string.ascii_letters + string.digits
    random_string = "".join(choice(letters_and_digits) for _ in range(randint(min_length, max_length)))
    return random_string