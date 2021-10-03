import timeit

print(timeit.timeit(setup="import psycopg2", stmt="""
with psycopg2.connect(dbname = "postgres", user = "postgres", host = "db", port = "5432", password = "123456") as conn:
    with conn.cursor() as curs:
        curs.execute("INSERT INTO test(name) VALUES ('test');")
"""), number=10000)