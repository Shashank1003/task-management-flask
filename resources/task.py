import uuid

# from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import TaskModel
from schemas import TaskSchema
from db import db

blp = Blueprint("tasks", __name__, description="operations on tasks")


@blp.route("/task")
class TaskList(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema(many=True))
    def get(self):
        return TaskModel.query.all()

    @jwt_required()
    @blp.arguments(TaskSchema)
    @blp.response(201, TaskSchema)
    def post(self, task_data):
        task = TaskModel(**task_data)
        try:
            db.session.add(task)
            db.session.commit()
        except SQLAlchemyError as e:
            print("error", e)
            abort(500, message=str(e))

        return task


@blp.route("/task/<string:task_id>")
class Task(MethodView):
    @jwt_required()
    @blp.response(200, TaskSchema)
    def get(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        return task

    @jwt_required()
    @blp.arguments(TaskSchema)
    @blp.response(200, TaskSchema)
    def put(self, task_data, task_id):
        task = TaskModel.query.get(task_id)

        if task:
            task.title = task_data["title"]
            task.description = task_data["description"]
            task.story_points = task_data["story_points"]
            task.status = task_data["status"]
            task.reporter = task_data["reporter"]
            task.assignee = task_data["assignee"]
        else:
            task = TaskModel(**task_data, id=task_id)

        db.session.add(task)
        db.session.commit()

        return task

    @jwt_required()
    def delete(self, task_id):
        task = TaskModel.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "task deleted"}
