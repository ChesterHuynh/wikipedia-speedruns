from flask import jsonify, request, Blueprint, session

from db import get_db
from pymysql.cursors import DictCursor

from datetime import datetime


run_api = Blueprint('runs', __name__, url_prefix='/api/runs')


@run_api.route('/', methods=['POST'])
def create_run():
    query = "INSERT INTO `runs` (`start_time`, `end_time`, `path`, `prompt_id`, `user_id`) VALUES (%s, %s, %s, %s, %s)"
    sel_query = "SELECT LAST_INSERT_ID()"

    # datetime wants timestamp in seconds since epoch
    start_time = datetime.fromtimestamp(request.json['start_time']/1000)
    end_time = datetime.fromtimestamp(request.json['end_time']/1000)
    path = str(request.json['path']) # TODO Format path
    prompt_id = request.json['prompt_id']

    print(session)
    user_id = session['user_id']
    # TODO validate

    db = get_db()
    with db.cursor() as cursor:
        result = cursor.execute(query, (start_time, end_time, path, prompt_id, user_id))
        
        cursor.execute(sel_query)
        id = cursor.fetchone()[0]
        db.commit()

        return jsonify(id)

    return "Error submitting prompt"


@run_api.route('/', methods=['GET'])
def get_all_runs():
    # TODO this should probably be paginated, and return just ids
    query = "SELECT * FROM `runs`"

    db = get_db()
    with db.cursor(cursor=DictCursor) as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)


