from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql.expression import desc
from api import db
from .seeders import Permissions, Roles


class TimestampMixin:
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    # TODO
    # add default value to updated_at
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Follow(db.Model):
    followed_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True
    )
    follower_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), primary_key=True
    )
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class User(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False
    )
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    location = db.Column(db.String(64))
    about = db.Column(db.Text())
    avatar = db.Column(db.Text())
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)
    role = db.relationship("Role", lazy=True, back_populates="users")
    posts = db.relationship(
        "Post",
        lazy=True,
        back_populates="author",
        order_by=lambda: desc(Post.created_at),
        cascade="all, delete-orphan",
    )
    comments = db.relationship(
        "Comment",
        lazy=True,
        back_populates="author",
        cascade="all, delete-orphan",
    )
    _following = db.relationship(
        "Follow",
        foreign_keys=[Follow.follower_id],
        lazy=True,
        backref=db.backref("follower", lazy="joined"),
        cascade="all, delete-orphan",
    )
    _followers = db.relationship(
        "Follow",
        foreign_keys=[Follow.followed_id],
        lazy=True,
        backref=db.backref("followed", lazy="joined"),
        cascade="all, delete-orphan",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.role_id:
            self.role = Role.query.filter_by(name=Roles.USER.value).first()

    @property
    def password(self):
        raise AttributeError("'password' is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role.can(Permissions.ADMIN.value)

    def is_following(self, user):
        result = Follow.query.filter_by(
            follower_id=self.id, followed_id=user.id
        ).first()
        return result is not None

    def is_followed_by(self, user):
        result = Follow.query.filter_by(
            followed_id=self.id, follower_id=user.id
        ).first()
        return result is not None

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            f = Follow.query.filter_by(
                follower_id=self.id, followed_id=user.id
            ).first()
            db.session.delete(f)
            db.session.commit()

    @property
    def followers_count(self):
        return Follow.query.filter_by(followed_id=self.id).count()

    @property
    def following_count(self):
        return Follow.query.filter_by(follower_id=self.id).count()

    @property
    def followers(self):
        return (
            User.query.join(
                Follow,
                User.id == Follow.follower_id,
            )
            .filter(self.id == Follow.followed_id)
            .all()
        )

    @property
    def following(self):
        return (
            User.query.join(
                Follow,
                User.id == Follow.followed_id,
            )
            .filter(self.id == Follow.follower_id)
            .all()
        )


# association table
role_permission = db.Table(
    "role_permission",
    db.Column(
        "role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True
    ),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permission.id"),
        primary_key=True,
    ),
)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship("User", lazy=True, back_populates="role")
    permissions = db.relationship(
        "Permission",
        secondary=role_permission,
        lazy="joined",
        back_populates="roles",
    )

    def can(self, permission):
        result = (
            Permission.query.with_parent(self)
            .filter_by(name=permission)
            .first()
        )
        return result is not None


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    roles = db.relationship(
        "Role",
        secondary=role_permission,
        lazy=True,
        back_populates="permissions",
    )


class Post(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", lazy="joined", back_populates="posts")
    comments = db.relationship(
        "Comment",
        lazy=True,
        back_populates="post",
        cascade="all, delete-orphan",
    )

    def is_author(self, user):
        return user is self.author


class Comment(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    disabled = db.Column(db.Boolean, default=False, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    post = db.relationship("Post", lazy=True, back_populates="comments")
    author = db.relationship("User", lazy=True, back_populates="comments")

    def is_author(self, user):
        return user is self.author
