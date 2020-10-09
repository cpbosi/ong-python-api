# Python3 ONG API for dummies

This is a simple CRUD API developed while i studied Python3 with Flask (micro web framework), SQLAlchemy, marshmallow using the sqlite3.

## Usage

### Setup Database
Create de database using the commands on the shell

```bash
python3

from app import db
db.create_all()
```

If everything works fine a file named 'db.sqlite3' will be created at your project folder this file will be use to keep the data.

After this execute the file app.py

```bash
python3 app.py
```

Open the URL http://localhost:5000/ in the browser.

## References

The first commit was created using the knowledge of many tutorials (this part i was confortable to write) but the use of SQLAlchemy and marshmallow was using this [tutorial](https://dev.to/nahidsaikat/flask-with-sqlalchemy-marshmallow-5aj2)


## License
[MIT](https://choosealicense.com/licenses/mit/)