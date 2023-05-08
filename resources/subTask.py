import uuid

# from flask import re
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from models import TaskModel, SubTaskModel
from schemas import SubTaskSchema
from db import db
from flask_jwt_extended import jwt_required


blp = Blueprint("sub_tasks", __name__, description="Operations on sub tasks")


@blp.route("/subtask")
class SubTaskList(MethodView):
    @jwt_required()
    @blp.response(200, SubTaskSchema(many=True))
    def get(self):
        return SubTaskModel.query.all()

    @jwt_required()
    @blp.arguments(SubTaskSchema)
    @blp.response(201, SubTaskSchema)
    def post(self, sub_task_data):
        sub_task = SubTaskModel(**sub_task_data)

        try:
            db.session.add(sub_task)
            db.session.commit()
        except SQLAlchemyError as e:
            print("error", e)
            abort(500, message=str(e))

        return sub_task


@blp.route("/subtask/<string:subtask_id>")
class SubTask(MethodView):
    @jwt_required()
    @blp.response(200, SubTaskSchema)
    def get(self, subtask_id):
        subtask = SubTaskModel.query.get_or_404(subtask_id)
        return subtask

    @jwt_required()
    @blp.arguments(SubTaskSchema)
    @blp.response(200, SubTaskSchema)
    def put(self, subtask_data, subtask_id):
        subtask = SubTaskModel.query.get(subtask_id)
        if subtask:
            subtask.title = subtask_data["title"]
            subtask.description = subtask_data["description"]
            subtask.status = subtask_data["status"]
            subtask.assignee = subtask_data["assignee"]
            subtask.parent_task_id = subtask_data["parent_task_id"]
        else:
            subtask = SubTaskModel(**subtask_data, id=subtask_id)

        db.session.add(subtask)
        db.session.commit()

        return subtask

    @jwt_required()
    @blp.response(200)
    def delete(self, subtask_id):
        subtask = SubTaskModel.query.get_or_404(subtask_id)
        db.session.delete(subtask)
        db.session.commit()
        return {"message": "sub task deleted successfully"}
