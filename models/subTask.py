from db import db


class SubTaskModel(db.Model):
    __tablename__ = "subtasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(30), nullable=False)
    assignee = db.Column(db.String(30), nullable=False)
    parent_task_id = db.Column(
        db.Integer(), db.ForeignKey("tasks.id"), unique=False, nullable=False
    )
    parent_task = db.relationship("TaskModel", back_populates="sub_tasks")
