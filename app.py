# ルートによってメソッドを呼び出す

from flask import Flask, render_template, request
import methods

app = Flask(__name__)
player = methods.player()


# 初めのログイン画面表示
@app.route("/")
def login_screen():
    return render_template("login.html", message="")


# ログインボタンでログインしゲーム画面へ
@app.route("/login", methods=["POST"])
def login():
    # 入力データを引数にloginメソッド呼ぶ
    id = request.form["id"]
    password = request.form["password"]
    # DBと同じならゲーム画面へ、違うならもう一度入力してもらう
    if id == "" or password == "":
        return render_template("login.html", message="ユーザIDとパスワードを入力してください")
    if not id.isdecimal():
        return render_template("login.html", message="ユーザーIDには半角数字を入力してください")
    if player.login(id, password):
        player.update_data()
        return render_template("game.html", message="", neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks)  # foodsとbuysを追加(これ以降全て)
    else:
        return render_template("login.html", message="ユーザIDもしくはパスワードが間違っています")

# 入力を元にアカウント追加
@app.route("/create", methods=["POST"])
def create_account():
    id = request.form["id"]
    password = request.form["password"]

    if id == "" or password == "":
        return render_template("login.html", message="ユーザIDとパスワードを入力してください")
    if not id.isdecimal():
        return render_template("login.html", message="ユーザーIDには半角数字のみを入力してください")
    if player.create(id, password):
        player.update_data()
        return render_template("game.html", message="", neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks)
    else:
        return render_template("login.html", message="ユーザIDが既に使用されています")


# セーブボタン用
@app.route("/save")
def save():
    player.save()
    return render_template("game.html", message="セーブしました", neet_answer="",
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


# セーブしてログイン画面に戻る
@app.route("/logout")
def logout():
    player.save()
    return render_template("login.html", message="")


# ご飯と同じく選択肢で
@app.route("/talk")
def talk():
    # トーク
    talk_id = request.args.get("talk_id")
    answer = player.talk(talk_id)
    '''
    if player.check_neet():
        # 　クリアしたとき　要変更
        return render_template("game.html", message="ニートが出てきた", neet_answer=answer,
                               money=player.money, time=player.time, foods=player.foods, buys=player.buys)
    '''
    return render_template("game.html", message=player.talks[int(talk_id)], neet_answer=answer,
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


@app.route("/feed")
def feed():
    # feed
    food_id = request.args.get("food_id")
    # result = player.feed(food_id)　 #バグが出たので除去
    result = player.feed(food_id)
    # result = "食事を与えた"
    '''if player.check_neet():
        # 　クリアしたとき　要変更
        return render_template("game.html", message="息子が出てきた", neet_answer="", money=player.money,
                               fatigue=player.mother_fatigue, time=player.time, foods=player.foods, buys=player.buys)
    else:
    '''
    return render_template("game.html", message=result, neet_answer="",
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


@app.route("/buy")
def buy():
    # buy
    buy_id = request.args.get("buy_id")
    result = player.buy(buy_id)  # バグが出たので除去
    # player.buy(buy_id)
    # result="物を買ってあげた"
    '''if player.check_neet():
        # 　クリアしたとき　要変更
        return render_template("game.html", message="息子が出てきた", neet_answer="", money=player.money,
                               fatigue=player.mother_fatigue, time=player.time, foods=player.foods, buys=player.buys)
    '''
    return render_template("game.html", message=result, neet_answer="",
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


@app.route("/work_sleep")
def work():
    if player.time:
        result = player.work()
    else:
        result = player.sleep()
    player.update_data()
    if player.check_neet():
        return render_template("game.html", message="ニートが出てきた", neet_answer="", money=player.money,
                               fatigue=player.mother_fatigue, time=player.time, count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks)
        # return render_remplete("end.html")
    return render_template("game.html", message=result, neet_answer="",
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


@app.route("/clean")
def clean():
    if player.clean:
        return render_template("game.html", message="(部屋はきれいだから,掃除はいらないかな)", neet_answer="", money=player.money,
                               fatigue=player.mother_fatigue, time=player.time, count=player.count, foods=player.foods, buys=player.buys, talks=player.talks)
    else:
        player.mother_fatigue -= 30
        player.neet_motivation += 50
        player.clean = True;
        return render_template("game.html", message="(掃除しました)", neet_answer="", money=player.money,
                               fatigue=player.mother_fatigue, time=player.time, count=player.count, foods=player.foods, buys=player.buys, talks=player.talks)


if __name__ == '__main__':
    app.run()
