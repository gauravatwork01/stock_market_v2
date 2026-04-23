from flask import Blueprint
from interfaces import controller
from app.services import auth_app_service


api_bp = Blueprint("api", __name__)

@api_bp.route("/auth/vendor_login")
def vendor_login():
    controller.AuthController.vendor_login()
    return {"msg": "users"}


@api_bp.route("/auth/vendor_request_token")
def vendor_login():
    controller.AuthController.accept_vendor_request_token()
    return {"msg": "users"}