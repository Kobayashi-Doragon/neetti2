# 各メソッドを用意する用
import sql
import random
from flask import Flask, render_template, request, make_response


class player():
    # コンストラクタ
    def __init__(self):
        self.player_id = 0
        self.mother_fatigue = 0
        self.money = 1000
        self.neet_fulness = 0
        self.neet_motivation = 0
        self.time = True
        self.count = 1

        self.foods = []  # 表示する食事のリスト()
        self.buys = []  # 表示する商品のリスト
        self.talks = []
        self.foods_id = []  # foods[i]のデータベース上のidがfoods_id[i]
        self.buys_id = []
        self.talks_id = []

        sql.connect(self)
        self.clean = False

    # データベースの値を表示するために取得(追加したメソッド)
    def update_data(self):

        # random.seed(2 * self.count + self.time+int(self.player_id))
        self.foods_id = random.sample(range(1, 40), 5)
        self.buys_id = random.sample(range(1, 40), 5)
        self.talks_id = random.sample(range(1, 40), 5)
        self.foods.clear()
        self.buys.clear()
        self.talks.clear()

        for item in self.foods_id:  # データの読み込み
            check = "select food_name from food1 where food_id = '" + str(item) + "'"
            check2 = "select food_price from food1 where food_id = '" + str(item) + "'"
            name = sql.query(self, check)
            price = sql.query(self, check2)
            self.foods.append({'name': name[0], 'price': price[0]})  # foods(配列)にデータを追加

        for item in self.buys_id:  # データの読み込み
            check = "select buy_name from buy where buy_id = '" + str(item) + "'"
            check2 = "select buy_price from buy where buy_id = '" + str(item) + "'"
            name = sql.query(self, check)
            price = sql.query(self, check2)
            self.buys.append({'name': name[0], 'price': price[0]})  # buys(配列)にデータを追加

        for item in self.talks_id:  # データの読み込み
            check = "select talk_sentence from talk where talk_id = '" + str(item) + "'"
            name = sql.query(self, check)
            self.talks.append(name[0])


    # 入力を元にログインしてゲーム画面に
    def login(self, id, password):
        # DBと入力を照合(true or false)
        text = "select exists(select * from users where player_id = '" + id + "');"
        result = sql.query(self, text)

        # ユーザIDが重複するとき
        if result[0]:
            text = "select * from users where player_id = " + id
            result = sql.query(self, text)
            if result[1] == password:
                self.player_id = id
                self.mother_fatigue = result[2]
                self.money = result[3]
                self.time = result[4]
                self.neet_fulness = result[5]
                self.neet_motivation = result[6]
                self.count = result[7]
                return True
            else:
                return False
        # ユーザIDが重複しないとき
        else:
            return False


    # 入力を元にアカウントの作成
    def create(self, id, password):
        text = "select exists(select * from users where player_id = " + id + ");"
        result = sql.query(self, text)

        # ユーザIDが重複するとき
        if result[0]:
            return False

        else:  # ユーザIDが重複しないとき
            text = "insert into users values(" + id + ",'" + password + "',0,1000,True,0,0,1);"
            sql.add(self, text)
            self.player_id = id
            return True


    # ステータスをDBに格納
    def save(self):
        if self.time:
            time_bool = "True"
        else:
            time_bool = "False"

        # selfのステータスをDBに格納
        text = "update users set mother_fatigue=" + str(self.mother_fatigue) + ",money=" +\
               str(self.money) + ",time='"+ time_bool +"',neet_fulness=" + str(self.neet_fulness) +\
               ",neet_motivation=" + str(self.neet_motivation) + ",count=" + str(self.count) +\
               " where player_id=" + str(self.player_id) + ";"
        sql.add(self, text)
        return True


    # 話しかけたとき
    def talk(self, talk_id):
        self.mother_fatigue += 10
        if self.neet_fulness < -100:  # お腹がすいている場合の返事(追加)
            self.neet_motivation -= 10
            return "お腹がすいた"
        else:  # DBのtalkテーブルからニートの返事を選択
            text = "select * from talk where talk_id = '" + str(self.talks_id[int(talk_id)]) + "'"
            result = sql.query(self, text)
            rand_int = random.randint(0, 1)
            self.neet_motivation += result[3][rand_int]
            self.talks.pop(int(talk_id))
            self.talks_id.pop(int(talk_id))
            return result[2][rand_int]


    # 食事を与えたとき
    def feed(self, food_id):
        # お金が足りるか確認用
        check = "select food_price from food1 where food_id = '" + str(self.foods_id[int(food_id)]) + "'"  # 変更箇所
        price = sql.query(self, check)[0]
        self.mother_fatigue -= 50

        # お金が足りないときエラーメッセージ
        if self.money - price < 0:
            return "(お金が足りない)"
        else:
            text = "select * from food1 where food_id = '" + str(self.foods_id[int(food_id)]) + "'"  # 変更箇所
            result = sql.query(self, text)
            self.money -= price
            self.neet_fulness += 100
            self.neet_motivation += result[3]
            self.foods.pop(int(food_id))
            self.foods_id.pop(int(food_id))
            return "(" + result[1] + "をあげた)"


    # 物を買ってあげたとき
    def buy(self, buy_id):
        # お金が足りるか確認用
        check = "select buy_price from buy where buy_id = '" + str(self.buys_id[int(buy_id)]) + "'"  # 変更箇所
        price = sql.query(self, check)[0]
        self.mother_fatigue -= 30

        # お金が足りないときエラーメッセージ
        if self.money - price < 0:
            return "(お金が足りない)"
        else:
            text = "select * from buy where buy_id = '" + str(self.buys_id[int(buy_id)]) + "'"  # 変更箇所
            result = sql.query(self, text)
            self.money -= price
            self.neet_motivation += result[3]
            self.buys.pop(int(buy_id))
            self.buys_id.pop(int(buy_id))
            return "(" + result[1] + "をあげた)"


    # 仕事に行ったとき
    def work(self):
        # ステータス(時間、疲労度、お金)を更新
        self.time = False
        self.neet_fulness -= 20
        if self.mother_fatigue < -500:  # 疲労度が一定以下の場合
            self.mother_fatigue -= 100
            return "(疲れが溜まっていて、仕事に行かず寝てしまった)"
        else:  # 疲労度が一定以上の場合
            self.mother_fatigue -= 50
            if self.count % 7 == 0:
                self.money += 10000
                self.mother_fatigue -= 50
                return "(仕事に行ってきた。今日はいつもより多く働いた)"
            else:
                self.money += 2000
                return "(仕事に行ってきた)"


    # 寝たとき
    def sleep(self):
        # ステータス(時間、疲労度)を更新
        self.time = True
        self.clean = False
        self.count += 1
        self.neet_fulness -= 30
        if self.count % 6 == 1:
            self.mother_fatigue += 30
            return "(あまり眠れなかった)"
        else:
            self.mother_fatigue += 100
            return "(ぐっすり眠れた)"


    # ニートの機嫌を確認
    def check_neet(self):
        if self.neet_motivation >= 1000:
            return True
        else:
            return False


    # 各クライアントにcookieでゲームデータを保存する
    def set_cookies(self, response):
        response.set_cookie('player_id', value=str(self.player_id))
        response.set_cookie('mother_fatigue', value=str(self.mother_fatigue))
        response.set_cookie('money', value=str(self.money))
        response.set_cookie('neet_fulness', value=str(self.neet_fulness))
        response.set_cookie('neet_motivation', value=str(self.neet_motivation))
        response.set_cookie('time', value=str(self.time))
        response.set_cookie('count', value=str(self.count))

        # 配列を","でつないだ文字列でcookieに保存
        text=""
        for i in range(len(self.foods)):
            text += self.foods[i]['name'] + ','
            text += str(self.foods[i]['price']) + ','
        response.set_cookie('foods', value=text)
        text = ""
        for i in range(len(self.buys)):
            text += self.buys[i]['name'] + ','
            text += str(self.buys[i]['price']) + ','
        response.set_cookie('buys', value=text)
        text = ""
        for i in range(len(self.talks)):
            text += self.talks[i] + ','
        response.set_cookie('talks', value=text)

        response.set_cookie('foods_id', value=str(self.foods_id))
        response.set_cookie('buys_id', value=str(self.buys_id))
        response.set_cookie('talks_id', value=str(self.talks_id))
        response.set_cookie('clean', value=str(self.clean))
        return response


    #　各クライアントからcookieでゲームデータを取得する
    def get_cookies(self):
        self.player_id = int(request.cookies.get('player_id', None))
        self.mother_fatigue = int(request.cookies.get('mother_fatigue', None))
        self.money = int(request.cookies.get('money', None))
        self.neet_fulness = int(request.cookies.get('neet_fulness', None))
        self.neet_motivation = int(request.cookies.get('neet_motivation', None))
        if request.cookies.get('time', None) == 'True':
            self.time = True
        else:
            self.time = False
        self.count = int(request.cookies.get('count', None))

        # ","で区切って配列に格納
        self.foods.clear()
        self.buys.clear()
        self.talks.clear()
        foods = request.cookies.get('foods', None)[:-1]
        buys = request.cookies.get('buys', None)[:-1]
        talks = request.cookies.get('talks', None)[:-1]
        num = 0
        for i in foods.split(','):
            if num%2 == 0:
                name = i
                num += 1
            else:
                price = int(i)
                self.foods.append({'name': name, 'price': price})
                num += 1
        num = 0
        for i in buys.split(','):
            if num % 2 == 0:
                name = i
                num += 1
            else:
                price = int(i)
                self.buys.append({'name': name, 'price': price})
                num += 1
        for i in talks.split(','):
            self.talks.append(i)

        self.foods_id.clear()
        self.buys_id.clear()
        self.talks_id.clear()
        foods_id = request.cookies.get('foods_id', None)[1:-1]
        buys_id = request.cookies.get('buys_id', None)[1:-1]
        talks_id = request.cookies.get('talks_id', None)[1:-1]
        for i in foods_id.split(','):
            self.foods_id.append(int(i))
        for i in buys_id.split(','):
            self.buys_id.append(int(i))
        for i in talks_id.split(','):
            self.talks_id.append(int(i))

        if request.cookies.get('clean', None) == 'True':
            self.clean = True
        else:
            self.clean = False
        return True