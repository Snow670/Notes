# Git分支管理

## 一、内容回顾

创建、合并分支

解决合并冲突（手动解决）

非Fast forward模式合并分支

实际开发中的分支管理



## 二、Bug分支与Feature分支

#### Bug分支

情景：当你在dev分支上正在开发项目，此时你的文件名为newdev.txt，突然有任务需要你改bug，（假设bug位于master分支上的sss.txt文件中），你需要先改完bug，再完成你的开发。

步骤：

```
1.首先切换到dev分支       git checkout dev
2.把你正在写的文件newdev.txt添加到dev分支上   git add newdev.txt
3.查看当前分支状态        git status
4.储存当前分支状态        git stash
5.创建解决bug的分支       git checkout -b issue-100
6.修改sss.txt文件
7.提交修改的文件          git add sss.txt  git commit -m "bug 100"
8.返回到master分支        git checkout master
9.合并bug分支             git merge --no-ff -m "合并Bug 100" issue-100
10.推送到远程master分支   git push origin master
11.返回你的dev分支        git checkout dev
12.恢复你之前正在写的状态   git stash pop
13.可以使用git stash list查看有多少个stash,然后恢复指定的stash
14.此时还没有修复dev上的bug,在dev分支上执行命令git cherry-pick 2e5c4cc,把修复的bug复制到dev分支上
15.执行完毕后，要删除bug分支   git branch -D issue-100
```

#### Feature分支

软件开发过程中，总会有一些新需求需要添加进来。这时候，为了不把master分支搞乱了，每添加一个新功能，最好新建一个feature分支，在feature分支上开发，完成后合并，最后删除feature分支

```
1. git switch -c feature-faceID

2. touch face.py

3. git add face.py

4. git status

5. git commit -m '添加了人脸识别的功能'

6. git switch dev

   但是，此时公司管理层觉得人脸识别这个功能太耗费钱了，还是取消吧，虽然白干了，但是没办法，只能删掉这个分支

   git branch -d feature-faceID

   又报错了：error: The branch 'feature-faceID' is not fully merged. If you are sure you want to delete it, run 'git branch -D feature-faceID'. 表示销毁失败

   执行 git branch -D feature-faceID，强制删除

7. git merge --no-ff -m '合并新功能分支' feature-faceID

8. git branch -d feature-faceID 删除分支


```



## 三、多人协作



1. 远程仓库的信息怎么看？远程仓库名字是什么？

   当你git clone，实际是Git自动把本地的master分支和远程master分支对应起来，并且，远程仓库名称默认是origin

   git remote 查看远程仓库的信息

   git remote -v 显示更详细的信息

2. 推送分支

   就是把该分支上所有本地提交推送到远程库 ，推送的时候指定本地分支，这样的话Git就会把该分支推送的远程库对应的远程分支上

   git push origin（远程库名称） master(本地的master分支)

   git push origin dev

   但是并不是一定要把所有的本地分支往远程推送，哪些需要推送，哪些不需要推送呢？

   master 分支是主分支，因此要时刻与远程同步

   dev分支是开发分支，团队所有成员都需要在上面工作，所以也需要与远程同步

   bug分支用来在本地修复bug的，所以没有必要推送到远程，除非老板或者组长需要看看你每周到底修复了几个bug

   feature分支取决于你是否和其他人进行合作

3. 抓取分支

   git clone git@github.com:ITClubOfBruce/Python-lesson-plan.git

   当你从远程仓库clone时候，默认你只能看到master分支

```
C:\Users\Bruce\Desktop\newfolder\Python-lesson-plan (master -> origin)
   $ git branch
   * master
```

​	想要在dev分支上进行开发，必须创建远程origin的dev分支到本地

```
git checkout -b dev origin/dev

git add  new.txt

git commit -m '添加新文件'

git push origin dev
```

但是，此时另一个同学也对new.txt文件进行了修改，并且也正要推送，执行上面的操作会报错，原因是你的提交和这个同学的提交有冲突，解决办法：

```
git pull 把最新的提交从origin/dev抓下来，然后，在本地合并，解决冲突，然后再推送

git pull也可能会失败。原因是没有指定本地dev分支与远程origin/dev分支的链接，这个时候，需要设置dev和远程origin/dev分支的链接：git branch --set-upstream-to=origin/dev dev

再次git pull，就成功了。
```

总结：

1. 首先，使用git push origin 你自己的分支名称 推送自己的修改
2. 如果推送失败，则因为远程分支比你的本地分支上的代码更新，需要先使用git pull 试图合并一下
3. 如果合并有冲突，这解决冲突，并在本地提交commit
4. 如果没有冲突或者解决完冲突，再用git push origin 你的分支名称 推送就能成功了
5. 如果git pull 提示 no tracking information，说明本地分支和远程分支的链接关系还没有创建，用git branch --set-upstream-to=origin/dev dev 创建

## git pull



git pull用法：
git pull命令的作用是：取回远程主机某个分支的更新，再与本地的指定分支合并。

一句话总结git pull和git fetch的区别：git pull = git fetch + git merge

git fetch不会进行合并执行后需要手动执行git merge合并分支，而git pull拉取远程分之后直接与本地分支进行合并。更准确地说，git pull使用给定的参数运行git fetch，并调用git merge将检索到的分支头合并到当前分支中。

基本用法：

git pull <远程主机名> <远程分支名>:<本地分支名>

例如执行下面语句：

git pull origin master:brantest

将远程主机origin的master分支拉取过来，与本地的brantest分支合并。



上面的pull操作用fetch表示为：

git fetch origin master:brantest 

git merge brantest 

相比起来git fetch更安全一些，因为在merge前，我们可以查看更新情况，然后再决定是否合并。









