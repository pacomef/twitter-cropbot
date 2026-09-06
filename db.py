import os
import MySQLdb

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

template_query = "INSERT INTO crop (user, user_id, nb_img, past_tweet, new_tweet, removed_pixels, date) VALUES ('{0}', {1}, {2}, '{3}', '{4}', {5}, NOW())"


def query(req):
    conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD,
                           database=DB_NAME)
    cur = conn.cursor()
    cur.execute(req)
    cur.close()
    conn.commit()
    conn.close()
