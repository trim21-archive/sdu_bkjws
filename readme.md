master: [![Build Status](https://travis-ci.org/Trim21/sdu_bkjws.svg?branch=master)](https://travis-ci.org/Trim21/sdu_bkjws)
dev: [![Build Status](https://travis-ci.org/Trim21/sdu_bkjws.svg?branch=dev)](https://travis-ci.org/Trim21/sdu_bkjws)

pypi:[https://pypi.python.org/pypi/sdu-bkjws](https://pypi.python.org/pypi/sdu-bkjws)

一个用来解析山东大学(shandong university)教务系统的库 包括查成绩 获取课表 查询成绩排名

(似乎清华用的也是这个系统)

python2未经测试

## [Docs](https://github.com/Trim21/sdu_bkjws/blob/dev/docs/index.md)

## todo:
- 获取教学计划 
- 添加课程(bkjwxk)
- 查询课程信息(bkjwxk)


## [changelog](https://github.com/Trim21/sdu_bkjws/blob/master/CHANGELOG.md#100-2017-07-03)


## for contributor:

### method of test
1. create a `keys.json` in `test` dir
```json
{
    "student_id": "student_id",
    "password": "password"
}
```

then 
```
python -m unittest test
```
or 

2. export `student_id` and `password` to environment