# 🐘 SQLAlchemy + PostgreSQL + Alembic Setup Guide
Easily connect your Python project to a **PostgreSQL** database using **SQLAlchemy** as the ORM and **Alembic** for migrations.  
This guide walks you through the full setup — from database connection to creating and applying migrations.

---

## 📚 SQLAlchemy Core Concepts

### What is SQLAlchemy?
SQLAlchemy is a Python SQL toolkit and Object-Relational Mapping (ORM) library that provides:
- **SQL Expression Language**: Write SQL queries using Python objects
- **ORM**: Map Python classes to database tables
- **Connection Pooling**: Efficient database connection management
- **Database Agnostic**: Works with PostgreSQL, MySQL, SQLite, and more

### Two Layers of SQLAlchemy

#### 1. **SQLAlchemy Core** (Low-level)
- Direct SQL expression construction
- More control, closer to raw SQL
- Better for complex queries and performance-critical operations

#### 2. **SQLAlchemy ORM** (High-level)
- Work with Python objects instead of SQL
- Automatic query generation
- Relationship management
- Better for rapid development and maintainability

---

## 🏗️ ORM Architecture

### The Session
The **Session** is the primary interface for database operations:
- Acts as a "holding zone" for objects
- Tracks changes to objects (dirty tracking)
- Manages transactions (commit/rollback)
- **Not thread-safe** — create new sessions per request/thread
```python
from sqlalchemy.orm import Session

# Create a session
session = Session(engine)

# Use it
user = session.query(User).filter_by(name="John").first()
session.commit()
session.close()
```

### The Engine
The **Engine** manages database connections:
- Connection pooling
- Dialect-specific SQL generation
- Created once per application
```python
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost/dbname")
```

### Models (Declarative Base)
Models are Python classes that map to database tables:
```python
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True)
```

---

## 🔗 Relationships in SQLAlchemy

### One-to-Many
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
```

### Many-to-Many
```python
# Association table
user_group = Table('user_group', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('group_id', ForeignKey('groups.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    groups = relationship("Group", secondary=user_group, back_populates="users")

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    users = relationship("User", secondary=user_group, back_populates="groups")
```

---

## 🔄 Session Lifecycle & State Management

Objects in SQLAlchemy have different states:

1. **Transient**: New object, not in session
2. **Pending**: Added to session but not saved to DB
3. **Persistent**: In session and saved to DB
4. **Detached**: Was in session but is now removed
```python
# Transient
user = User(name="Alice")

# Pending
session.add(user)

# Persistent
session.commit()

# Detached
session.close()
```

---

## ⚡ Query Patterns

### Basic Queries
```python
# Get all
users = session.query(User).all()

# Filter
user = session.query(User).filter_by(name="John").first()
user = session.query(User).filter(User.age > 18).all()

# Order
users = session.query(User).order_by(User.name).all()

# Limit
users = session.query(User).limit(10).all()
```

### Joins
```python
# Implicit join via relationship
posts = session.query(Post).join(User).filter(User.name == "John").all()

# Explicit join
from sqlalchemy import select
stmt = select(User, Post).join(Post, User.id == Post.user_id)
```

### Aggregations
```python
from sqlalchemy import func

# Count
count = session.query(func.count(User.id)).scalar()

# Group by
results = session.query(User.city, func.count(User.id))\
    .group_by(User.city).all()
```

---

## 🚀 1. Install Required Packages
```bash
# ORM and PostgreSQL driver
pip install sqlalchemy psycopg2

# Database migration tool
pip install alembic
```

---

## 💡 Best Practices

### ✅ Do's
- Use `sessionmaker` for session creation
- Always close sessions (or use context managers)
- Use relationship `lazy` loading strategies wisely
- Leverage connection pooling
- Use Alembic for all schema changes

### ❌ Don'ts
- Don't share sessions across threads
- Avoid creating engines repeatedly
- Don't use ORM for bulk operations (use Core instead)
- Don't forget to commit transactions
- Avoid N+1 query problems (use `joinedload` or `selectinload`)

---

## 🔍 Common Gotchas

**N+1 Query Problem**
```python
# Bad - triggers one query per user
for user in session.query(User).all():
    print(user.posts)  # Separate query for each user!

# Good - loads everything in 2 queries
from sqlalchemy.orm import joinedload
users = session.query(User).options(joinedload(User.posts)).all()
```

**Session Scope**
```python
# Bad - session outlives request
session = Session(engine)

# Good - new session per request
from contextlib import contextmanager

@contextmanager
def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
```

---
