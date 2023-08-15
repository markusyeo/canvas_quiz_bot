from api.utility import *

class Quizzes(Rooted):

    URL = 'quizzes'

    @property
    def info(self):
        def make_data(p):
            return {
                'per_page': 100,
                'page': p
            }
        page = 1
        result = []
        while True:
            response = self.HTTP.get(self.URL, data=make_data(page))
            json_response = response.json()
            if not json_response: break
            if 'status' in json_response:
                return None
            result.extend(json_response)
            page += 1
        headers = ['id', 'title', 'html_url', 'mobile_url', 'description', 'quiz_type', 'time_limit', 'timer_autosubmit_disabled', 'due_at', 'unlock_at', 'lock_at', 'cant_go_back', 'question_count', 'points_possible']
        data = []
        for quiz in result:
            id = quiz['id']
            title = quiz['title']
            html_url = quiz['html_url']
            mobile_url = quiz['mobile_url']
            description = quiz['description']
            quiz_type = quiz['quiz_type']
            time_limit = quiz['time_limit']
            timer_autosubmit_disabled = quiz['timer_autosubmit_disabled']
            due_at = quiz['due_at']
            unlock_at = quiz['unlock_at']
            lock_at = quiz['lock_at']
            cant_go_back = quiz['cant_go_back']
            question_count = quiz['question_count']
            points_possible = quiz['points_possible']
            data.append([id, title, html_url, mobile_url, description, quiz_type, time_limit, timer_autosubmit_disabled, due_at, unlock_at, lock_at, cant_go_back, question_count, points_possible])
        return Table(headers=headers, data=data)
    
    @guess_id
    def __call__(self, id):
        return Quizzes(self, id)