import time


def fetch_db():
    for i in range(0, 1000):
        time.sleep(.1)
        yield i


data = fetch_db()
for i in data:
    print(i)
