import jwt
from flask import jsonify, request, current_app, g
from functools import wraps
from schema import User

def jwt_required(role = None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # get token
            header = request.headers.get("Authorization")
            if not header or not header.startswith("Bearer "):
                return jsonify({"Error": "Missing token.."})
            token = header.split(" ")[1]

            try:
                payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms = ["HS256"])
            except jwt.ExpiredSignatureError:
                return jsonify({"error":"expired token"})
            except jwt.InvalidTokenError:
                return jsonify({"error":"invalid token"})
            except:
                return jsonify({"error":"somethin's wrong.."})
            #stateful authorization of user, helps dynamic updates.
            user = User.query.get(payload["user_id"])

            if not user:
                return jsonify({"error":"user dne"})
            if role and user.role!=role:
                return jsonify({"error":"forbidden access"})
            
            #store user using http global 
            g.current_user = user

            return f(*args, **kwargs)
        return wrapper
    return decorator