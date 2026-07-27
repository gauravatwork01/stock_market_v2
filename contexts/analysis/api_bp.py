
from flask import Blueprint, redirect, request, render_template 
from .services.app_services import AnalysisAppService



analysis_bp = Blueprint("analysis_bp", __name__, url_prefix="/analysis")


@analysis_bp.route("/", endpoint="home", methods=["GET"])
def analysis_home():
    AnalysisAppService().get_report()

    return {"status": "done"}, 200 




