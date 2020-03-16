# SQLの接続、読み込みなどをする用

import psycopg2


# psqlに接続
def connect(self):
    self.conn = psycopg2.connect("host=127.0.0.1 dbname=food user=postgres password=postgres")#ここは変えてください
    self.cur = self.conn.cursor()


# sql文を実行
def query(self, text):
    self.cur.execute(text)
    return self.cur.fetchone()


# sql文(add)を実行
def add(self, text):
    self.cur.execute(text)
    self.conn.commit()
