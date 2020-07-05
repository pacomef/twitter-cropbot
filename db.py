import MySQLdb

#conn = MySQLdb.connect(host='***REMOVED_DB_HOST***', user='***REMOVED_DB_USER***', password='***REMOVED_DB_PASSWORD***', database='***REMOVED_DB_NAME***')
template_query = "INSERT INTO crop (user, user_id, nb_img, past_tweet, new_tweet, removed_pixels, date) VALUES ('{0}', {1}, {2}, '{3}', '{4}', {5}, NOW())"


def query(req):
    conn = MySQLdb.connect(host='***REMOVED_DB_HOST***', user='***REMOVED_DB_USER***', password='***REMOVED_DB_PASSWORD***',
                           database='***REMOVED_DB_NAME***')
    cur = conn.cursor()
    cur.execute(req)
    cur.close()
    conn.commit()
    conn.close()
