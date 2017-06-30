import os
import random
import string

def string_generator(size, keyword, chars=string.ascii_uppercase + string.digits):
    insert_index = random.choice(range(size))
    result = ""
    for i in range(size):
        if i is insert_index:
            result +=keyword
        else:
            result += random.choice(chars)
    return result


if __name__ == "__main__":
    keywords = ["w10100", "w10101", "w10102", "w10103", "w10104",
                "w10105", "w10106", "w10107", "w10108", "w10109"]

    # create directory
    for keyword in keywords:
        cur_path = os.path.join(os.getcwd(), keyword)
        if not os.path.exists(cur_path):
            os.mkdir(cur_path)

    # create test files
    for keyword in keywords:
        for i in range(1000):
            open(os.path.join(os.getcwd(), string_generator(10, keyword)), "a").close()