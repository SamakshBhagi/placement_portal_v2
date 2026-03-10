from flask import jsonify
def respond(meta = None, data=None, message = "", success = True, status = 200):
    return jsonify({
        "success": success,
        "message":message,
        "status": status,
        "data":data,
        "meta":meta
    })