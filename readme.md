master: [![Build Status](https://travis-ci.org/Trim21/sdu_bkjws.svg?branch=master)](https://travis-ci.org/Trim21/sdu_bkjws)
dev: [![Build Status](https://travis-ci.org/Trim21/sdu_bkjws.svg?branch=dev)](https://travis-ci.org/Trim21/sdu_bkjws)

一个用来解析山东大学教务系统的库

(似乎清华用的也是这个系统)

因为所用到的依赖beautifulsoup4不支持python2,所以本项目不会支持python2

done:
- 登录
- 获取个人信息
- 更新联系方式
- 课程
- 本学期成绩
- 往年成绩
- 查询成绩排名

todo:
- 获取教学计划 
- 添加课程(bkjwxk)
- 查询课程信息(bkjwxk)

for contributor:

creat a `keys.json` in `test` dir
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