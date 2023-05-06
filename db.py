import psycopg2
class DBSentiment:
    def init(self, sentiment: str, score: float):
        self.conn = psycopg2.connect(
            host="c.cluster-jc-review.postgres.database.azure.com",
            database="citus",
            user="citus",
            password="pass123!"
        )

    def delete_by_name(self, name: str):
        cur = self.conn.cursor()

        cur.execute("DELETE FROM sentiments WHERE sentiment = %s", (name))

        self.conn.commit()

        cur.close()
        self.conn.close()

    def add_to_db(self, name: str, sentiment: str):
        cur = self.conn.cursor()

        cur.execute("INSERT INTO sentiments VALUES (%s, %s)", (name, sentiment))

        self.conn.commit()

        cur.close()
        self.conn.close()

    def getAll(self):
        cur = self.conn.cursor()

        cur.execute("SELECT * FROM sentiments")

        rows = cur.fetchall()

        cur.close()
        self.conn.close()
