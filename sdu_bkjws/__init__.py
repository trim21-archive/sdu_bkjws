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
        self.post_headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                             'X-Requested-With': 'XMLHttpRequest'}

    @property
    def echo(self):
        return random.randint(1, 9)

    @staticmethod
    def aodata(echo, columns, xnxq=None, final_exam=False):

        ao_data = [{"name": "sEcho", "value": echo},
                   {"name": "iColumns", "value": len(columns)},
                   {"name": "sColumns", "value": ""},
                   {"name": "iDisplayStart", "value": 0},
                   {"name": "iDisplayLength", "value": -1},
                   ]
        if xnxq:
            if final_exam:
                ao_data.append({"name": "ksrwid", "value": "000000005bf6cb6f015bfac609410d4b"})
            ao_data.append({"name": "xnxq", "value": "2016-2017-2"})

            # pass

        for index, value in enumerate(columns):
            ao_data.append({"name": "mDataProp_{}".format(index), "value": value})
            ao_data.append({"name": "bSortable_{}".format(index), "value": False})

        return urlencode({"aoData": ao_data})

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
                s.close()
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

    @_keep_live
    def get_fail_score(self):
        echo = self.echo
        r = self.post('http://bkjws.sdu.edu.cn/b/cj/cjcx/xs/bjgcx',

                      data=self.aodata(echo, ["xnxq", "kch", "kcm", "kxh", "xf", "kssj", "kscjView"]))
        # print(r)
        if self._check_response(r, echo):
            return r['object']['aaData']
        else:
            raise Exception(r, 'unexpected error please create a issue on GitHub')

    @property
    def detail(self):
        if hasattr(self, '_detail'):
            return self._detail
        else:
            self.get_detail()
            return self._detail

    @_keep_live
    def get_detail(self):
        """
        :type: dict
        :return:
        """
        r = self.post("http://bkjws.sdu.edu.cn/b/grxx/xs/xjxx/detail",
                      data=None)
        # r = r.json()
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

        response = self.post("http://bkjws.sdu.edu.cn/b/cj/cjcx/xs/lscx",

                             data=self.aodata(echo,
                                              columns=["xnxq", "kcm", "kxh", "xf", "kssj", "kscjView", "wfzjd", "wfzdj",
                                                       "kcsx"]))
        if self._check_response(response, echo):
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

        response = self.post("http://bkjws.sdu.edu.cn/b/cj/cjcx/xs/list",

                             data=self.aodata(echo,
                                              columns=["xnxq", "kcm", "kxh", "xf", "kssj", "kscjView", "wfzjd", "wfzdj",
                                                       "kcsx"]))
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

    @staticmethod
    def _check_response(response, echo):
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
            if not value:
                info[key] = ''
        r = self.post('http://bkjws.sdu.edu.cn/b/grxx/xs/xjxx/save',

                      data=info)
        if r['result'] == 'success' and r['msg'] == "保存成功":
            return True
        else:
            raise Exception(r, 'unexpected error please create a issue on GitHub')

    @_keep_live
    def get_multi_rank_with_query(self, search_list):
        query = "aoData=&dataTableId_length=-1"
        for obj in search_list:
            lesson_num_long, lesson_num, exam_time = obj['lesson_num_long'], obj['lesson_num_short'], obj['exam_time']
            query += '&kch_kxh_kssj={}_{}_{}'.format(lesson_num_long, lesson_num, exam_time)
        return self._get_rank_with_query(query)

    @_keep_live
    def post(self, url, data, headers=None):
        if headers:
            r = self.session.post(url, headers=headers,
                                  data=data)
        else:
            r = self.session.post(url,
                                  headers=self.post_headers,
                                  data=data)
        if r.headers['content-type'].find('json') != -1:
            return r.json()
        if r.headers['content-type'].find('html') != -1:
            return r.text

    @_keep_live
    def get_rank_with_query(self, lesson_num_long, lesson_num_short, exam_time):
        query = "aoData=&dataTableId_length=-1"
        query += '&kch_kxh_kssj={}_{}_{}'.format(lesson_num_long, lesson_num_short, exam_time)
        return self._get_rank_with_query(query)[0]

    def _get_rank_with_query(self, query):
        r = self.post('http://bkjws.sdu.edu.cn/f/cj/cjcx/xs/xspm',
                      data=query)
        soup = BeautifulSoup(r, 'html.parser')
        s = soup.find('table', id='dataTableId')
        l = s.find_all('tr')
        head = l[0]
        body = l[1:]
        head = list(map(lambda x: x.text, head.find_all('th')))
        body = list(map(lambda x: x.find_all('td'), body))
        obj_list = []
        for line in body:
            line = list(map(lambda x: x.text, line))
            obj_list.append({
                "lesson_num_long": line[head.index('课程号')],
                "lesson_name": line[head.index('课程名')],
                "lesson_num_short": line[head.index('课序号')],
                "credit": line[head.index('学分')],
                "exam_time": line[head.index('考试时间')],
                "score": line[head.index('成绩')],
                "number": line[head.index('选课人数')],
                "rank": line[head.index('排名')],
                "max_score": line[head.index('最高分')],
                "min_score": line[head.index('最低分')]
            })
        return obj_list

    def comment_lesson(self):
        # todo: this function
        pass

    @_keep_live
    def get_comment_lesson_info(self):  # 获取课程序列

        echo = random.randint(0, 9)
        response = self.post('http://bkjws.sdu.edu.cn/b/pg/xs/list',

                             data=self.aodata(echo, ['kch', 'kcm', 'jsm', 'function', 'function']), )
        if self._check_response(response, echo=echo):
            return response['object']['aaData']
        else:
            raise Exception(response, 'unexpected error please create a issue on GitHub')

    @_keep_live
    def get_exam_time(self, xnxq):
        echo = self.echo
        r = self.post('http://bkjws.sdu.edu.cn/b/ksap/xs/vksapxs/pageList',
                      data=self.aodata(echo,
                                       columns=["function", 'ksmc', 'kcm', 'kch', 'xqmc', 'jxljs', 'sjsj', "ksfsmc",
                                                "ksffmc", "ksbz"]))
        if self._check_response(r, echo):
            self._raw_past_score = r
            return self._raw_past_score
        else:
            raise Exception(
                r, 'unexpected error please create a issue on GitHub')
