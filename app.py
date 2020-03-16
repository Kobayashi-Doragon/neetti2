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
    # 入力データを取得
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
                               buys=player.buys, talks=player.talks)
    else:
        return render_template("login.html", message="ユーザIDもしくはパスワードが間違っています")


# アカウント作成
@app.route("/create", methods=["POST"])
def create_account():
    # 入力データを取得
    id = request.form["id"]
    password = request.form["password"]
    # 入力が不十分な時
    if id == "" or password == "":
        return render_template("login.html", message="ユーザIDとパスワードを入力してください")
    if not id.isdecimal():
        return render_template("login.html", message="ユーザーIDには半角数字のみを入力してください")
    if int(id) >= 100000:
        return render_template("login.html", message="idには5桁までの半角数字を入力してください")
    if player.create(id, password):
        player.update_data()
        return render_template("game.html", message="", neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks)
    else:
        return render_template("login.html", message="ユーザIDが既に使用されています")


# セーブボタンを押したとき
@app.route("/save")
def save():
    player.save()
    return render_template("game.html", message="セーブしました", neet_answer="",
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


# ログアウトボタンを押したとき
@app.route("/logout")
def logout():
    player.save()
    return render_template("login.html", message="")


# 話しかけたとき
@app.route("/talk")
def talk():
    # talk_idを取得しtalkメソッド呼び出し
    talk_id = request.args.get("talk_id")
    word=player.talks[int(talk_id)]
    response = player.talk(talk_id)
    return render_template("game.html", message=word, neet_answer=response,
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks)


# ご飯を与えたとき
@app.route("/feed")
def feed():
    # food_idを取得しfeedメソッド呼び出し
    food_id = request.args.get("food_id")
    player.feed(food_id)
    result = "食事を与えた"
    return render_template("game.html", message=result, neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks)


# 物を買い与えたとき
@app.route("/buy")
def buy():
    # buy_idを取得しbuyメソッド呼び出し
    buy_id = request.args.get("buy_id")
    player.buy(buy_id)
    result="物を買ってあげた"
    # クリアしたとき別画面へ
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


# 働く/寝るボタンを押したとき
@app.route("/work_sleep")
def work():
    # 疲労度，時間によって呼び出すメソッドを変更する
    if player.mother_fatigue < -500:
        player.sleep()
        result = "疲れて仕事に行けないので寝た"
    elif player.time:
        result = player.work()
    else:
        result = player.sleep()
    player.update_data()
    if player.check_neet():
        return render_template("end.html", money=player.money, time=player.time,
                               count=player.count)
    return render_template("game.html", message=result, neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks)


if __name__ == '__main__':
    app.run()
