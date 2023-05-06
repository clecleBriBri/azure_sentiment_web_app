import psycopg2
import os


class DBSentiment:
    def connect(self):
        return psycopg2.connect(
            host="c.cluster-jc-review.postgres.database.azure.com",
            database="citus",
            user="citus",
            password=os.environ["DB_PASSWORD"],
        )

    def show_all(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM sentiments")

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    def get_column_names(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'sentiments'"
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    def delete_by_name(self, name: str):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM sentiments WHERE movie = %s", (name,))

        conn.commit()

        cur.close()
        conn.close()

    def add_to_db(self, name: str, sentiment: str):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO sentiments (movie, sentiment) VALUES (%s, %s)",
            (name, sentiment),
        )

        conn.commit()

        cur.close()
        conn.close()

    def get_movie(self, name):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("SELECT * FROM sentiments WHERE movie = %s", (name,))

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows
