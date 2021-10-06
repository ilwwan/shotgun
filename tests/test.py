import psycopg2
import random
import string
import time

def test(connections, transactions):
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="db")
    ts = time.perf_counter()
    for t in range(transactions):
        with conn.cursor() as c:
            c.execute(generate_transaction())
    te = time.perf_counter() - ts
    print(f"Took {te-ts} seconds to perform {transactions} transactions")
    print(f"Transactions per second : {transactions/(te-ts)}")


def generate_transaction():
    return "INSERT INTO shotgun_cotisant_entry(first_name, last_name, email, phone_number, vr_username) VALUES ({}, {}, {}, {}, {})".format(
        (randstr(10), randstr(10), randstr(10), randstr(10), randstr(10))
    )

def randstr(x):
    return "".join(random.choice(string.ascii_letters) for _ in range(x))

if __name__ == "__main__":
    test()