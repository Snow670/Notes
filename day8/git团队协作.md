## 一、环境初始化
1. github上新建仓库，然后使用git clone 下来
2. 有更新的话：git remote update origin --prune
3. cd 1903C-Bruce下，使用ls -al。看到有.git文件，说明本地仓库已经初始化

## 二、git开发原则
开发分支开发 dev

测试分支测试  test

master分支   master

新建分支  git checkout -b dev

git branch -r   查看远程分支 -吧

git branch       查看本地分支

git branch -a   查看所有分支

## 三、新建分支并创建项目

1.git checkout -b dev

2.vim aa.txt

3.git add .

4.git commit -m "aaa"

5.git push origin dev

## 四、合并分支

1. 先从dev分支把最新的代码拉下来

   git pull origin dev

2. 切换到主分支

   git checkout master

3. 将dev分支的代码合并到主分支

   git merge origin/dev

4. 将代码推送到主分支

   git push origin master


## 五、test分支练习

1. 切换到test分支

   git checkout test

2. 新建test.txt文件

   刚新建完的文件，没做任何提交，在所有分支上是都能看到的

   

## 删除

1. 删除已经上传到远程分支的文件

   git rm test.txt

   git commit -m '删除dev上的test.txt'

   git push origin dev

2.要删除服务器远端的分支，则执行如下所示的命令：

​	git push origin --delete 分支名

3.如果是要删除本地已经合并了的分支，则执行：

​	git branch -d 分支名

4.删除本地未合并的分支：

 	git branch -D 分支名

## 解决合并冲突

##### 1.切换分支  (2种方式)

​	1.1git checkout dev

​	1.2.test分支不存在的情况下：git  switch -c test

​     		test分支存在的情况下:git  switch  test

2.在test分支下创建readmw.md文件，并写入内容

3.在test分支上提交readmw.md

​			git  add  readmw.md

​			git commit -m "test分支的readme"

4.切换回master分支       git  switch  master

​	在master分支下创建readmw.md文件，并写入内容

5.在master分支上提交readmw.md

​			git  add  readmw.md

​			git commit -m "master分支的readme"

6.这个时候master分支和test分支都有readme.md，这个时候无法进行“快速合并”，必须手动解决冲突后再提交

7.master分支上执行 git merge test 

```
$ git merge test
CONFLICT (add/add): Merge conflict in readme.md
Auto-merging readme.md
Automatic merge failed; fix conflicts and then commit the result.
```

![image-20200721143017274](C:\Users\Dell\AppData\Roaming\Typora\typora-user-images\image-20200721143017274.png)

 8.选择‘采用传入的更改’，手动更新文档后，再次提交和推送到远程仓库就可以了

​	  git add as.txt

 	git commit -m "最终的as"

 	git push origin master

 9.使用git log --graph查看分支的合并情况

10.删除test分支   git branch -d test

## 非Fast forward模式

1.git默认情况下使用的是Fast forward模式，Fast forward模式下，删除分支后，会丢掉分支的信息，我们可以使用非Fast forward模式，也就是禁用Fast forward模式，这样Git在每次merge

2.切换到test分支上，修改readme.md,再次提交

​	git add readme.md

​	git commit -m "添加分支非Fast forward模式"

3.切换到master分支上	git switch master

4.合并	git merge --no-ff -m "使用非Fast forward合并" test

5..选择‘采用传入的更改’，再次提交和推送到远程仓库就可以了

​	  git add  readme.md

 	git commit -m "最终的as"

 	git push origin master

## Git分支策略

1. master分支是非常稳定的分支，仅仅用来发布新版本，平时的不能再这个分支上开发
2. 要在dev分支上进行开发工作，dev分支是不稳定的分支，比方说：第一个迭代版本 V1.0发布的时候，再把dev分支合并到master分支上，在master分支上发布V1.0
3. 多人都在dev分支上开发，每个人都有自己的分支，平时经常的往dev分支上合并就可以