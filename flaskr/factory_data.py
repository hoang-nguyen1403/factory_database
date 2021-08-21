import os
import functools

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app, g

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.db import close_db

bp = Blueprint("production", __name__, url_prefix="/production")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.route("/warehouse", methods=("GET", "POST"))
@login_required
def get_goods_data():
    try:
        if g.user is not None:
            conn = get_db()
            conn.commit()
            mathang = conn.execute("SELECT * FROM MATHANG").fetchall()
            loaihang = conn.execute("SELECT * FROM LOAIHANG").fetchall()
            is_existing_db = True

            conn.close()
        else:
            return render_template("production/warehouse.html")
    except:
        "failed to connecting to DB"

    return render_template("production/warehouse.html", is_existing_db=is_existing_db,
                           mathang=mathang, loaihang=loaihang)


@bp.route("/warehouse/<string:msmh>/delete", methods=("POST",))
def xoa_mahang(msmh):
    conn = get_db()
    print(f"DELETE from MATHANG WHERE MSMH = {msmh}")
    conn.execute(f"DELETE from MATHANG WHERE MSMH = '{msmh}'")
    conn.commit()
    conn.close()
    print("Deleted ")
    return redirect(url_for("production.get_goods_data"))


@bp.route("/addnew", methods=("GET", "POST"))
@login_required
def them_mathang():
    if request.method == "POST":
        msmh = request.form["MSMH"]
        TENMH = request.form["TENMH"]
        MOTA = request.form["MOTA"]
        MATHANGDVT = request.form["MATHANGDVT"]
        MSLOAI = request.form["MSLOAI"]

        error = None

        if not msmh:
            error = "MSMH is required."

        if error is not None:
            flash(error)
        else:
            conn = get_db()
            print(f"INSERT INTO MATHANG VALUES ('{msmh}', '{TENMH}' , '{MOTA}', '{MATHANGDVT}' , '{MSLOAI}' )")
            conn.execute(f"INSERT INTO MATHANG VALUES ('{msmh}', '{TENMH}', '{MOTA}', '{MATHANGDVT}' , '{MSLOAI}' );")
            conn.commit()
            conn.close()
            return redirect(url_for("production.get_goods_data"))
    else:
        return render_template("production/addnew.html")

@bp.route("/edit", methods=("GET", "POST"))
@login_required
def sua_mathang():
    if request.method == "POST":
        msmh = request.form["MSMH"]
        TENMH = request.form["TENMH"]
        MOTA = request.form["MOTA"]
        MATHANGDVT = request.form["MATHANGDVT"]
        MSLOAI = request.form["MSLOAI"]

        error = None

        if not msmh:
            error = "MSMH is required."

        if error is not None:
            flash(error)
        else:
            conn = get_db()
            print(f"UPDATE MATHANG SET TENMH = '{TENMH}',MOTA= '{MOTA}', MATHANGDVT = '{MATHANGDVT}', MSLOAI = '{MSLOAI}' WHERE msmh = '{msmh}'")
            conn.execute(f"UPDATE MATHANG SET TENMH = '{TENMH}',MOTA= '{MOTA}', MATHANGDVT = '{MATHANGDVT}', MSLOAI = '{MSLOAI}' WHERE msmh = '{msmh}'")
            conn.commit()
            conn.close()
            return redirect(url_for("production.get_goods_data"))
    else:
        return render_template("production/edit.html")
