"""
This module contains the routes for the search page.
"""
from flask import Blueprint, render_template, request
from app.db import get_all_products, query_products
bp = Blueprint("search", __name__)


@bp.route("/substitute/", methods=("GET", "POST"))
def substitute():
    if request.method == "POST":
        query = request.form.get('query')
        if query:
            data = query_products(query)
            return render_template("substitute.html", data=data)

    return render_template("substitute.html")

@bp.route("/comparison/")
def comparison():
    products_df = get_all_products()
    return render_template("comparison.html", parts=products_df)
