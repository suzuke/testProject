import multiprocessing

def task(keyword):
    print(keyword)
    return keyword

def main():
    keywords = ["w10100", "w10101", "w10102", "w10103", "w10104",
                "w10105", "w10106", "w10107", "w10108", "w10109"]
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool()

    pool.map(task, (keywords,))


if __name__ == '__main__':
    main()
