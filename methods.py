# 各メソッドを用意する用
import sql
import random


class player():
    # コンストラクタ
    def __init__(self):
        self.player_id = 0
        self.mother_fatigue = 0
        self.money = 1000
        self.neet_fulness = 0
        self.neet_motivation = 0
        self.time = True
        self.foods = []
        self.buys = []
        self.talks = []
        self.data_id = []
        self.count = 1
        sql.connect(self)


    # データベースの値を表示するためにDBから取得
    def update_data(self):
        # 日にちによってシード値固定
        random.seed(self.count)
        # data_idを重複なしで5つ選ぶ
        self.data_id = random.sample(range(1,31),5)
        # 不要な配列データを削除
        self.foods.clear()
        self.buys.clear()
        self.talks.clear()

        # データの読み込み
        for item in self.data_id:
            check = "select food_name from food1 where food_id = '" + str(item) + "'"
            check2 = "select food_price from food1 where food_id = '" + str(item) + "'"
            name = sql.query(self, check)
            price = sql.query(self, check2)
            # foods配列にデータを追加
            self.foods.append({'name': name, 'price': price})

            check = "select buy_name from buy where buy_id = '" + str(item) + "'"
            check2 = "select buy_price from buy where buy_id = '" + str(item) + "'"
            name = sql.query(self, check)
            price = sql.query(self, check2)
            # buys配列にデータ追加
            self.buys.append({'name': name, 'price': price})

            check = "select talk_sentence from talk where talk_id = '" + str(item) +"'"
            name = sql.query(self, check)
            # talks配列にデータ追加
            self.talks.append(name)


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
        # DBと入力を照合(true or false)
        text = "select exists(select * from users where player_id = " + id + ");"
        result = sql.query(self, text)

        # ユーザIDが重複するとき
        if result[0]:
            return False
        # ユーザIDが重複しないときアカウント作成
        else:
            text = "insert into users values(" + id + ",'" + password + "',0,2000,True,0,0,1);"
            sql.add(self, text)
            self.player_id = id
            return True


    # ステータスをDBに格納
    def save(self):
        if self.time:
            time_bool="True"
        else:
            time_bool="False"

        # selfのステータスをDBに格納
        text = "update users set mother_fatigue=" + str(self.mother_fatigue) + ",money=" +\
               str(self.money) + ",time='"+ time_bool +"',neet_fulness=" + str(self.neet_fulness) +\
               ",neet_motivation=" + str(self.neet_motivation) + ",count=" + str(self.count) +\
               " where player_id=" + str(self.player_id) + ";"
        sql.add(self, text)
        return True


    # 話しかけたとき
    def talk(self, talk_id):
        # DBのtalkテーブルからニートの返事を選択
        text = "select * from talk where talk_id = '" + str(self.data_id[int(talk_id)]) + "'"
        result = sql.query(self, text)
        rand_int=random.randint(0, 1)
        # ステータスを更新
        self.neet_motivation += result[3][rand_int]
        # ステータスによって返事を変える
        if self.neet_fulness <= -100:
            return result[1],"お腹がすいた"
        else:
            return result[1],result[2][rand_int]


    # 食事を与えたとき
    def feed(self, food_id):
        # お金が足りるか確認用
        check = "select food_price from food1 where food_id = '" + str(self.data_id[int(food_id)]) + "'"
        price = sql.query(self, check)[0]

        # お金が足りないときエラーメッセージ
        if self.money - price < 0:
            return "お金が足りません"
        # お金が足りるとき購入，ステータス更新
        else:
            text = "select * from food1 where food_id = '" + str(self.data_id[int(food_id)]) + "'"
            result = sql.query(self, text)
            self.money -= price
            self.neet_fulness += 100
            self.neet_motivation += result[3]


    # 物を買ってあげたとき
    def buy(self, buy_id):
        # お金が足りるか確認用
        check = "select buy_price from buy where buy_id = '" + str(self.data_id[int(buy_id)]) + "'"
        price = sql.query(self, check)[0]

        # お金が足りないときエラーメッセージ
        if self.money - price < 0:
            return "お金が足りません"
        # お金が足りるとき購入，ステータス更新
        else:
            text = "select * from buy where buy_id = '" + str(self.data_id[int(buy_id)]) + "'"
            result = sql.query(self, text)
            self.money -= price
            self.neet_motivation += result[3]


    # 掃除したとき
    def clean(self):
        # 疲れているとき掃除できない
        if self.mother_fatigue <= 0:
            return "疲れていて掃除できない"
        # ステータス更新
        else:
            self.mother_fatigue -= 40
            self.neet_motivation += 50
            return "部屋を掃除した"


    # 仕事に行ったとき
    def work(self):
        # ステータスを更新
        self.time = False
        self.mother_fatigue -= 100
        self.money += 3000
        self.neet_fulness -= 50
        return "仕事に行った"


    # 寝たとき
    def sleep(self):
        # ステータスを更新
        self.time = True
        self.mother_fatigue += 200
        self.neet_fulness -= 50
        self.count += 1
        return "寝た"


    # ニートの機嫌を確認
    def check_neet(self):
        if self.neet_motivation >= 1000:
            return True
        else:
            return False
