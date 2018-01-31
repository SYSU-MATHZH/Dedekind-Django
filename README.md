### 项目说明(model_v2)

这是一个开发中的用于中珠数院公益时管理的Django Web App，代号：Project Dedekind

你现在所在的分支是model_v2，这是重新设计过models的Dedekind版本。

### 项目进展(model_v2)

- [1] models重新设计
- [1] 编写每一个model的基本serializers(用于测试及list API)
- [1] 编写list API View(通过ReadOnlyModelViewSet)
- [1] 编写AddFormMixin #18
- [ ] 编写ChangeFormMixin #19
- [ ] 编写DetailMixin #20
- [ ] 编写每一个model的add html View #13 #14 #15 #16 #17
- [ ] 编写每一个model的change html View
- [ ] 编写每一个model的detail html View
- [ ] 编写学生端主页的index html View
- [ ] 编写管理端主页的admin html View
- [ ] 编写权限管理部分代码...
- [ ] 制作相应网页模板...


### 本地部署(model_v2暂不可用)

1. 安装virtualenv
2. clone仓库，用virtualenv创建虚拟环境venv，并激活venv

```bash
cd Dedekind-Django
virtualenv venv
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -Ur requirements/local.txt
```

4. 添加token.py

```bash
touch project/sua/token.py
echo "TOKEN = 'YourTokenHere'" > project/sua/token.py
```

5. 初始化数据库，并创建超级用户

```bash
python manage.py makemigrations sua
python manage.py migrate
python manage.py createsuperuser
```

6. 启动服务器

```bash
python manage.py runserver
```

7. 用浏览器打开[http://localhost:8000/](http://localhost:8000/)
（由于后端代码还不完善，启动服务器后应通过[http://localhost:8000/super/admin](http://localhost/super/admin:8000/)及时添加两个SuaGroup：“个人用户”及“学院”）
