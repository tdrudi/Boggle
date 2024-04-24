from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "key"

boggle_game = Boggle()


"""Show board"""
@app.route("/")
def home():
    """from boggle class - make board function"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    numPlays = session.get("numPlays", 0)

    """Take values and send to index.html"""
    return render_template("/home/teagan/FlaskBoggle/index.html", board=board, highscore=highscore, numPlays=numPlays)


"""Check if word is in dict"""
@app.route("/check-word")
def check_word():
    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)
    return jsonify({"result" : res})


"""Get score, update plays and highscore"""
@app.route("/post-score", methods = ["POST"])
def post_score():
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numPlays = session.get("numPlays", 0)

    session["numPlays"] = numPlays + 1
    session["highscore"] = max(score, highscore)

    return jsonify(breakRecord = score > highscore)