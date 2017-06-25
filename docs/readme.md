# 关于sdu_bkjws

学校之前新换了一套教务系统,应该会使用比较长的一段时间.
所以写一个python的包来减少一些重复的工作.

## 开始

```
from sdu_bkjws import SduBkjws

sdu_bkjws = SduBkjws('student_id', 'password')
```

当初始化class的时候,会常识登陆.如果账号密码错误,会在此报错.

## 获取课表

```
from sdu_bkjws import SduBkjws

sdu_bkjws = SduBkjws('student_id', 'password')
sdu_bkjws.get_lesson()
print(sdu_bkjws.lessons)
```

在使用`lessons`属性获取课表之前,需要使用`get_lesson()`方法来获取课表.
当然,`get_lesson()`方法同样也会返回课表.