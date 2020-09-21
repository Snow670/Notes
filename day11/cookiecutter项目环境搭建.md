## Centos8下部署Python项目

#### 一、配置系统环境

1. 更新一下yum：yum upgrade

2. yum -y install epel-release

3. yum -y install gcc gcc-c++ 编译的时候

4. yum -y install wget 

5. yum -y install zlib zlib-devel zlib* openssl openssl-devel ncurses-devel sqlite sqlite-devel bzip2-devel readline-devel tk-devel gdbm-devel xz-devel

6. 编译Python时候，如果缺少，会导致pip安装不成功:    yum -y install libffi-devel 

7. 帮助管理/proc目录，fuser，killall,pstree等:    yum install psmisc 

#### 二、源码安装Python3.7.8

1. cd /opt 进入opt目录

2. 使用wget命令下载压缩包 wget https://www.python.org/ftp/python/3.7.8/Python-3.7.8.tgz

3. tar -zxvf Python-3.7.8.tgz

4. cd Python-3.7.8

5. ./configure --prefix=/usr/local/python3

6. make 

7. make install

8. 创建软链接      ln -s /usr/local/python3/bin/python3 /usr/bin/python3

   如果建立错了，删除软连接 rm -rf /usr/bin/python3

   ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

#### 三、源码安装Django

9. 给python3安装django   

   pip3 install django

   建立软连接

   ln -s /usr/local/python3/bin/django-admin /usr/bin/django-admin

10. 出错：SQLite 3.8.3 or later is required (found 3.7.17)

    (执行python3 manage.py makemigtations)

参考：https://blog.csdn.net/qq_39969226/article/details/92218635

wget https://www.sqlite.org/2019/sqlite-autoconf-3300100.tar.gz

11. 关闭防火墙: 

    查看防火墙状态: firewall-cmd --state 

    停止防火墙: systemctl stop firewalld.service 

    禁止firewall开机启动: systemctl disable firewalld.service 

#### 四、源码安装uwsgi

12. 从网站https://uwsgi-docs.readthedocs.io/en/latest/Download.html下载最新版uwsgi，下载

Stable/LTS版本的源文件

13. tar -zxvf uwsgi压缩包文件

14. cd uwsgi解压过的目录

15. 安装：python3 setup.py install
16. 建立软连接： ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi 

17. 安装完成后，使用uwsgi运行

#### 五、安装配置nginx，配置uwsgi

1. yum -y install nginx      启动nginx：nginx

   nginx 常见指令：启动 nginx       重启（ nginx -s reload）  

   检查nginx.conf有没有错（nginx -t）    关闭(nginx -s stop)

   查看进程  ps -ef | grep nginx

2. 将server_name 改成自己ip地址

3. 配置location

   ```
   include uwsgi_params; uwsgi_pass 127.0.0.1:8000;
   ```

4. 在location下新建另一个新的location

   ```
   location /static {
   alias /root/www/unicom/static; //改成你自己的
   }
   ```

5. 在manage.py的同级目录下，新建一个uwsgi.ini文件，配置此文件

   ```python
   [uwsgi] 
   master = true //主进程
   socket = 127.0.0.1:8000 //对本机8000端口提供服务
   chdir = /home/feixue/python/www/for_test //项目根目录 
   module = for_test.wsgi:application //指定wsgi模块 
   daemonize = /home/feixue/python/www/for_test/run.log // 日志文件 
   disable-logging = true //不记录正常信息，只记录错误信息
   #vhost = true //多站模式 
   #no-site = true //多站模式时不设置入口模块和文件 
   #workers = 2 //子进程数 
   #reload-mercy = 10 
   #vacuum = true //退出、重启时清理文件 
   #max-requests = 1000 
   #limit-as = 512 
   #buffer-size = 30000 
   #pidfile = /var/run/uwsgi9090.pid //pid文件，用于下脚本启动、停止该进程 
   ```

6. 进入项目目录下，启动服务:uwsgi uwsgi.ini

7. 将settings.py中ALLOWED_HOSTS = ['自己的ip']            DEBUG = False

8. 重新运行服务:先删除之前uwsgi进程：killall -9 uwsgi

9. 再次启动 uwsgi uwsgi.ini

10. 启动Django项目,如果出现Error:That port is already in use. 关掉8000的进程就好 sudo fuser -k

8000/tcp

#### 六、创建管理员账号

1. python3 manage.py createsuperuser 根据提示输入用户名，邮箱，密码等就可以。

2. 这个时候访问到的admin模块是没有静态资源的

#### 七、配置静态资源

1. 打开django项目中settings.py文件（/unicom/settings.py），添加 STATIC_ROOT =

‘/root/www/unicom/static/’

2. 运行python3 manage.py collectstatic，此命令是搜集静态文件的命令，搜集后的静态文件存放

在/root/www/unicom/static/中 

3. 重新启动uwsgi和nginx： nginx -s reload 		uwsgi uwsgi.ini

4. 配置templates中的 DIRS:[os.path.join(BASE_DIR,'templates')]

## cookiecutter项目环境搭建

#### 一、centos8安装pipenv

1. pip3 install pipenv

2. 建立软连接 ln -s /usr/local/python3/bin/pipenv /usr/bin/pipenv

   


#### **二、cookiecutte **生成itclub

```python
安装Cookiecutter

参考教程：https://www.cnblogs.com/taceywong/p/10506032.html

安装步骤：

1.安装git                  yum install -y git

2.安装cookiecutter         pip3 install cookiecutter

3.创建软连接                 
ln -s /usr/local/python3/bin/cookiecutter /usr/bin/cookiecutter

（不知道在哪儿可以用命令：find / -name cookiecutter 查找）

4.创建项目         
cookiecutter https://github.com/pydanny/cookiecutter-django.git
```

1. 回到root目录下

2. 创建项目    cookiecutter https://github.com/pydanny/cookiecutter-django.git

3. 按照提示一顿操作

4. 执行过程：

   ```bash
   project_name [My Awesome Project]: itclub
   project_slug [itclub]:
   description [Behold My Awesome Project!]:
   author_name [Daniel Roy Greenfeld]: snow
   domain_name [example.com]:
   email [jairo@example.com]: 1419517126@qq.com
   version [0.1.0]:
   Select open_source_license:
   1 - MIT
   2 - BSD
   3 - GPLv3
   4 - Apache Software License 2.0
   5 - Not open source
   Choose from 1, 2, 3, 4, 5 [1]:5
   timezone [UTC]: Asia/shanghai
   windows [n]: n
   use_pycharm [n]: y
   use_docker [n]:
   Select postgresql_version:
   1 - 11.3
   2 - 10.8
   3 - 9.6
   4 - 9.5
   5 - 9.4
   Choose from 1, 2, 3, 4, 5 [1]:
   Select js_task_runner:
   1 - None
   2 - Gulp
   Choose from 1, 2 [1]:
   Select cloud_provider:
   1 - AWS
   2 - GCP
   3 - None
   Choose from 1, 2, 3 [1]: 3
   Select mail_service:
   1 - Mailgun
   2 - Amazon SES
   3 - Mailjet
   4 - Mandrill
   5 - Postmark
   6 - Sendgrid
   7 - SendinBlue
   8 - SparkPost
   9 - Other SMTP
   Choose from 1, 2, 3, 4, 5, 6, 7, 8, 9 [1]: 9
   use_async [n]: 
   use_drf [n]:
   custom_bootstrap_compilation [n]:
   use_compressor [n]: y
   use_celery [n]: y
   use_mailhog [n]:
   use_sentry [n]:
   use_whitenoise [n]: y
   use_heroku [n]:
   Select ci_tool:
   1 - None
   2 - Travis
   3 - Gitlab
   Choose from 1, 2, 3 [1]:
   keep_local_envs_in_vcs [y]: n
   debug [n]: y
    [WARNING]: You chose not to use a cloud provider, media files won't be served in production.
    [SUCCESS]: Project initialized, keep up the good work!
   ```

5. cd itclub下 

6. 创建本项目的虚拟环境   pipenv --python 3.7

7. 虚拟环境地址： /root/.local/share/virtualenvs/itclub-hhe5if0D

   


#### 三、配置pycharm远程连接

1. 创建空文件夹itclub，用pycharm打开
2. **配置deployment**

![image-20200813103552797](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813103552797.png)		

- 2.1点击+，选择SFTP，给服务器起名字

.			![image-20200813103628827](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813103628827.png)

- 2.2.配置ssh连接服务器

![image-20200813103857520](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813103857520.png)	

- 2.3.连接服务器

![image-20200813104042686](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813104042686.png)					

- 2.4配置上传路径及服务器IP

![image-20200813104405840](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813104405840.png)				

- 2.5.文件意义

​    	 1 Mapping 本地和远程项目目录映射关系

​			![image-20200813195725351](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813195725351.png)

​     	2 root path +deployment path 要等于远程的项目路径

​    	 3 Excluded Paths 添加一些不需要同步到远程的路径，或者不需要下			载到本地的路径

3. **连接到服务器上的Python解释器**

   ​	settings中配置Python interpreter，点击齿轮，点击show all，点击+，选择SSH Inteerpreter,

​	![image-20200813105918542](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813105918542.png)

​		选择move,然后next,通过命令pipenv --py查看解析器路径，填入，并编辑Sync folders

​		![image-20200813110402872](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813110402872.png)



4. **同步文件，选择Sync**

![image-20200813111203066](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813111203066.png)

5. **检查**

   此时，试着修改下本地的文件，看看文件更新以后，提交到/root下的哪儿，如果，提交的位置有问题，那么执行上述的2.4-2.5

6. **配置Django服务器**

   6.1.首先点击

​			![image-20200813111756611](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813111756611.png)

​		6.2.点击+，选择Django Server

​		6.3.配置信息

​				![image-20200814113129148](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200814113129148.png)

​		6.4.logs里面勾选下面两个console，选择apply , ok完成

​		6.5.settings中查找django，点击后

​			![image-20200813112445685](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813112445685.png) 

​		6.6.勾选，并选择文件

![image-20200813112756932](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813112756932.png)

​		6.7.再进行配置

​			![image-20200813113019981](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200813113019981.png)

​		6.8.运行下即可



#### 四、mysql8和数据库用户设置

```python
#mysql8的yum安装方式及连接Navicat报错处理
https://www.cnblogs.com/kevingrace/p/10482469.html
```

登录数据库：mysql -u root -p

1. 创建主数据库：create database itclub charset utf8;

2. 创建测试数据库：create database test_itclub charset utf8;

3. 开发阶段创建账户，设置所有的IP都可以访问：

​	create user 'itclub'@'%' identified by '12345678';

4. 授权itclub账户拥有itclub数据库的所有权限：

​	grant all on itclub.* to 'itclub'@'%';

​	grant all on test_itclub.* to 'itclub'@'%';

5. 更新权限：flush privileges;

6. 退出：exit



#### 五、修改项目目录

1. config 配置文件夹

包括settings的配置，路由配置，wsgi服务器的配置

2. docs 文档目录，因为后续自己写文档，所以清空一下

3. locale 国际化相关的，python manage.py makemessages 给你翻译成对应语言

4. requirements 项目依赖的包

5. utility 本项目需要的脚本和工具，因为系统环境需要自己安装和配置，所以清空一下

6. bwitclub 下的contrib 数据库

7. bwitclub下的 static ，sass，less 动态化的css

8. users 应用：已经完成了登录注册找回密码这些功能，adapters.py 将来用于继承django-allauth

第三方登录

9. conftest.py ，用pytest测试时候使用的文件

10. .editorconfig 编辑器相关的配置

11. .pylintrc 检查代码是否符合PEP8规范



#### 六、安装依赖，运行项目

1. 修改base.txt

   ```python
   #修改django的版   
   django == 2.2.13
   #配置连接数据库的引擎 
   mysqlclient==2.0.1
   ```

2. 修改production.txt

   ```python
   # 注释掉 django-anymail==7.2.1 # https://github.com/anymail/django-anymail
   ```

3. 修改Pipfile的安装源

   ```python
   url = "https://mirrors.aliyun.com/pypi/simple/"
   ```

4. 服务器上安装本地运行环境的依赖： 

   pipenv install -r requirements/local.txt
   
   ```python
   #若此时安装报错：OSError: mysql_config not found
   #原因是linux需要mysql相关的一些依赖包
   #执行命令
   yum install mysql-devel gcc gcc-devel python-devel(centos7)
   yum install mysql-devel gcc(centos8)
   ```
   
   

#### 七、settings配置

1. base.py 

```python
# 设置找到文件路径，也就是最外层的bwitclub，使用的是django-environ 

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent 

# 开发过程中使用本地的 .env文件配置 （创建.env文件）

READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True) 

# 时区和编码语言 

TIME_ZONE = "Asia/Shanghai" 

LANGUAGE_CODE = "zh-Hans"

# 是否将mysql的http请求封装成事务 

DATABASES["default"]["ATOMIC_REQUESTS"] = True 

# 打开humanize 

"django.contrib.humanize" 

# 暂时不写后台，去掉 "django.contrib.admin", 

# 改为False 

CSRF_COOKIE_HTTPONLY = False 

# 发送邮件配置，从 .env 文件中读取的配置 

EMAIL_HOST = env('DJANGO_EMAIL_HOST')
EMAIL_USE_SSL = env('DJANGO_EMAIL_USE_SSL',default=True)
EMAIL_PORT = env('DJANGO_EMAIL_PORT',default=465)
EMAIL_HOST_USER = env('DJANGO_EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('DJANGO_EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DJANGO_DEFAULT_FROM_EMAIL')

# 去掉后台管理的配置 

# ADMIN 

# -------------------------------------------------------------------------- 

# Django Admin URL. 
ADMIN_URL = "admin/" 
# https://docs.djangoproject.com/en/dev/ref/settings/#admins 
ADMINS = [("""Bruce""", "bruce@example.com")] 
# https://docs.djangoproject.com/en/dev/ref/settings/#managers 
MANAGERS = ADMINS 

--------------------------------------------------------
# 修改celery的配置 

CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND") 

# 指定接收的内容类型，增加msgpack数据类型,它比json的序列化更小更快 

CELERY_ACCEPT_CONTENT = ["json","msgpack"] 

# 任务序列化与反序列化使用msgpack，msgpack是一个二进制的json序列化方案 

CELERY_TASK_SERIALIZER = "msgpack" 

# 读取任务一般性能要求不高，使用可读性更好的json就可以 

CELERY_RESULT_SERIALIZER = "json" 

# 单个任务的最大运行时间为5分钟 

CELERY_TASK_TIME_LIMIT = 5 * 60 

# 任务的软时间限制，超时会抛出SoftTimeLimitExceeded异常 

CELERY_TASK_SOFT_TIME_LIMIT = 60 
```

2. local.py 

```python
ALLOWED_HOSTS = ["*"] 

EMAIL相关的配置删除
```

3. production.py 

```
admin 

email 

media 

static 

Anymail 

这几个部分全部删除
```



4. .env

```python
#MySQL
DATABASE_URL=mysql://root:123456@127.0.0.1/itclub
#REDIS
REDIS_URL=redis://127.0.0.1:6379

DJANGO_DEBUG=True
DJANGO_SECRET_KEY=ePUsvlGl8nZEouakbRewlpTQ2shFik66ZnBCpNgT6FtW5FEQmiWVNg3tTvDWaf1N

#Email
DJANGO_EMAIL_USE_SSL=True
DJANGO_EMAIL_HOST=smtp.qq.com
DJANGO_EMAIL_PORT=465
DJANGO_EMAIL_HOST_USER=1419517126@qq.com
DJANGO_EMAIL_HOST_PASSWORD=hcuuamtyygumjaee
DJANGO_DEFAULT_FROM_EMAIL=1419517126@qq.com
#Celery
CELERY_BROKER_URL=redis://127.0.0.1:6379/1
CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/2
```

5. config下的wsgi

   ```python
   os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
   ```

6.找到users下的admin.py删除

7.项目总的urls.py(config下)，删除admin相关的

8.去虚拟环境中同步数据库：pipenv run python manage.py migrate，运行项目



#### 八、用户模型类 models.py

1. 自定义用户模型

   ```python
   """自定义用户模型"""
   nickname = models.CharField(null=True,blank=True, max_length=255,verbose_name='昵称')
   job_title = models.CharField(max_length=50,null=True,blank=True,verbose_name='职称')
   introduction = models.TextField(blank=True,null=True,verbose_name='简介')
   avatar = models.ImageField(upload_to='user_avatars/',null=True,blank=True,verbose_name='用户头像')
   location = models.CharField(max_length=50,null=True,blank=True,verbose_name='城市')
   personal_url = models.URLField(max_length=255,null=True,blank=True,verbose_name='个人链接')
   weibo = models.URLField(max_length=255, null=True, blank=True, verbose_name='微博链接')
   zhihu = models.URLField(max_length=255, null=True, blank=True, verbose_name='知乎链接')
   github = models.URLField(max_length=255, null=True, blank=True, verbose_name='github链接')
   linkedin = models.URLField(max_length=255, null=True, blank=True, verbose_name='领英链接')
   created_at = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
   update_at = models.DateTimeField(auto_now=True,verbose_name='更新时间')
   
   # 定义元数据
       class Meta:
           verbose_name = '用户'
           verbose_name_plural = verbose_name
           
   # 定义直观读取usename的方法
       def __str__(self):
           return self.username
       
   # nickname不存在就返回username
       def get_profile_name(self):
           if self.nickname:
               return self.nickname
           return self.username
       
       def get_absolute_url(self):
           """Get url for user's detail view.
           Returns:str: URL for user detail.
           """
           return reverse("users:detail", kwargs={"username": self.username})
   ```

   

2. AbstractUser

   ```python
   #AbstractUser源码中有email
   email = models.EmailField(_('email address'), blank=True)
   # 可以不用写create_at 和 updated_at ,但是为了做到统一就填上了
   date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
   ```

   

3. 设置项目兼容Python2.x版本

   ```python
   from __future__ import unicode_literals
   from django.db import models
   from django.utils.encoding import python_2_unicode_compatible
   
   @python_2_unicode_compatible
   class User(AbstractUser):
   ```

   

4. 同步数据库

```python
1. pipenv run python manage.py makemigrations

You are trying to add the field 'created_at' with 'auto_now_add=True' to user without a default; the database needs something to populate existing rows.

 1) Provide a one-off default now (will be set on all existing rows)
 2) Quit, and let me add a default in models.py
Select an option: 1     # 输入1，提供当前时间
Please enter the default value now, as valid Python
You can accept the default 'timezone.now' by pressing 'Enter' or you can provide another value.
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
[default: timezone.now] >>>      #直接回车


2. pipenv run python manage.py migrate
```



#### 九、第三方登录

1. Django-Allauth             3days ago   star : 5700

   ```python
   文档地址：https://django-allauth.readthedocs.io/en/latest/
   ```

2. Django Social Auth     7 years ago   star ：2600

3. Python-Social-Auth   4 years ago    star: 2800



#### 十、修改itclub

```python
# 安装sorl-thumbnail
pipenv install sorl-thumbnail
在base.py 第三方Apps 'sorl.thumbnail',

# config/urls.py
path("", TemplateView.as_view(template_name="base.html"), name="home"),

#只要有报错，就修改href="#"(base.html)
#例如：
<li class="nav-item"><a class="nav-link" href="#">&nbsp;&nbsp;首页</a></li>
```



#### 十一、集成第三方账号，github为例

```python
# 第一步
# base.py
THIRD_PARTY_APPS = [
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "django_celery_beat",
    'sorl.thumbnail',
]

# 第二步，github上获取Client ID和Client Secret
settings下的Developer settings  下的 OAuth Apps
地址：https://github.com/settings/developers
  
Client ID
e14fd578d080d6572018
Client Secret
2fc32ee84ec73fbff5ebe34dc725fd8611ccfa43

# 第三步
socialaccount_socialapp 数据库中增加一条记录
1 GitHub GitHub 4c62a239f66f5be85d87 644929ac62a5d762b13b405628548fb29bd5546b 
socialaccount_socialapp_sites 数据库中增加一条记录
1 1 1
```

#### 十二、QAuth2.0协议

| 角色                    | 作用                                                         |
| ----------------------- | ------------------------------------------------------------ |
| Third-party application | 第三方应用程序，又称客户端，比如：itclub                     |
| HTTP Service            | HTTP服务提供商，提供登录信息的一方，如GitHub                 |
| Resource Owner          | 资源所有者，又成用户，如：GitHub的用户                       |
| Use Agent               | 用户代理，如：浏览器                                         |
| Authorization Server    | 认证服务器，也就是HTTP服务提供商专门用来处理认证的服务器，   |
| Resource Server         | 资源服务器，也就是HTTP服务提供商专门用来处理认证的服务器，如：GitHub的认证服务器 |

![image-20200818084458282](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200818084458282.png)

A：网站应用请求用户授权

B: 用户授权

C:网站应用向第三方认证服务器请求token

D:应用拿到token，携带着token向资源服务器请求认证信息

E:资源服务器通过token判断请求是否合法，如果token正确，则发送认证信息到应用

F:登录成功

#### 十三、完成用户模块（users）

1. 删除无用的文件form.py

2. 修改views.py

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, RedirectView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = 'users/user_detail.html'
    slug_field = "username"
    slug_url_kwarg = "username"


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = 'users/user_form.html'
    fields = ["nickname","job_title","introduction","avatar","location","personal_url","weibo","zhihu","github","linkedin"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # return User.objects.get(username=self.request.user.username)
        return self.request.user


#class UserRedirectView(LoginRequiredMixin, RedirectView):

    #permanent = False

    #def get_redirect_url(self):
        #return reverse("users:detail", kwargs={"username": self.request.user.username})
```

3. 修改users下的urls,py

```python
from django.urls import path
from itclub.users import views


app_name = "users"
urlpatterns = [
    #path("~redirect/", view=views.UserRedirectView.as_view(), name="redirect"),
    path("~update/", view=views.UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=views.UserDetailView.as_view(), name="detail"),
]
```

4. 修改config下的base.py

```python
# LOGIN_REDIRECT_URL = "users:redirect"改为下面
LOGIN_REDIRECT_URL = "account_logout"
```

5. 修改apps.py

```python
from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "itclub.users"
    verbose_name = "用户"

    def ready(self):
        try:
            import itclub.users.signals  # noqa F401
        except ImportError:
            pass

```

6. 生成头像，首先在itclub下创建media文件夹，然后上传，修改页面中的字段picture改为avatar(因为model字段名改了)，如果本地没有的话，同步下代码

#### 十四、模型类、视图、网站编写测试用例

检验你写的代码的健壮性

1. 删除users/tests下的factory.py、test_task.py、forms.py

2. 删除utils下的conftest.py,conftest.py是test_case(测试模块)的配置文件

3. 安装django-test-plus

```python
#命令
pipenv install pytest-runner --dev
pipenv install pytest-django --dev
pipenv install django-test-plus --dev
```

4. models.py的测试用例

```python
#test_models.py
from test_plus.test import TestCase
class TestUser(TestCase):
    def setUp(self):
        self.user = self.make_user()
    def test__str__(self):
        self.assertEqual(self.user.__str__(),'testuser')

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(),"/users/testuser/")

    def test_get_profile_name(self):
        assert self.user.get_profile_name() == 'testuser'
        self.user.nickname = '昵称'
        assert self.user.get_profile_name() == '昵称'
```

​	点击三角形，点击run，开始测试

![image-20200820101142946](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200820101142946.png)

5. urls的测试用例

```python
#test_urls.py
from test_plus.test import TestCase
from django.urls import reverse,resolve
class TestUserURLs(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail',kwargs={'username':'testuser'}),'/users/testuser/')

    def test_detail_resolve(self):
        self.assertEqual(resolve('/users/testuser/').view_name,'users:detail')

    def test_update_reverse(self):
        self.assertEqual(reverse('users:update'), '/users/update/')

    def test_update_resolve(self):
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')
```

6. views的测试用例

```python
#只需要测试view就行
from django.test import RequestFactory
from test_plus.test import TestCase

from itclub.users.views import UserUpdateView


#需要把用到的公共信息提取到一个基类中
class BaseUserTestCase(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


#RequestFactory和真实的浏览器请求的区别:
# 就是RequestFactory模式不用再经过Django的中间件、路由、wsgi处理
class TestUserUpdateView(BaseUserTestCase):
    def setUp(self):
        super().setUp()
        self.view = UserUpdateView()
        request = self.factory.get("/fake-url")
        request.user = self.user
        self.view.request = request

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(),'/users/testuser/')

    def test_get_object(self):
        self.assertEqual(self.view.get_object(),self.user)

```

#### 十五、首页动态功能实现

1. 新建一个app，并将app移动到itclub下

```python
pipenv run python manage.py startapp news
```

2. 设计News的模型类

```python
from django.db import models
from django.conf import settings
import uuid


# Create your models here.
class News(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField(verbose_name='动态内容')
    # 用外键关联到User表
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='publisher', verbose_name='用户')
    # 用户评论，放在一张表中，设置一个bool值  A评论  B，C,D能不能回复A的评论呢，动态的发表者能不能回复评论呢？
    # 作者回复其他人，其他人也可以回复作者的，
    # 自关联 的关系   省-市-县   动态-评论-评论的回复
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE,
                               related_name="thread", verbose_name="自关联")

    # 一个人可以给多个动态点赞，一条动态也可以接受多个人的点赞：多对多的关系
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, null=True,
                                   related_name='liked_news', verbose_name='点赞用户')
    replay = models.BooleanField(default=False, verbose_name='是否为评论')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = '首页'
        verbose_name_plural = verbose_name
        ordering = ("-create_at",)

    def __str__(self):
        return self.content

    def switch_like(self, user):
        '''点赞和取消赞'''
        if user in self.liked.all():
            self.liked.remove(user)
        else:
            self.liked.add(user)

    # 判断parent是本身还是上一级记录
    def get_parent(self):
        if self.parent:
            return self.parent
        else:
            return self

    def reply_this(self, user, text):
        parent = self.get_parent()
        News.objects.create(
            user=user,
            content=text,
            replay=True,
            parent=parent
        )

    def get_thread(self):
        '''关联到当前记录的所有记录'''
        parent = self.get_parent()
        # 通过父记录查询到子记录
        return parent.thread.all()

    # 评论的数量
    def comment_count(self):
        return self.get_thread().count()

    # 点赞数
    def count_likers(self):
        return self.liked.all().count()
```

3. 注册到app中，然后迁移数据库

4. 设计News的views.py

```python
from django.shortcuts import render

# 网站需要登录后才能看到动态
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from bwitclub.news.models import News

class NewsListView(LoginRequiredMixin,ListView):
    model = News
    #queryset = News.objects.all()
    # 规定分页显示的条数
    paginate_by = 20
    #page_kwarg = 'p'
    # 定义queryset查询集在模板中的名字,默认情况下:模型类名_list或者object_list
    #context_object_name = 'news_list'
    # 排序  单个字段'create_at' 多个字段是元组('create_at','liked')
    #ordering = 'create_at'
    # 模型类名_list.html
    # template_name = 'users/user_detail.html'
    #def get_ordering(self):
        #pass

    #def get_paginate_by(self, queryset):
        #pass

    def get_queryset(self):
        # 筛选出所有的动态，再去显示
        return News.objects.filter(replay=False)
    # context = self.get_context_data() 返回额外的上下文，News，
    # 返回每条动态的浏览次数
    #def get_context_data(self, *, object_list=None, **kwargs):
        #context = super().get_context_data()
        #context['views'] = 100
        #return context

```

5. 发表动态

   news.js    ajax的post请求  /news/post-news/

   ajax中的data是news_form.modal.html中的postNewsForm   数据类型是 form_data

```python
views.py
#/news/post-news/ 处理这个请求
#还需要一个装饰器，用来实现ajax请求
@login_required
@ajax_required
@require_http_methods(['POST'])
def post_new(request):
    '''发表动态，Ajax 的POST请求'''
    post = request.POST['post'].strip()
    if post:
        posted = News.objects.create(user=request.user,content=post)
        # 将post内容和request请求渲染到模板中
        html = render_to_string('news/news_single.html',{'news':posted,'request':request})

        return HttpResponse(html)
    else:
        return HttpResponseBadRequest("内容不允许为空！！！")
```

​	装饰器helper.py

```python
from django.http import HttpResponseBadRequest
from functools import wraps
'''
    自定义装饰器，判断request是ajax请求
    request.is_ajax()
    闭包
'''
# functools wraps


def ajax_required(f):
    @wraps(f)
    def wrapTheFunction(request,*args,**kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("这不是Ajax请求")
        # 直接返回f，会影响原来的函数名称
        return f(request,*args,**kwargs)

    return wrapTheFunction

```

6. 设计路由

```python
#news下的urls
from django.urls import path
from itclub.users import views


app_name = "users"
urlpatterns = [
    path("update/", view=views.UserUpdateView.as_view(), name="update"),
    path("<str:username>/", view=views.UserDetailView.as_view(), name="detail"),
]
```

```python
#总的urls
path("news/", include("news.urls",namespace='news')),
```

7. 修改模板，把news下的模板中的delete_news删除，并把头像字段由picture改为avatar

8. 设计删除动态

```python
from django.urls import reverse,reverse_lazy

class NewsDeleteView(LoginRequiredMixin,AuthorRequireMixin,generic.DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    # 通过url传入要删除的对象主键id，默认值是slug
    # slug_url_kwarg = 'slug'
    # 通过 url传入要删除的对象主键id，默认值是pk
    # pk_url_kwarg = 'pk'
    # 在项目URLConf未加载前使用
    success_url = reverse_lazy('news:list')
```

```python
path('delete/<str:pk>',views.NewsDeleteView.as_view(),name='delete_news'),
```

```python
helpers.py
    
# 作者才有删除的权限  helper.py
'''
    验证是否是作者，用于删除动态，文章编辑
'''
from django.views.generic import View
from django.core.exceptions import PermissionDenied

class AuthorRequireMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request,*args,**kwargs)
```

9. 点赞的逻辑和实现

```python
'''
    局部刷新，用Ajax，更新点赞数
'''
from django.http import JsonResponse
@login_required
@ajax_required
@require_http_methods(['POST'])
def like_news(request):
    news_id = request.POST['news']
    news = News.objects.get(pk=news_id)
    news.switch_like(request.user)

    return JsonResponse({'likes':news.count_likers()})
```

```python
path('like-news/',views.like_news,name='like_news'),
```

10. 评论回复

```python
@login_required
@ajax_required
@require_http_methods(["GET"])
def get_thread(request):
    """返回动态的评论，AJAX GET请求"""
    news_id = request.GET['news']
    news = News.objects.select_related('user').get(pk=news_id)  # 不是.get(pk=news_id).select_related('user')
    # render_to_string()表示加载模板，填充数据，返回字符串
    news_html = render_to_string("news/news_single.html", {"news": news})  # 没有评论的时候
    thread_html = render_to_string("news/news_thread.html", {"thread": news.get_thread()})  # 有评论的时候
    return JsonResponse({
        "uuid": news_id,
        "news": news_html,
        "thread": thread_html,
    })


@login_required
@ajax_required
@require_http_methods(["POST"])
def post_comment(request):
    """评论，AJAX POST请求"""
    post = request.POST['reply'].strip()
    parent_id = request.POST['parent']
    parent = News.objects.get(pk=parent_id)
    if post:
        parent.reply_this(request.user, post)
        return JsonResponse({'comments': parent.comment_count()})
    else:  # 评论为空返回400.html
        return HttpResponseBadRequest("内容不能为空！")
```

```python
path('get-thread/',views.get_thread,name='get_thread'),
    path('post-comment/',views.post_comment,name='post_comment'),
```

11. 首页模型、视图测试、url测试

```python
#test_models.py
from test_plus import TestCase
from news.models import News


class NewsModels(TestCase):
    def setUp(self):
        self.user = self.make_user('user01')
        self.other_user = self.make_user('user02')
        self.first_news = News.objects.create(
            user=self.user,
            content='第一条动态'
        )
        self.second_news = News.objects.create(
            user=self.user,
            content='第二条动态'
        )
        self.third_news = News.objects.create(
            user=self.other_user,
            content='第一条动态的评论',
            replay=True,
            parent=self.first_news
        )

    def test_switch_like(self):
        self.first_news.switch_like(self.user)
        assert self.first_news.count_likers() == 1
        assert self.user in self.first_news.liked.all()

    def test_reply_this(self):
        self.first_news.reply_this(self.other_user,'对第一条动态的评论')
        assert self.third_news.comment_count != 0
        assert self.third_news in self.first_news.get_thread()

    def test__str__(self):
        self.assertEqual(self.first_news.__str__(),'第一条动态')

```

```python
# test_views.py
```

```python
# test_urls.py
from test_plus.test import TestCase
from django.urls import reverse,resolve


class TestNewsURLs(TestCase):
    def setUp(self):
        self.user = self.make_user()

    def test_list_reverse(self):
        self.assertEqual(reverse('news:list'), '/news/')

    def test_list_resolve(self):
        self.assertEqual(resolve('/news/').view_name, 'news:list')

    def test_post_news_reverse(self):
        self.assertEqual(reverse('news:post_news'), '/news/post-news/')

    def test_post_news_resolve(self):
        self.assertEqual(resolve('/news/post-news/').view_name, 'news:post_news')

    def test_like_news_reverse(self):
        self.assertEqual(reverse('news:like_news'), '/news/like-news/')

    def test_like_news_resolve(self):
        self.assertEqual(resolve('/news/like-news/').view_name, 'news:like_news')

    def test_get_thread_reverse(self):
        self.assertEqual(reverse('news:get_thread'), '/news/get-thread/')

    def test_get_thread_resolve(self):
        self.assertEqual(resolve('/news/get-thread/').view_name, 'news:get_thread')

    def test_post_comment_reverse(self):
        self.assertEqual(reverse('news:post_comment'), '/news/post-comment/')

    def test_post_comment_resolve(self):
        self.assertEqual(resolve('/news/post-comment/').view_name, 'news:post_comment')
```

12. 压力测试：测试各个接口的承压范围

    服务器配置：40G存储内存  2G运行内存

    承压的范围：

| 用户模块                 | 承压范围 |
| ------------------------ | -------- |
| /accounts/login/         | 280      |
| /accounts/signup/        | 275      |
| /accounts/confirm-email/ | 1380     |
| /users/update/           | 194      |
| /accounts/logout/        | 6        |

| 动态模块            | 承压范围 |
| ------------------- | -------- |
| /news/              | 203      |
| /news/post-news/    | 218      |
| /news/post-comment/ | 220      |
| /news/get-thread/   | 230      |

​	综合上述各接口的承压范围来看，服务器的承压范围大概为200



#### 十六、文章模块功能实现

1. 新建一个app，并将app移动到itclub下

```python
pipenv run python manage.py startapp article
```

2. Article模型的设计

```python
#models.py
from django.db import models
from django.conf import settings

# Create your models here.

class Article(models.Model):
    STATUS = (("D","Draft"),("P","Published"))

    title = models.CharField(max_length=255,unique=True,verbose_name="标题")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL,
                             related_name='author',verbose_name='作者')
    image = models.ImageField(upload_to='articles_pictures/%Y/%m/%d',verbose_name='文章图片')
    slug = models.SlugField(max_length=255,verbose_name='(URL)别名')
    status = models.CharField(max_length=1,choices=STATUS,default="D",verbose_name="文章状态")
    content = models.TextField(verbose_name="内容")
    edited = models.BooleanField(default=False,verbose_name="是否可编辑")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ("create_at",)

    def __str__(self):
        return self.title
```

3. 上述models有两个缺陷，一个是slug（不能每次都让作者生成别名URL），一个是tags（标签）

   解决方法：使用python-slugify  和  django-taggit

```python
# github地址： https://github.com/un33k/python-slugify
from slugify import slugify
txt = '影師嗎'
r = slugify(txt)
self.assertEqual(r, "ying-shi-ma")

# github地址：https://github.com/jazzband/django-taggit
from taggit.managers import TaggableManager
class Food(models.Model):
    # ... fields here
    tags = TaggableManager()
```

```python
#Article表中添加字段models.py

from slugify import slugify
from taggit.managers import TaggableManager

tags = TaggableManager(help_text="多个标签使用,（英文）隔开",verbose_name='标签')

def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.slug = slugify(self.title)
        #重载父类的方法
        super(Article,self).save()
```

4. 自定义queryset

```python
#写在Article表前面models.py
'''
    自定义一个queryset
'''
class ArticleQuerySet(models.query.QuerySet):
    def get_drafts(self):
        '''获取草稿箱'''
        return self.filter(status="D")
    
 #Article表中添加字段
objects = ArticleQuerySet.as_manager()
```

5. 注册到app中(config/settings/base.py/LOCAL_APPS)，然后迁移数据库

   ```python
   THIRD_PARTY_APPS = [
       "crispy_forms",
       "allauth",
       "allauth.account",
       "allauth.socialaccount",
       "allauth.socialaccount.providers.github",
       "django_celery_beat",
       "sorl.thumbnail",
       'taggit',
       'markdownx',
       'django_comments',
   ]
   ```

6. 设计views.py

```python
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from articles.models import Article
from articles.forms import ArticleForm
from itclub.helpers import AuthorRequireMixin


class ArticlesListView(LoginRequiredMixin, generic.ListView):
    '''文章列表'''
    model = Article
    paginate_by = 10
    context_object_name = 'articles'
    template_name = 'articles/article_list.html'


class ArticlesCreateView(LoginRequiredMixin, generic.CreateView):
    ''' 发表文章 '''
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_create.html'
    message = '发表成功'
    # initial = {'title':"草稿箱标题"}

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:list")

    # def get_initial(self):
    #     initial = super(ArticlesCreateView, self).get_initial()
    #
    #     return initial

    
class DraftListView(ArticlesListView):
    '''草稿'''
    def get_queryset(self):
        '''当前用户的草稿'''
        return Article.objects.filter(user=self.request.user).get_drafts()
    
    
class ArticleDetailView(LoginRequiredMixin,generic.DetailView):
    '''文章详情'''
    model = Article
    template_name = 'articles/article_detail.html'
    
    
class UpdateArticleView(LoginRequiredMixin,AuthorRequireMixin,generic.UpdateView):
    '''编辑文章'''
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article_update.html'
    message = '编辑成功'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse_lazy("articles:article",kwargs={"slug":self.get_object().slug})
```

7. 设计form表单验证

```python
#forms.py
from django import forms
from articles.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','content','image','tags']
```

8. 设计路由

```python
#articles下的urls
from django.urls import path
from articles import views

app_name = 'articles'

urlpatterns = [
    path('',views.ArticlesListView.as_view(),name='list'),
    path('write_new/',views.ArticlesCreateView.as_view(),name='write_new'),
    path('drafts/',views.DraftListView.as_view(),name='drafts'),
    path('<str:slug>/',views.ArticleDetailView.as_view(),name='article'),
    path('edit/<int:pk>/',views.UpdateArticleView.as_view(),name='edit_article'),
]

```

```python
#总的urls
path("articles/", include("articles.urls",namespace='articles')),
```



#### 十七、Django-markdownx(编辑文章内容)

​		Markdown是一种可以使用普通文本编辑器编写的标记语言，通过简单的标记语法，它可以使普通文本内容具有一定的格式。

​	https://neutronx.github.io/django-markdownx/

1. 安装

   ```
   pipenv install django-markdownx
   ```

2. 注册到第三方app

   ```python
   THIRD_PARTY_APPS = [
   #.....................
      'markdownx',
   ]
   ```

3. 注册路由

   ```python
   urlpatterns = [
       # [...]
       path('markdownx/', include('markdownx.urls')),
   ]
   ```

4. 用法models.py

   ```python
   #models.py
   
   from markdownx.models import MarkdownxField
   
   # content = models.TextField(verbose_name='内容')
       content = MarkdownxField(verbose_name='内容')
    
   
   #在前端使用，需要在models.py中导入
   from markdownx.utils import markdownify
   #给Article表添加方法
   #将markdown文本转换成html
    def get_markdown(self):
           return markdownify(self.content)
   ```
   
5. forms.py表单验证修改

   ```python
   from django import forms
   from articles.models import Article
   from markdownx.fields import MarkdownxFormField
   
   
   class ArticleForm(forms.ModelForm):
       content = myfield = MarkdownxFormField()
   
       class Meta:
           model = Article
           fields = ['title','content','imae','tags']
   ```

6. 同步数据库

7. 同步静态文件，将Markdown需要的css，js同步到static_root下

   ```
   pipenv run python manage.py collectstatic
   ```

8. 前端html表单中

   ```html
   <form method="POST" action="">{% csrf_token %}
       {{ form }}
   </form>
   
   {{ form.media }}
   ```

9. 更改编辑|预览模板

   ```python
   1. #DJANGO_APPS中注册
    DJANGO_APPS = ["django.forms"]
       
   2. #更改查找模板的顺序
    FROM_RENDERER = 'django.forms.renderers.TemplatesSetting'
       
   3. #修改模板名称
    templates/markdownx/widget.html
   ```



#### 十八、django-contrib-comments(文章评论)

​	https://django-contrib-comments.readthedocs.io/en/latest/quickstart.html

1. 安装

   ```
   pipenv install django-contrib-comments
   ```

2. 注册到第三方app

   ```python
   'django_comments'
   ```

3. 注册路由

   ```python
   path('comments/', include('django_comments.urls')),
   ```

4. 迁移数据库，并同步项目文件

#### 十九、问答模块

###### 一、数据库设计

1. 问题，用户，回答，投票这几个数据库怎么设计？

   问题和回答是一对多的关系，但是提问者接收答案只能接收一个。

2. 用户-问题-回答-点赞/踩-采纳    逻辑关系

   用户表：核心表

   问题表：has_answer  是否有唯一的答案

   回答表：is_answer    是不是唯一答案

   赞/踩表：value区分

3. 设计结果

   ```python
   import uuid
   
   from django.db import models
   from django.conf import settings
   
   from slugify import slugify
   from markdownx.models import MarkdownxField
   from taggit.managers import TaggableManager
   from markdownx.utils import markdownify
   
   '''
       自定义一个queryset
   '''
   class QuestionQuerySet(models.query.QuerySet):
       def get_answered(self):
           '''已经有答案的问题'''
           return self.filter(has_answer=True)
       def get_unanswered(self):
           '''未回答的问题'''
           return self.filter(has_answer=False)
       def get_counted_tags(self):
           '''统计所有的问题标签的数量'''
           pass
   
   
   # Create your models here.
   class Question(models.Model):
       STATUS = (("D","Draft"),("O","Open"),("C","Close"))
       user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,
                                related_name='q_author', verbose_name='提问者')
       title = models.CharField(max_length=255,unique=True,verbose_name="标题")
       slug = models.SlugField(max_length=255, verbose_name='(URL)别名')
       status = models.CharField(max_length=1, choices=STATUS, default="O", verbose_name="问题状态")
       content = MarkdownxField(verbose_name="内容")
       tags = TaggableManager(help_text="多个标签使用,（英文）隔开", verbose_name='标签')
       has_answer = models.BooleanField(default=False,verbose_name="接受回答") #表示是否有接受的回答
       create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
       update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
       # 自定义查询集
       objects = QuestionQuerySet.as_manager()
   
       class Meta:
           verbose_name = "问题"
           verbose_name_plural = verbose_name
           ordering = ("-create_at",)
       # 自动生成问题的slug
       def save(self,*args,**kwargs):
           if not self.slug:
               self.slug = slugify(self.title)
           super(Question, self).save(*args,**kwargs)
   
       def __str__(self):
           return self.title
   
   
   class Answer(models.Model):
       uuid_id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
       user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                related_name='a_author', verbose_name='回答者')
   
       question = models.ForeignKey(Question,on_delete=models.CASCADE(),verbose_name='问题')
       content = MarkdownxField(verbose_name='内容')
       is_answer = models.BooleanField(default=False,verbose_name='回答是否被接受')
       create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
       update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
   
       class Meta:
           verbose_name = "回答"
           verbose_name_plural = verbose_name
           ordering = ("-is_answer","-create_at",)
   
       def __str__(self):
           return self.content
   
       # 将Markdown文本转换成html
       def get_markdown(self):
           return markdownify(self.content)
   ```

###### 二、所有问题列表页

1. views.py

   ```python
   from django.urls import reverse_lazy
   from django.contrib import messages
   from django.http import JsonResponse
   from django.core.exceptions import PermissionDenied
   from django.contrib.auth.decorators import login_required
   from django.contrib.auth.mixins import LoginRequiredMixin
   from django.views.decorators.http import require_http_methods
   from django.views.generic import ListView,DetailView
   
   from bwitclub.helpers import ajax_required
   from bwitclub.qa.models import Question,Answer
   
   class QuestionListView(LoginRequiredMixin,ListView):
       model = Question
       paginate_by = 10
       context_object_name = "questions"
       template_name = "qa/question_list.html"
   
       def get_context_data(self, *, object_list=None, **kwargs):
           context = super(QuestionListView,self).get_context_data()
           context['popular_tags'] = Question.objects.get_counted_tags()
           context['active'] = "all"
           return context
   
   
   class QuestionDetailView(LoginRequiredMixin,DetailView):
       pass
   ```

2. urls.py

   ```python
   from django.urls import path
   
   from bwitclub.qa import views
   
   app_name = 'qa'
   
   urlpatterns = [
       path('indexed/',views.QuestionListView.as_view(),name='all_q'),
   ]
   ```

###### 三、已回答&待回答问题页

1. views.py

   ```python
   # 已回答，已经采纳答案的问题
   class AnsweredQuestionListView(QuestionListView):
       def get_queryset(self):
           '''当前用户的草稿'''
           return Question.objects.get_answered()
   
       def get_context_data(self, *, object_list=None, **kwargs):
           context = super(AnsweredQuestionListView,self).get_context_data()
           context['active'] = "answered"
           return context
   
   # 待回答的问题
   class UnAnsweredQuestionListView(QuestionListView):
       def get_queryset(self):
           '''当前用户的草稿'''
           return Question.objects.get_unanswered()
   
       def get_context_data(self, *, object_list=None, **kwargs):
           context = super(UnAnsweredQuestionListView,self).get_context_data()
           context['active'] = "unanswered"
           return context
   ```

   

2. urls.py

   ```python
   from django.urls import path
   
   from bwitclub.qa import views
   
   app_name = 'qa'
   
   urlpatterns = [
       path('',views.UnAnsweredQuestionListView.as_view(),name='unanswered_q'),
       path('answered/',views.AnsweredQuestionListView.as_view(),name='answered_q'),
       path('indexed/',views.QuestionListView.as_view(),name='all_q'),
   ]
   ```

###### 四、用户提问

1. views.py

   ```python
   # 用户提问
   class CreateQuestionView(LoginRequiredMixin,CreateView):
       model = Question
       form_class = QuestionForm
       template_name = 'qa/question_form.html'
       messages = "问题已提交"
   
       def form_valid(self, form):
           form.instance.user = self.request.user
           return super().form_valid(form)
   
       def get_success_url(self):
           messages.success(self.request,self.messages)
           return reverse_lazy("qa:unanswered_q")
   ```

2. forms.py

   ```python
   from django import forms
   from markdownx.fields import MarkdownxFormField
   from qa.models import Question
   
   
   class QuestionForm(forms.ModelForm):
       status = forms.CharField(widget=forms.HiddenInput())
       content = MarkdownxFormField()
   
       class Meta:
           model = Question
           fields = ['title','content','status','tags']
   
   ```

3. urls.py

   ```python
   path('ask_question/',views.CreateQuestionView.as_view(),name='ask_question'),
   ```

###### 五、问题详情页

1. views.py

   ```python
   # 问题详情页
   class QuestionDetailView(LoginRequiredMixin,DetailView):
       model = Question
       context_object_name = 'question'
       template_name = 'qa/question_detail.html'
   ```

2. urls.py

   ```python
   path('question_detail/<int:pk>/',views.QuestionDetailView.as_view(),name='question_detail'),
   ```

###### 六、回答问题

1. views.py

   ```python
   # 用户回答
   class CreateAnswerView(LoginRequiredMixin,CreateView):
       model = Answer
       fields = ['content']
       template_name = 'qa/answer_form.html'
       messages = "回答已提交"
   
       def form_valid(self, form):
           form.instance.user = self.request.user
           form.instance.question_id = self.kwargs['question_id']
           return super(CreateAnswerView,self).form_valid(form)
   
       def get_success_url(self):
           messages.success(self.request,self.messages)
           return reverse_lazy("qa:question_detail",kwargs=
           {"pk":self.kwargs['question_id']})
   ```

2. urls.py

   ```python
   path('propose_answer/<int:question_id>/',views.CreateAnswerView.as_view(),name='propose_answer'),
   ```

###### 七、点赞/踩/采纳答案

1. models.py

   ```python
   from django.db import models
   import uuid
   from collections import Counter
   from django.contrib.contenttypes.models import ContentType
   from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
   from users.models import User
   from slugify import slugify
   from taggit.managers import TaggableManager
   from markdownx.models import MarkdownxField
   from markdownx.utils import markdownify
   
   
   class Vote(models.Model):
       uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                related_name='qa_vote', verbose_name='点赞人')
       value = models.BooleanField(default=True, verbose_name='赞还是踩')
       content_type = models.ForeignKey(ContentType, related_name='votes_on', on_delete=models.CASCADE)
       object_id = models.CharField(max_length=255)
       vote = GenericForeignKey('content_type', 'object_id')
       create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
       update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
   
       class Meta:
           verbose_name = '投票'
           verbose_name_plural = verbose_name
           unique_together = ('user', 'content_type', 'object_id')  # 联合唯一
           # SQL优化
           index_together = ('content_type', 'object_id')  # 联合唯一索引
   
   
   class QuestionQuerySet(models.query.QuerySet):
       def get_answered(self):
           """
               未答
           """
           return self.filter(has_answer=True)
   
       def get_unanswered(self):
           """
               以答
           """
           return self.filter(has_answer=False)
   
       def get_counted_tags(self):
           # return self.all().count()
           pass
   
       # def get_counted_tags(self):
       #     '''统计所有问题标签的数量'''
       #     tag_dict = {}
       #     query = self.all().annotate(tagged=Count('tags')).filter(tags__gt=0)
       #     for obj in query:
       #         for tag in obj.tags.names():
       #             if tag not in tag_dict:
       #                 tag_dict[tag] = 1
       #             else:
       #                 tag_dict[tag] += 1
       #     return tag_dict.items()
   
   
   class Question(models.Model):
       STATUS = (
           ('D', 'Draft'),
           ('O', 'Open'),
           ('C', 'close')
       )
       title = models.CharField(max_length=255, unique=True, verbose_name='标题')
       user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,
                                related_name='q_author', verbose_name='提问人')
       slug = models.SlugField(max_length=255, verbose_name='(URL)别名')
       status = models.CharField(max_length=1, choices=STATUS, default='O', verbose_name='问题状态')
       # content = models.TextField(verbose_name='内容')
       content = MarkdownxField(verbose_name='内容')
       tags = TaggableManager(help_text='多个标签 , 隔开', verbose_name='标签')
       has_answer = models.BooleanField(default=False, verbose_name='接受回答')
       votes = GenericRelation(Vote, verbose_name='投票情况')
       create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
       update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
       objects = QuestionQuerySet.as_manager()
   
       class Meta:
           verbose_name = '问题'
           verbose_name_plural = verbose_name
           ordering = ('-create_at', )
   
       def __str__(self):
           return self.title
   
       def save(self, force_insert=False, force_update=False, using=None,
                update_fields=None):
           self.slug = slugify(self.title)
           # 重载父类的方法
           super(Question, self).save()
   
       # 将markdown文本转html
       def get_markdown(self):
           return markdownify(self.content)
   
       def total_votes(self):
           """得票数"""
           dic = Counter(self.votes.values_list('value', flat=True))
           return dic[True] - dic[False]
   
       def get_answer(self):
           return Answer.objects.filter(question=self)
   
       def count_answer(self):
           """所有回答数量"""
           return Answer.objects.filter(question=self).count()
   
       def get_upvoters(self):
           """赞同"""
           return [vote.user for vote in self.votes.filter(value=True)]
   
       def get_downvoters(self):
           """反对"""
           return [vote.user for vote in self.votes.filter(value=False)]
   
       def get_accepted_answer(self):
           """采纳"""
           return Answer.objects.get(question=self, is_answer=True)
   
   
   class Answer(models.Model):
       uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
       user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name='a_author', verbose_name='回答人')
       question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='问题')
       content = MarkdownxField(verbose_name='内容')
       is_answer = models.BooleanField(default=False, verbose_name='是否被接受')
       votes = GenericRelation(Vote, verbose_name='投票情况')  # 不是实际字段
       create_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
       update_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
   
       class Meta:
           verbose_name = '回答'
           verbose_name_plural = verbose_name
           ordering = ('-is_answer', '-create_at')
   
       def __str__(self):
           return self.content
   
       def get_markdown(self):
           return markdownify(self.content)
   
       def total_votes(self):
           """得票数"""
           dic = Counter(self.votes.values_list('value', flat=True))
           return dic[True] - dic[False]
   
       def get_upvoters(self):
           """赞同"""
           return [vote.user for vote in self.votes.filter(value=True)]
   
       def get_downvoters(self):
           """反对"""
           return [vote.user for vote in self.votes.filter(value=False)]
   
       def accept_answer(self):
           """接受回答"""
           answer_set = Answer.objects.filter(question=self.question)
           answer_set.update(is_answer=False)  # 其他一律未接受
           self.is_answer = True
           self.save()
           # 设置该问题以为接受回答
           self.question.has_answer = True
           self.question.save()
   
   
   ```

2. views.py

   ```python
   @login_required
   @ajax_required
   @require_http_methods(['POST'])
   def question_vote(request):
       """
           给问题投票
       """
       question_id = request.POST.get('question')
       if request.POST.get('value') == 'U':
           value = True
       else:
           value = False
   
       question = Question.objects.get(pk=question_id)
       users = question.votes.values_list('user', flat=True)
   
       # 已经赞过或踩过
       if request.user.pk in users and (question.votes.get(user=request.user).value == value):
           question.votes.get(user=request.user).delete()
       #
       else:
           question.votes.update_or_create(user=request.user, defaults={'value': value})
   
       return JsonResponse({
           "votes": question.total_votes()
       })
       # # 1.用户首次操作
       # if request.user.pk not in users:
       #     question.votes.update_or_create(user=request.user, defaults={'value': value})
       #
       # # 2.用户已经赞过取消赞
       # elif question.votes.get(user=request.user).value:
       #     if value:
       #         question.votes.get(user=request.user).delete()
       #     else:
       #         question.votes.update_or_create(user=request.user, defaults={'value': value})
       #
       # else:
       #     if not value:
       #         question.votes.get(user=request.user).delete()
       #     else:
       #         question.votes.update_or_create(user=request.user, defaults={'value': value})
       #
       # # 用户是否赞过或踩过
   
   
   @login_required
   @ajax_required
   @require_http_methods(['POST'])
   def answer_vote(request):
       """
           给问题投票
       """
       answer_id = request.POST.get('answer')
       if request.POST.get('value') == 'U':
           value = True
       else:
           value = False
   
       answer = Answer.objects.get(uuid_id=answer_id)
       users = answer.votes.values_list('user', flat=True)
   
       # 已经赞过或踩过
       if request.user.pk in users and (answer.votes.get(user=request.user).value == value):
           answer.votes.get(user=request.user).delete()
       else:
           answer.votes.update_or_create(user=request.user, defaults={'value': value})
   
       return JsonResponse({
           "votes": answer.total_votes()
       })
   
   
   @login_required
   @ajax_required
   @require_http_methods(['POST'])
   def accept_answer(request):
       '''接受回答'''
       answer_id = request.POST['answer']
       answer = Answer.objects.get(pk=answer_id)
       #用户登录
       if answer.question.user.username != request.user.username:
           raise PermissionDenied
       answer.accept_answer()
       return JsonResponse({'status':'true'})
   ```

3. urls.py

   ```python
   path('question/vote/',views.question_vote,name='question_vote'),
       path('answer/vote/',views.answer_vote,name='answer_vote'),
    path('accept/answer/',views.accept_answer,name='accept_answer'),
   ```
   
   

















































































注：

​	reverse用于FBV

​	reverse_lazy用于CBV