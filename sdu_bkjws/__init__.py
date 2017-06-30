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
        self.session = self.login()

    # return a requests session, which include cookies. you can use it to get
    # html directly
    def login(self):
        if not hasattr(self, 'session'):
            self.last_connect = time.time()
            s = requests.session()
            s.get('http://bkjws.sdu.edu.cn')
            data = {
                'j_username': self.student_id,
                'j_password': self.password
            }
            r6 = s.post('http://bkjws.sdu.edu.cn/b/ajaxLogin', data=data)
            if r6.text == '"success"':
                return s
            else:
                raise Exception('username or password error')

    # not sure if it's appropriate to use
    @property
    def lessons(self):
        if hasattr(self, '_lessons'):
            return self._lessons
        else:
            self.get_lesson()
            return self._lessons

    def get_lesson(self):
        html = self.session.get('http://bkjws.sdu.edu.cn/f/xk/xs/bxqkb').text
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

    @property
    def detail(self):
        if hasattr(self, '_detail'):
            return self._detail
        else:
            self.get_detail()
            return self._detail
            # raise Exception('run get_detail() to init first')

    @_keep_live
    def get_detail(self):
        """
        :type: dict
        :return:
        """
        r = self.session.post("http://bkjws.sdu.edu.cn/b/grxx/xs/xjxx/detail",
                              headers={"X-Requested-With": "XMLHttpRequest"})
        r = r.json()
        if r['result'] == 'success':
            self._detail = r['object']
            return self._detail
        else:
            raise Exception(r, 'unexpected error please create a issue on GitHub')

    @_keep_live
    def get_raw_past_score(self):
        """
        :type: dict
        :return:
        """
        echo = random.randint(1, 9)
        data = {"aoData": [{"name": "sEcho", "value": echo}, {"name": "iColumns", "value": 10},
                           {"name": "sColumns", "value": ""}, {"name": "iDisplayStart", "value": 0},
                           {"name": "mDataProp_0", "value": "xnxq"}, {"name": "mDataProp_1", "value": "kch"},
                           {"name": "mDataProp_2", "value": "kcm"}, {"name": "mDataProp_3", "value": "kxh"},
                           {"name": "mDataProp_4", "value": "xf"}, {"name": "mDataProp_5", "value": "kssj"},
                           {"name": "mDataProp_6", "value": "kscjView"},
                           {"name": "mDataProp_7", "value": "wfzjd"},
                           {"name": "mDataProp_8", "value": "wfzdj"}, {"name": "mDataProp_9", "value": "kcsx"},
                           {"name": "iSortCol_0", "value": 5}, {"name": "sSortDir_0", "value": "desc"},
                           {"name": "iSortingCols", "value": 1}, {"name": "bSortable_0", "value": False},
                           {"name": "bSortable_1", "value": False}, {"name": "bSortable_2", "value": False},
                           {"name": "bSortable_3", "value": False}, {"name": "bSortable_4", "value": False},
                           {"name": "bSortable_5", "value": True}, {"name": "bSortable_6", "value": False},
                           {"name": "bSortable_7", "value": False}, {"name": "bSortable_8", "value": False},
                           {"name": "bSortable_9", "value": False}]}

        string = urlencode(data)
        response = self.session.post("http://bkjws.sdu.edu.cn/b/cj/cjcx/xs/lscx",
                                     headers={"X-Requested-With": "XMLHttpRequest",
                                              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                                     data=string)
        response = response.json()
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

    @_keep_live
    def get_raw_now_score(self):
        """
        :type: dict
        :return:
        """
        echo = random.randint(1, 9)
        data = {"aoData": [{"name": "sEcho", "value": echo}, {"name": "iColumns", "value": 10},
                           {"name": "sColumns", "value": ""}, {"name": "iDisplayStart", "value": 0},
                           {"name": "mDataProp_0", "value": "xnxq"}, {"name": "mDataProp_1", "value": "kch"},
                           {"name": "mDataProp_2", "value": "kcm"}, {"name": "mDataProp_3", "value": "kxh"},
                           {"name": "mDataProp_4", "value": "xf"}, {"name": "mDataProp_5", "value": "kssj"},
                           {"name": "mDataProp_6", "value": "kscjView"},
                           {"name": "mDataProp_7", "value": "wfzjd"},
                           {"name": "mDataProp_8", "value": "wfzdj"}, {"name": "mDataProp_9", "value": "kcsx"},
                           {"name": "iSortCol_0", "value": 5}, {"name": "sSortDir_0", "value": "desc"},
                           {"name": "iSortingCols", "value": 1}, {"name": "bSortable_0", "value": False},
                           {"name": "bSortable_1", "value": False}, {"name": "bSortable_2", "value": False},
                           {"name": "bSortable_3", "value": False}, {"name": "bSortable_4", "value": False},
                           {"name": "bSortable_5", "value": True}, {"name": "bSortable_6", "value": False},
                           {"name": "bSortable_7", "value": False}, {"name": "bSortable_8", "value": False},
                           {"name": "bSortable_9", "value": False}]}
        string = urlencode(data)
        response = self.session.post("http://bkjws.sdu.edu.cn/b/cj/cjcx/xs/list",
                                     headers={"X-Requested-With": "XMLHttpRequest",
                                              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                                     data=string)
        response = response.json()
        if self._check_response(response, echo):
            self._raw_now_score = response
            return self._raw_now_score
        else:
            raise Exception(
                response, 'unexpected error please create a issue on GitHub')

    @_keep_live
    def get_now_score(self):
        """
        :type: bool
        :return:
        """
        response = self.get_raw_now_score()
        score_list = response['object']['aaData']
        return score_list

    def _check_response(self, response, echo):
        if response['result'] == 'success' and response['object']['sEcho'] == str(echo):
            return True
        else:
            return False

    @_keep_live
    def update_contact_info(self, english_name='', phone_number='', postcode='', address=''):
        if hasattr(self, '_detail'):
            self.get_detail()
        detail = self.detail
        english_name = english_name if english_name else detail['ywxm']
        phone_number = phone_number if phone_number else detail['lxdh']
        address = address if address else detail['txdz']
        postcode = postcode if postcode else detail['yb']
        info = {'ywxm': english_name,
                'lxdh': phone_number,
                'txdz': address,
                'yb': postcode}
        for key, value in info.items():
            if value == None:
                info[key] = ''
        r = self.session.post('http://bkjws.sdu.edu.cn/b/grxx/xs/xjxx/save',
                              headers={'X-Requested-With': 'XMLHttpRequest'},
                              data=info)
        r = r.json()
        if r['result'] == 'success' and r['msg'] == "保存成功":
            return True
        else:
            raise Exception(r, 'unexpected error please create a issue on GitHub')

    @_keep_live
    def get_rank_with_query(self, lesson_num_long, lesson_num, exam_time):
        kch_kxh_kssj = '{}_{}_{}'.format(lesson_num_long, lesson_num, exam_time)
        query = {'aoData': '',
                 'dataTableId_length': -1,
                 'kch_kxh_kssj': kch_kxh_kssj}
        print(query)
        r = self.session.post('http://bkjws.sdu.edu.cn/f/cj/cjcx/xs/xspm',
                              headers={"X-Requested-With": "XMLHttpRequest",
                                       "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                              data=query)
        soup = BeautifulSoup(r.text, 'html.parser')
        s = soup.find('table', id='dataTableId')
        # print(s)

        l = s.find_all('tr')
        head = l[0]
        body = l[1:]
        head = list(map(lambda x: x.text, head.find_all('th')))
        # body = list(map(lambda x: x.find_all('td'), body))
        print(head)
        body = list(map(lambda x: x.find_all('td'), body))
        objList = []
        for line in body:
            line = list(map(lambda x: x.text, line))
            objList.append({
                "lesson_num_long": line[head.index('课程号')],
                "lesson_name": line[head.index('课程名')],
                "lesson_num": line[head.index('课序号')],
                "credit": line[head.index('学分')],
                "exam_time": line[head.index('考试时间')],
                "score": line[head.index('成绩')],
                "number": line[head.index('选课人数')],
                "rank": line[head.index('排名')],
                "max_score": line[head.index('最高分')],
                "min_score": line[head.index('最低分')]
            })
        return objList
