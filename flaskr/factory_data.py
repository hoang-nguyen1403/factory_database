import os
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint("production", __name__, url_prefix="/production")

@bp.route("/warehouse", methods=("GET", "POST"))
def get_goods_data():
    try:
        if g.user is not None:
            conn = get_db().cursor()
            goods = conn.execute("SELECT * FROM MATHANG").fetchall()
            fetching_data = [dict( row)for row in goods]
            is_existing_db = True
        else:
            return render_template("production/warehouse.html")
    except:
        "failed to connecting to DB"

    return render_template("production/warehouse.html", is_existing_db=is_existing_db, fetching_data=goods)
