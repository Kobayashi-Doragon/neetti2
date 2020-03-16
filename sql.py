# SQLの接続、読み込みなどをする用

import psycopg2


# psqlに接続
def connect(self):
    self.conn = psycopg2.connect("host=ec2-3-229-210-93.compute-1.amazonaws.com dbname=dee8l23t0g1dpi user=dokugxlaflejbo password=b9ee89b627b014f5aafb4d66cc4b67ab3f1fc486183a5b06775157c6e6e4cfab")#ここは変えてください
    self.cur = self.conn.cursor()


# sql文を実行
def query(self, text):
    self.cur.execute(text)
    return self.cur.fetchone()


# sql文(add)を実行
def add(self, text):
    self.cur.execute(text)
    self.conn.commit()
