from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    #TODO -- write tests for every view function / feature!
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_home(self):
        with self.client:
            res = self.client.get("/")
            self.assertIn("board", session)
            self.assertIn(b"High Score: ", res.data)
            self.assertIn(b"Score: ", res.data)
            self.assertIn(b"Time Left: ", res.data)
            self.assertIsNone(session.get("highscore"))
            self.assertIsNone(session.get("numPlays"))

    def test_valid(self):
        with self.client as client:
            with client.session_transaction() as session:
                session["board"] =[["W", "O", "R", "K"],["W", "O", "R", "K"],
                                   ["W", "O", "R", "K"],["W", "O", "R", "K"],
                                   ["W", "O", "R", "K"]]
        res = self.client.get("/check-word?word=work")
        self.assertEqual(res.json["result"], "ok")

    def test_invalid(self):
        self.client.get("/")
        res = self.client.get("check-word?word=")
        self.assertEqual(res.json["result"], "not-on-board")

    def not_english(self):
        self.client.get("/")
        res = self.client.get("/check-word?word=asdjk")
        self.assertEqual(res.json["result"], "not-word")

