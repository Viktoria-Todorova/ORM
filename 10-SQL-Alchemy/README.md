pip install sqlalchemy

pip install psycopg2

**in modules**

from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base

**main.py**

DATABASE_URL =
'postgresql+psycopg2://your_username:your_password@your_host
/your_database'
engine = create_engine(DATABASE_URL)

**Alemic**

pip install alembic
alembic init alembic

**alembic.ini**

sqlalchemy.url =
postgresql+psycopg2://username:password@localhost/db_name

**Create a Migration**

alembic revision --autogenerate -m "Add User Table"

**▪ Apply Migrations**

alembic upgrade head

**▪ Downgrade (Rollback) Migrations**
alembic downgrade -1

