from marshmallow import Schema, fields


class PlainTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    story_points = fields.Int()
    reporter = fields.Str()
    assignee = fields.Str()


class PlainSubTaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    status = fields.Str()
    assignee = fields.Str()


class TaskSchema(PlainTaskSchema):
    sub_tasks = fields.Nested(PlainSubTaskSchema(), many=True)


class SubTaskSchema(PlainSubTaskSchema):
    parent_task_id = fields.Int(required=True, load_only=True)
    parent_task = fields.Nested(PlainTaskSchema(), dump_only=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
