

from services.kite_connect import KiteConnect



def save_vendor_token(req_token):

    kit_connect = KiteConnect()
    kit_connect.save_request_token(
        req_token = req_token
    )

    pass 











