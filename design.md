# 设计文档

## 用户系统
operator预先在班级中导入新生的`学号+姓名`，建立unregistered状态用户。

用户通过`学号+姓名`验证激活账号，设置邮箱和密码，激活后为normal状态。

毕业后可改为readonly状态，即只读。

用户通过`学号/邮箱 + 密码`登录，operator无学号，由sysadmin建立。

> 注：学号在内部为字符串，保留可扩展性

## 班级与operator
班级创建、operator创建、operator权限设置，由且仅由sysadmin进行操作。

operator对一个班级的权限：无、只读(1)、读写(2)
