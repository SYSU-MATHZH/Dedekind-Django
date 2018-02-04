### 项目说明

这是一个开发中的用于中珠数院公益时管理的Django Web App，代号：Project Dedekind


### 项目进展

- 基本完成学生端，正在进行代码整理
- 基本完成管理端后端，正在开发前端及整理后端代码

### 本地部署

1. 安装virtualenv
2. clone仓库，用virtualenv创建虚拟环境venv35，并激活venv35

```bash
cd Dedekind-Django
virtualenv venv35 --python=python3.5
source venv35/bin/activate
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
