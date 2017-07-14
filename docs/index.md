---
layout: post
title: sdu-bkjws 介绍
---
<!--[![PyPI version](https://badge.fury.io/py/sdu-bkjws.svg)](https://badge.fury.io/py/sdu-bkjws)-->
version: 1.0.0

<!-- TOC -->

 [TOC]
 
<!-- /TOC -->


sdu-bkjws是为简化与山东大学教务系统交互而写的库

[山东大教务系统](http://bkjws.sdu.edu.cn/)

##  1. quick start

```python
from sdu_bkjws import SduBkjws

sdu_bkjws = SduBkjws('student_id', 'password')
sdu_bkjws.get_lesson()
sdu_bkjws.get_past_score()
sdu_bkjws.update_contact_info(english_name='my English name', phone_number='my new phone number')
```

##  2. 安装
`sdu-bkjws`提供pypi的安装方式
```
(sudo) pip install sdu-bkjws
```

##  3. sdu-bkjws
在`sdu-bkjws`模块中,只有一个类`SduBkjws`,包括了本库提供的所有方法.

###   类初始化
```python
from sdu_bkjws import SduBkjws

sdu_bkjws = SduBkjws('student_id', 'password')
```
`student_id`为学号,`password`为密码
在初始化是会进行登录.

帐号或密码错误时会抛出异常.
### session
#### SduBkjws.login()和Sdubkjws.session
`login()`会使用初始化时传递的`student_id`和`password`做为学号和密码尝试登录.tudent_id`self.session``requests.Session()`对象,已经处于登录状态.

requests.session的使用参见[requests高级用法](http://docs.python-requests.org/zh_CN/latest/user/advanced.html)

### 个人信息

#### SduBkjws.get_detail()和SduBkjws.detail
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
如果你能确定某项的含义,希望你能提供帮助.

#### SduBkjws.update_contact_info()
```
SduBkjws.update_contact_info(self, english_name='my english name', phone_number='my new phone number, postcode='my new postcode', address='my new address')
```
如果你不想更改某一项,不要传递相应的参数.

### lesson
#### SduBkjws.lessons
由dict组成的list
每个dict包含一节课的所有信息.

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

#### SduBkjws.get_lessons()
从系统请求并解析课程信息.
返回SduBkjws.lessons

###   score
score是与成绩有关的部分
####   SduBkjws.get_now_score()
获取本学期成绩 返回一个dict组成的list
example:
```json
[{
  "bm": "str 班名",
  "bz": "NoneType 不能确定具体含义",
  "cxbkbz": "NoneType 不能确定具体含义",
  "djm": "NoneType 不能确定具体含义",
  "id": "NoneType 不能确定具体含义",
  "jsh": "str 教师号",
  "jsm": "str 教师名",
  "kccj": "NoneType 不能确定具体含义",
  "kch": "str 课程号",
  "kcm": "str 课程名",
  "kcsx": "str 课程属性,必修/限选/任选",
  "kkxsh": "str 不能确定具体含义",
  "kscj": "float 考试成绩",
  "kscjView": "str 同kscj",
  "kssj": "str 考试时间,format:YYYYMMDD",
  "kxh": "int 课序号",
  "lrzt": "str 不能确定具体含义",
  "pscj": "float 平时成绩",
  "pscjView": "str 平时成绩",
  "qmcj": "str 期末成绩",
  "qmcjView": "str 期末成绩",
  "qzcj": "float 期中成绩",
  "qzcjView": "str 期中成绩",
  "sfjscj": "str 不能确定具体含义",
  "sycj": "float 不能确定具体含义",
  "sycjView": "str 不能确定具体含义",
  "xf": "float 学分",
  "xh": "str 学好",
  "xm": "str 姓名",
  "xnxq": "str 学年学期 YYYY-YYYY-N",
  "xs": "float 学时",
  "xsh": "str 不能确定具体含义",
  "xsjc": "str 开课学院",
  "zczt": "str 不能确定具体含义"
}]
```
####   SduBkjws.get_past_score()
返回数据同`SduBkjws.get_now_score()`
####   SduBkjws.get_raw_now_score()
向教务系统进行请求返回的原始内容.不建议使用.
####   SduBkjws.get_rank_with_query
```
    def get_rank_with_query(self, lesson_num_long, lesson_num_short, exam_time):
```
查询条件:
- `lesson_num_long`
- `lesson_num_short`
- `exam_time`

三者为且关系,必须同时符合.

####   SduBkjws.get_multi_rank_with_query(query: list)
参数接受一个list[dict] 

dict:

```python
{ 'lesson_num_long':'',
  'lesson_num_short':''
  'exam_time':''}
```
dict之间为货关系,dict之内为且关系.
###   exam
####   SduBkjws.get_exam_time(xnxq)
获取某学年学期的考试时间
xnxq格式:`${开始年份}-${结束年份}-${学期}`
比如2016-2017年学春季学期就是`2016-2017-2`
###   comment
####   SduBkjws.get_comment_lesson_info()
获取所有需要评教的课程信息
返回一个list[dict]
example:
```json
[ {"cpxxbid": "不能确定具体含义",
  "id": "不能确定具体含义",
  "jsh": "教师号,",
  "jsm": "教师名",
  "kch": "课程号",
  "kcm": "课程名",
  "pgcs": "int 评教次数",
  "sfcp": "str 不能确定具体含义",
  "wqid": "str,但内容是int 不能确定具体含义",
  "xh": "学号",
  "xm": "姓名",
  "xnxq": "学年学期",
  "xsh": "str 但内容为int 不能确定具体含义"}]
```
####   SduBkjws.comment_lesson
此方法尚未完成
