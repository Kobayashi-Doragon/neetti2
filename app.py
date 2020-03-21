# ルートによってメソッドを呼び出す

from flask import Flask, render_template, request, make_response
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
    player.update_data()
    res = make_response(render_template("game.html", message="", neet_answer="",
                                        money=player.money, time=player.time,
                                        count=player.count, foods=player.foods,
                                        buys=player.buys, talks=player.talks))

    # 入力データを取得
    id = request.form["id"]
    password = request.form["password"]
    # DBと同じならゲーム画面へ、違うならもう一度入力してもらう


    if id == "" or password == "":
        return render_template("login.html", message="ユーザIDとパスワードを入力してください")
    if not id.isdecimal():
        return render_template("login.html", message="ユーザーIDには半角数字を入力してください")
    if player.login(id, password):
        return player.set_cookies(res)
    else:
        return render_template("login.html", message="ユーザIDもしくはパスワードが間違っています")


# アカウント作成
@app.route("/create", methods=["POST"])
def create_account():
    player.update_data()
    res = make_response(render_template("game.html", message="", neet_answer="",
                                             money=player.money, time=player.time,
                                             count=player.count, foods=player.foods,
                                             buys=player.buys, talks=player.talks))

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
        #player.update_data()
        return player.set_cookies(res)
    else:
        return render_template("login.html", message="ユーザIDが既に使用されています")


# セーブボタンを押したとき
@app.route("/save")
def save():
    # cookieからデータ取得
    player.get_cookies()

    player.save()
    res = make_response(render_template("game.html", message="セーブしました", neet_answer="",
                           money=player.money, time=player.time,
                           count=player.count, foods=player.foods,
                           buys=player.buys, talks=player.talks))
    return player.set_cookies(res)


# ログアウトボタンを押したとき
@app.route("/logout")
def logout():
    # cookieからデータ取得
    player.get_cookies()

    player.save()
    return render_template("login.html", message="")


# 話しかけたとき
@app.route("/talk")
def talk():
    # cookieからデータ取得
    player.get_cookies()
    # talk_idを取得しtalkメソッド呼び出し
    talk_id = request.args.get("talk_id")
    word=player.talks[int(talk_id)]
    response = player.talk(talk_id)

    res = make_response(render_template("game.html", message=word, neet_answer=response,
                                        money=player.money, time=player.time,
                                        count=player.count, foods=player.foods,
                                        buys=player.buys, talks=player.talks))

    return player.set_cookies(res)


# ご飯を与えたとき
@app.route("/feed")
def feed():
    # cookieからデータ取得
    player.get_cookies()
    # food_idを取得しfeedメソッド呼び出し
    food_id = request.args.get("food_id")
    result = player.feed(food_id)
    #result = "食事を与えた"
    res = make_response(render_template("game.html", message=result, neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks))
    return player.set_cookies(res)


# 物を買い与えたとき
@app.route("/buy")
def buy():
    # cookieからデータ取得
    player.get_cookies()
    # buy_idを取得しbuyメソッド呼び出し
    buy_id = request.args.get("buy_id")
    result = player.buy(buy_id)
    #result="物を買ってあげた"
    # クリアしたとき別画面へ
    res = make_response(render_template("game.html", message=result, neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks))
    return player.set_cookies(res)


@app.route("/clean")
def clean():
    # cookieからデータ取得
    player.get_cookies()
    if player.clean:
        res = make_response(render_template("game.html", message="(部屋はきれいだから,掃除はいらないかな)", neet_answer="",
                                            money=player.money, time=player.time,
                                            count=player.count, foods=player.foods,
                                            buys=player.buys, talks=player.talks))
        return player.set_cookies(res)
    else:
        player.mother_fatigue -= 30
        player.neet_motivation += 50
        player.clean = True;
        res = make_response(render_template("game.html", message="(掃除しました)", neet_answer="",
                                            money=player.money, time=player.time,
                                            count=player.count, foods=player.foods,
                                            buys=player.buys, talks=player.talks))
        return player.set_cookies(res)


# 働く/寝るボタンを押したとき
@app.route("/work_sleep")
def work():
    # cookieからデータ取得
    player.get_cookies()
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
        res = make_response(render_template("end.html", money=player.money, time=player.time,
                               count=player.count))
        return player.set_cookies(res)
    res = make_response(render_template("game.html", message=result, neet_answer="",
                               money=player.money, time=player.time,
                               count=player.count, foods=player.foods,
                               buys=player.buys, talks=player.talks))
    return player.set_cookies(res)


if __name__ == '__main__':
    app.run()
