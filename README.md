# ✋ 5-letters-solver
## Flask application for solving game 5-letters

How to run development server:

1. Create virtual environment:
```
$ python3 -m venv ./venv:
```

2. Activate it:
```
$ source /venv/bin/activate
```

3. Setting the FLASK_APP environment variable:
```
(venv) $ export FLASK_APP=five_letters.py
```

4. Create DB and User:
```
(venv) $ flask shell
>>> user = User(username='Carlos', email='useremail@example.com')
>>> user.set_password('password')
>>> db.session.add(user)
>>> db.session.commit()
>>> exit()
```

5. Start development server at localhost:
```
(venv) $ flask run
```

6. Open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) at your browser.