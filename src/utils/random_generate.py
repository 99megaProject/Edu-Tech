import random
char_str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
num_str = '0123456789'
special_str = '!@#$&'

def get_random_string(length=8):
    random_name = ''
    for j in range(2) :
        for i in range(2):
            random_name += random.choice(char_str)
        for i in range(1):
            random_name += random.choice(num_str)
        for i in range(1):
            random_name += random.choice(special_str)
     
    return random_name

