# from flask import , request, jsonify
from flask import Flask, Response, redirect, render_template, url_for, request, Blueprint
from domains.vendor_auth.auth_services import VendorAPIClientService, VendorAuthFlowService

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



@auth_bp.route("/vendor_login", endpoint="vendor_login_endpoint")
def vendor_login():
    login_url = VendorAPIClientService.get_login_url()
    return redirect(login_url)

@auth_bp.route("/vendor_request_token", endpoint="vendor_request_token")
def vendor_token():
    vendor_request_token = request.args.get("request_token")
    vendor_access_token = VendorAPIClientService.get_access_token(
        request_token= vendor_request_token
    )
    # vendor_access_token = {}
    # vendor_access_token["access_token"] = "98hujiop"
    VendorAuthFlowService.create_update_token(
        # token_date = current_date,
        request_token = vendor_request_token,
        access_token = vendor_access_token["access_token"]
    )
    VendorAPIClientService.attach_access_token(
        access_token= vendor_access_token["access_token"]
    )
    return redirect(url_for(" "))








