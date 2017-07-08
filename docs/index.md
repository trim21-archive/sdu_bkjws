---
layout: post
title: sdu-bkjws 介绍
---
<!--[![PyPI version](https://badge.fury.io/py/sdu-bkjws.svg)](https://badge.fury.io/py/sdu-bkjws)-->
version: 1.0.0

<!-- TOC -->
<!-- vscode-markdown-toc -->
* 1. [quick start](#quickstart)
* 2. [安装](#)
* 3. [sdu-bkjws](#sdu-bkjws)
	* 3.1. [类初始化](#-1)
	* 3.2. [SduBkjws.login()和Sdubkjws.session](#SduBkjws.loginSdubkjws.session)
	* 3.3. [    SduBkjws.update_contact_info()](#SduBkjws.update_contact_info)
	* 3.4. [SduBkjws.get_lessons()和SduBkjws.lessons](#SduBkjws.get_lessonsSduBkjws.lessons)
	* 3.5. [SduBkjws.get_detail()和SduBkjws.detail](#SduBkjws.get_detailSduBkjws.detail)
	* 3.6. [score](#score)
		* 3.6.1. [get_now_score()](#get_now_score)
		* 3.6.2. [get_past_score()](#get_past_score)
		* 3.6.3. [get_raw_now_score()](#get_raw_now_score)
		* 3.6.4. [get_rank_with_query](#get_rank_with_query)
		* 3.6.5. [get_multi_rank_with_query](#get_multi_rank_with_query)
	* 3.7. [exam](#exam)
		* 3.7.1. [get_exam_time()](#get_exam_time)
	* 3.8. [comment](#comment)
		* 3.8.1. [get_comment_lesson_info()](#get_comment_lesson_info)
		* 3.8.2. [comment_lesson](#comment_lesson)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->
<!-- /TOC -->


sdu-bkjws是为简化与山东大学教务系统交互而写的库

[山东大教务系统](http://bkjws.sdu.edu.cn/)

##  1. <a name='quickstart'></a>quick start

```python
from sdu_bkjws import SduBkjws

sdu_bkjws = SduBkjws('student_id', 'password')
sdu_bkjws.get_lesson()
sdu_bkjws.get_past_score()
sdu_bkjws.update_contact_info(english_name='my English name', phone_number='my new phone number')
```

##  2. <a name=''></a>安装
`sdu-bkjws`提供pypi的安装方式
```
(sudo) pip install sdu-bkjws
```

##  3. <a name='sdu-bkjws'></a>sdu-bkjws
在`sdu-bkjws`模块中,只有一个类`SduBkjws`,包括了本库提供的所有方法.

[TOC]

===============
- [SduBkjws.session()和SduBkjws.lessons](#SduBkjws.session()和SduBkjws.lessons)
- [SduBkjws.login()和Sdubkjws.session](#SduBkjws.login()和Sdubkjws.session)
- SduBkjws.get_lesson()
- SduBkjws.lessons()
- SduBkjws.get_fail_score()
- SduBkjws.detail()
- SduBkjws.get_detail()
- SduBkjws.get_raw_past_score()
- SduBkjws.get_past_score()
- SduBkjws.get_raw_now_score()
- SduBkjws.get_now_score()
- SduBkjws.update_contact_info()
- SduBkjws.get_multi_rank_with_query()
- SduBkjws.get_rank_with_query()
- SduBkjws.comment_lesson()
- SduBkjws.get_comment_lesson_info()
- SduBkjws.get_exam_time()
###  3.1. <a name='-1'></a>类初始化
```python
from sdu_bkjws import SduBkjws

sdu_bkjws = SduBkjws('student_id', 'password')
```
`student_id`为学号,`password`为密码
在初始化是会进行登录.

帐号或密码错误时会抛出异常.

###  3.2. <a name='SduBkjws.loginSdubkjws.session'></a>SduBkjws.login()和Sdubkjws.session
`login()`会使用初始化时传递的`student_id`和`password`做为学号和密码尝试登录.tudent_id`self.session``requests.Session()`对象,已经处于登录状态.

requests.session的使用参见[requests高级用法](http://docs.python-requests.org/zh_CN/latest/user/advanced.html)
###  3.3. <a name='SduBkjws.update_contact_info'></a>    SduBkjws.update_contact_info()
```
    def update_contact_info(self, english_name='', phone_number='', postcode='', address=''):
```

###  3.4. <a name='SduBkjws.get_lessonsSduBkjws.lessons'></a>SduBkjws.get_lessons()和SduBkjws.lessons
`get_lesson()`方法返回一个用dict组成的list,每个dict包含一节课的所有信息.
`lessons`属性与`get_lesson`返回方法相同,`get_lesson()`的返回值会自动保存在`lessons`属性中.如果未调用过`get_lesson()`而直接获取`lessons`时会自动调用`get_lesson()`

example
```json
[{"credit": "2",
  "days": "3",
  "lesson_name": "传统文学修养(国学)",
  "lesson_num_long": "sd00510170",
  "lesson_num_short": "605",
  "place": "中心理综楼313d",
  "school": "文学院",
  "teacher": "赵焕祯4",
  "times": "5",
  "weeks": "111111111111111111000000"}]
```
各项含义:
- `credit`:学分
- `days`上课日期
- `lesson_name`课程名
- `lesson_num_long` 课程号
- `lesson_num_short` 课序号
- `place`上课地点
- `school`开课学院
- `teacher`教师
- `times`上课节次 `1`表示上午第一大节,`2`表示上午第二大节.`3`表示下午第一大节,`4`表示下午第二大节.`5`表示晚上第一大节
- `weeks` 上课周次.如`week[n-1]`为`1`表示n周上课,为`0`表示不上课.

###  3.5. <a name='SduBkjws.get_detailSduBkjws.detail'></a>SduBkjws.get_detail()和SduBkjws.detail
获取学籍信息.
 `get_deail()`的结果会保存在`detail`中,在未调用过`get_detail`的情况下会自动调用`get_detail()`
 
 返回值: dict
 example:
 ```json
 {
    "object": {
        "xh": "学号",
        "xm": "姓名",
        "ywxm": "英文姓名",
        "sfzh": "身份证号",
        "xb": "性别",
        "mz": "民族",
        "jg": "籍贯",
        "csrq": "出生日期",
        "zzmm": "政治面貌",
        "xsh": "不能确定具体含义",
        "zyh": "不能确定具体含义",
        "zyfx": null,
        "bm": "班号",
        "rxnj": "入学年级",
        "ssnj": "我的这一项与入学年级相同,不能确定具体含义",
        "xslb": "学生类别 城市应届，农村应届，城市往届，农村往届",
        "sflb": "不能确定具体含义",
        "sfyxj": "不能确定具体含义",
        "kq": "考区",
        "byzx": "毕业中学",
        "gkzf": "高考总分",
        "wyyz": "外语语种",
        "ssdz": "宿舍地址,但实际内容是外语成绩 ",
        "dexwxsh": "不能确定具体含义",
        "dexwzyh": "不能确定具体含义",
        "dexwbm": "不能确定具体含义",
        "bylb": "不能确定具体含义",
        "flfx": "不能确定具体含义",
        "byrq": "毕业日期",
        "byzsbh": "不能确定具体含义",
        "xwzsbh": "不能确定具体含义",
        "bz": "不能确定具体含义",
        "lqh": "不能确定具体含义",
        "gkksh": "高考考号",
        "xw": "学位",
        "ycsj": "不能确定具体含义",
        "pyfs": null,
        "xmpy": "姓名拼音首字母,小写",
        "rxrq": "入学日期,格式为YYYYMMDD",
        "xklb": "不能确定具体含义,可能是学科类别",
        "xkmlm": "学科门类",
        "xz": "学制",
        "ydf": "不能确定具体含义",
        "ympy": "不能确定具体含义",
        "xsm": "学院",
        "xsjc": "学院",//不能确定以上两个学院的区别,希望有人可以提供更多信息.
        "zym": "专业名",
        "txdz": "不能确定具体含义",
        "yb":,"邮编"
        "lxdh": "不能确定具体含义",
        "id": "id,同学号"
    }
```
###  3.6. <a name='score'></a>score
1
####  3.6.1. <a name='get_now_score'></a>get_now_score()
2
####  3.6.2. <a name='get_past_score'></a>get_past_score()
3
####  3.6.3. <a name='get_raw_now_score'></a>get_raw_now_score()
4
####  3.6.4. <a name='get_rank_with_query'></a>get_rank_with_query
5
####  3.6.5. <a name='get_multi_rank_with_query'></a>get_multi_rank_with_query
6
###  3.7. <a name='exam'></a>exam
7
####  3.7.1. <a name='get_exam_time'></a>get_exam_time()
8
###  3.8. <a name='comment'></a>comment
9
####  3.8.1. <a name='get_comment_lesson_info'></a>get_comment_lesson_info()
0
####  3.8.2. <a name='comment_lesson'></a>comment_lesson
尚未完成
