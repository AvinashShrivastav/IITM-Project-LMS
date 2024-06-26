# from flask_restful import Resource, Api
# from application.database import db
# from application.models import User
# from flask_restful import fields, marshal_with
# from application.validation import NotFoundError



# output_fields = {
#     "user_id": fields.Integer,
#     "username": fields.String,
#     "email": fields.String
    
# }

# class UserAPI(Resource):
#   @marshal_with(output_fields)
#   def get(self, username):
#     print(username)
#     user = db.session.query(User).filter_by(username=username).first()
#     if user is None:
#       raise NotFoundError(status_code=404)
#     return user
  
#   def put(self, username):
#     print(username)
#     return {"username": username}
  
#   def delete(self, username):
#     print(username)
#     return {"username": username}
  
#   def post(self):
#     pass
  

