from m.extensions.sqlalchemy import SQLAlchemy
from sqlalchemy import Column, INTEGER, String, ForeignKey, UniqueConstraint, DateTime, Text
from sqlalchemy.orm import relationship

db = SQLAlchemy(config_prefix='database')


class User(db.Model):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    nickname = Column(String(45), unique=True, nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    password = Column(String(64), nullable=False)

    catalogs = relationship('Catalog', foreign_keys='[Catalog.user]')


class Catalog(db.Model):
    __tablename__ = 'catalog'
    __table_args__ = (UniqueConstraint('user', 'name', name='uq_catalog_user_name'),)

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    name = Column(String(45), nullable=False)

class Post(db.Model):
    __tablename__ = 'post'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String(192), nullable=False, default='Sky')
    author = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    catalog = Column(INTEGER, ForeignKey('catalog.id'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    status = Column(INTEGER, nullable=False, default=0)
    read_count = Column(INTEGER, nullable=False, default=0)
    image = Column(String(192), nullable=True)

    author2 = relationship('User', foreign_keys=[author])
    catalog2 = relationship('Catalog', foreign_keys=[catalog])
    content = relationship('PostContent', foreign_keys='[PostContent.id]', uselist=False)


class PostContent(db.Model):
    __tablename__ = 'post_content'

    id = Column(INTEGER, ForeignKey('post.id'), primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)


class Favorite(db.Model):
    __tablename__ = 'favorite'

    user_id = Column(INTEGER, ForeignKey('user.id'), primary_key=True)
    post_id = Column(INTEGER, ForeignKey('post.id'), primary_key=True)


class Like(db.Model):
    __tablename__ = 'like'

    user_id = Column(INTEGER, ForeignKey('user.id'), primary_key=True)
    post_id = Column(INTEGER, ForeignKey('post.id'), primary_key=True)


class Comment(db.Model):
    __tablename__ = 'comment'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    user = Column(INTEGER, ForeignKey('user.id'), nullable=False)
    post = Column(INTEGER, ForeignKey('post.id'), nullable=False)
    content = Column(String(420), nullable=False)
    ref = Column(INTEGER, ForeignKey('comment.id'), nullable=True)
    timestamp = Column(DateTime, index=True, nullable=False)

    user2 = relationship('User', foreign_keys=[user])
    ref2 = relationship('Comment', foreign_keys=[ref], uselist=True)



