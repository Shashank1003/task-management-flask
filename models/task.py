from db import db


class TaskModel(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    story_points = db.Column(db.Integer, nullable=True)
    reporter = db.Column(db.String(30), nullable=False)
    assignee = db.Column(db.String(30), nullable=False)
    sub_tasks = db.relationship(
        "SubTaskModel", back_populates="parent_task", lazy="dynamic"
    )
