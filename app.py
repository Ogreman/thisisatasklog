# app.py

import os

from flask import request, url_for, render_template

from flask.ext.api import FlaskAPI, status, exceptions
from flask.ext.api.decorators import set_renderers
from flask.ext.api.renderers import HTMLRenderer
from flask.ext.api.exceptions import APIException
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy import Column, String, Integer, DateTime


app = FlaskAPI(__name__)
app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL'],
)
db = SQLAlchemy(app)


class TaskHistory(db.Model):

    __tablename__ = "taskhistory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task = Column(String)
    target = Column(String)
    result = Column(Integer)
    time = Column(DateTime)

    def __repr__(self):
        return "Task history of task: {task}.".format(
            task=self.task,
        )

    def to_json(self):
        return {
            'id': self.id,
            'task': self.task,
            'target': self.target,
            'result': self.result,
            'time': self.time,
        }

    @classmethod
    def get_tasks(self):
        return [
            log.to_json() for log in TaskHistory.query.all()
        ]


@app.route("/api/", methods=['GET', 'POST'])
def logs():
    """
    List or create logs.
    """
    if request.method == 'POST':
        log = TaskHistory(
            task=request.data.get('task', ''),
            target=request.data.get('target', ''),
            result=request.data.get('result', 0),
            time=request.data.get('time', ''),
        )
        db.session.add(log)
        db.session.commit()
        return log.to_json(), status.HTTP_201_CREATED
    return TaskHistory.get_tasks(), status.HTTP_200_OK


if __name__ == "__main__":
    app.run(debug=True)