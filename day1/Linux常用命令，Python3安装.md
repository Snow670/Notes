## 一 、设置centos7自动root用户登录

1、当前普通用户登录，想要切换为root用户，需要输入命令

```
su
```

​    想要从root用户切换到普通用户，只需要输入

```
su  用户名
```

2、在命令窗口输入：

```
vim /etc/gdm/custom.conf 
```

3、按i键进入编辑，在`在daemon下面添加`

```
 AutomaticLoginEnable=True
 AutomaticLogin=root 
```



## 二、源码安装python3.7.7

更新yum :yum update

yum -y install gcc gcc-c++

yum -y install openssl openssl-devel

yum install zlib zlib-devel bzip2 bzip2-devel  ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-deve

yum -y install libffi-devel    #pip编译

地址 https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
进入opt目录 下载 : wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
解压 tar -zxvf Python-3.7.7.tgz 
cd Python-3.7.7 文件夹中
./configure --prefix=/usr/local/python3 编译到/usr/local/python3
make
make install 
创建python3的软连接： ln -s /usr/local/python3/bin/python3 /usr/bin/python3
创建pip3的软连接：ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3



yum -y install epel-release 源

## 三、用户操作

————————-记得要在root用户下————————-

1.新建用户
adduser testuser //新建testuser 用户
passwd testuser //给testuser 用户设置密码

2.建工作组
groupadd testgroup //新建test工作组

3.新建用户同时增加工作组
useradd -g testgroup testuser //新建testuser用户并增加到testgroup工作组

//注：：-g 所属组 -d 家目录 -s 所用的SHELL

4.给已有的用户增加工作组
usermod -G groupname username

5.临时关闭
在/etc/shadow文件中属于该用户的行的第二个字段（密码）前面加上就可以了。想恢复该用户，去掉即可
//或者使用如下命令关闭用户账号：
passwd testuser –l
//重新释放：
passwd testuser –u

6.永久性删除用户账号
userdel testuser
groupdel testgroup
usermod –G testgroup testuser //（强制删除该用户的主目录和主目录下的所有文件和子目录）

7.显示用户信息
id user
cat /etc/passwd

补充:查看用户和用户组的方法
用户列表文件：/etc/passwd
用户组列表文件：/etc/group
查看系统中有哪些用户：cut -d : -f 1 /etc/passwd
查看可以登录系统的用户：cat /etc/passwd | grep -v /sbin/nologin | cut -d : -f 1
查看用户操作：w命令(需要root权限)
查看某一用户：w 用户名
查看登录用户：who
查看用户登录历史记录：last

























