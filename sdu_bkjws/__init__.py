from bs4 import BeautifulSoup
import requests
import time


class SduBkjws(object):
    def __init__(self, student_id: str, password: str):
        self.student_id = student_id
        self.password = password
        self.login()

    # return a requests session, which include cookies. you can use it to get
    # html directly
    def login(self):
        self.last_connect = time.time()
        s = requests.session()
        s.get('http://bkjws.sdu.edu.cn')
        data = {
            'j_username': self.student_id,
            'j_password': self.password
        }
        r6 = s.post('http://bkjws.sdu.edu.cn/b/ajaxLogin', data=data)
        if r6.text == '"success"':
            self.session = s
        else:
            raise Exception('username or password error')

    def keep_live(fn):
        def wrapper(self, *args, **kwargs):
            if time.time() - self.last_connect > 15 * 60:
                self.session = self.login()
                self.last_connect = time.time()
            return fn(self, *args, **kwargs)
        return wrapper

    # use session to get lesson html
    @keep_live
    def get_lesson_html(self):
        s = self.session
        if s:
            r3 = s.get('http://bkjws.sdu.edu.cn/f/xk/xs/bxqkb')
            return r3.text
        else:
            return False

    # not sure if it's appropriate to use
    @property
    def lessons(self):
        if hasattr(self, '_lessons'):
            return self._lessons
        else:
            raise Exception('run get_lesson() to init first')

    def get_lesson(self):
        html = self.get_lesson_html()
        # print(html)
        soup = BeautifulSoup(html, "html.parser")
        s = soup.find('table',
                      attrs={"class": "table table-striped table-bordered table-hover",
                             "id": "ysjddDataTableId"})
        tr_box = s.find_all('tr')
        c = list()

        for les in tr_box[1:]:
            td_box = les.find_all('td')
            c.append({"lesson_num_long": td_box[1].text,
                      "lesson_name": td_box[2].text,
                      "lesson_num_short": td_box[3].text,
                      "credit": td_box[4].text,
                      "school": td_box[6].text,
                      "teacher": td_box[7].text,
                      "weeks": td_box[8].text,
                      "days": td_box[9].text,
                      "times": td_box[10].text,
                      "place": td_box[11].text})
        self._lessons = c
        return c
