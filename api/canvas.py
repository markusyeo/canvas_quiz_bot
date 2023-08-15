import os
import pickle

from getpass import getpass

CANVAS_LOGIN_FILENAME = 'credentials/canvas.pkl'

from env import CANVAS_TOKEN
from api.utility import *
from api.quizzes import Quizzes

class CanvasAPI:

    URL_BASE    = f'https://canvas.nus.edu.sg'

    def __init__(self, course_id):
        self.URL = self.URL_BASE + f'/api/v1/courses/{course_id}'

        self.course_id = course_id
        self.root = self

        self.HTTP           = CanvasHTTP(self)
        self.Quizzes    = Quizzes(self)
    
    def login(self, tag=None):
        if not os.path.exists(CANVAS_LOGIN_FILENAME) or tag == 'retry_sign_in':
            print("=== Canvas token required ===")
            token = CANVAS_TOKEN
            with open(CANVAS_LOGIN_FILENAME, 'wb+') as f:
                pickle.dump(token, f)
        with open(CANVAS_LOGIN_FILENAME, 'rb') as login_details:
            token = pickle.load(login_details)
        self.HTTP.session.headers.update({'Authorization': f"Bearer {token}"})
        try:
            self.ping()
            print("Success, you logged in to Canvas successfully.")
        except:
            self.login(tag='retry_sign_in')

    def ping(self):
        response = self.HTTP.get(self.URL)
        assert response.ok
        return response.json()
