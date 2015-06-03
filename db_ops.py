#!usr/bin/python
import psycopg2
import datetime


def update_database(quote):
    try:
        conn = psycopg2.connect("dbname=quotesdb user=vinodpankajakshan")
        cur = conn.cursor()
        cur.execute("""
                    INSERT INTO quotes (description, created_date, authorid)
                    values (%s, %s, %s)
                    """, (quote, datetime.date.today(), 1))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as ex:
        raise ex
