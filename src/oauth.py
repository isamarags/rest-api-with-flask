from flask import request, jsonify
from functools import wraps
from models import User
import jwt

def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = None
    if "Authorization" in request.headers:
      token = request.headers["Authorization"].split(" ")[1]
    if not token:
      return {
        "message": "Authentication Token is missing!",
        "data": None,
        "error": "Unauthorized"
      }, 401
    try:
      data = jwt.decode(jwt=token, key="teste", algorithms="HS256")

    except Exception as e:
      print("Error: ", e)
      return jsonify({'message': 'token is invalid or expired', 'data': {}}), 401

    return f(*args, **kwargs)
    
  return decorated
