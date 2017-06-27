import json
from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urlencode
import random


def _keep_live(fn):
    def wrapper(self, *args, **kwargs):
        if time.time() - self.last_connect > 15 * 60:
            self.session = self.login()
            self.last_connect = time.time()
        return fn(self, *args, **kwargs)

    return wrapper


class SduBkjws(object):
    def __init__(self, student_id, password):
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

    # use session to get lesson html
    @_keep_live
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

    @_keep_live
    def get_raw_past_score(self):
        """
        :type: dict
        :return:
        """
        echo = random.randint(1, 9)
        data = {"aoData": [{"name": "sEcho", "value": echo}, {"name": "iColumns", "value": 10},
                           {"name": "sColumns", "value": ""}, {
                               "name": "iDisplayStart", "value": 0},
                           # {"name": "iDisplayLength", "value": 70},
                           {"name": "mDataProp_0", "value": "xnxq"},
                           {"name": "mDataProp_1", "value": "kch"}, {
                               "name": "mDataProp_2", "value": "kcm"},
                           {"name": "mDataProp_3", "value": "kxh"}, {
                               "name": "mDataProp_4", "value": "xf"},
                           {"name": "mDataProp_5", "value": "kssj"}, {
                               "name": "mDataProp_6", "value": "kscjView"},
                           {"name": "mDataProp_7", "value": "wfzjd"}, {
                               "name": "mDataProp_8", "value": "wfzdj"},
                           {"name": "mDataProp_9", "value": "kcsx"}, {
                               "name": "iSortCol_0", "value": 5},
                           {"name": "sSortDir_0", "value": "desc"}, {
                               "name": "iSortingCols", "value": 1},
                           {"name": "bSortable_0", "value": False}, {
                               "name": "bSortable_1", "value": False},
                           {"name": "bSortable_2", "value": False}, {
                               "name": "bSortable_3", "value": False},
                           {"name": "bSortable_4", "value": False}, {
                               "name": "bSortable_5", "value": True},
                           {"name": "bSortable_6", "value": False}, {
                               "name": "bSortable_7", "value": False},
                           {"name": "bSortable_8", "value": False}, {"name": "bSortable_9", "value": False}]}

        string = urlencode(data)
        response = self.session.post("http://bkjws.sdu.edu.cn/b/cj/cjcx/xs/lscx",
                                     headers={"X-Requested-With": "XMLHttpRequest",
                                              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                                     data=string)
        response = json.loads(response.text)
        if response['result'] == 'success' and response['object']['sEcho'] == str(echo):
            self._raw_past_score = response
            return self._raw_past_score
        else:
            raise Exception(
                response, 'unexpected error please create a issue on GitHub')

    @_keep_live
    def get_past_score(self):
        """
        :type: list
        :return:
        """

        response = self.get_raw_past_score()
        score_list = response['object']['aaData']
        return score_list
