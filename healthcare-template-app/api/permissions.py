from flask import request
from flask_login import login_required
from flask_restx import Namespace, Resource
from models.models import db, User, Permission
from util.auth.auth import log_user_activity  
from util.data_access.permissions import get_user_permissions
from util.rate_limiting.rate_limiter import limiter

api = Namespace('permissions', description="""This is a special INTERNAL FACING API for ADMINS used by the Flask application. There is no token required for this API, but depends on the user being logged in using the Flask-Login mechanism, in addition to havbing the proper RBAC permissions for that user. If you want to experiment with this endpoint via Postman or Requests, you would first need to create a new session to login in, then use the session cookie to access this endpoint.""")

@api.route('/', methods=['GET', 'POST'])
class Permissions(Resource):
    @login_required
    @log_user_activity
    def get(self):
        permissions = Permission.query.all()
        permissions_list = [{"id": p.id, "user_id": p.user_id, "subject": p.subject, "object": p.object, "action": p.action} for p in permissions]
        return permissions_list, 200

    @login_required
    @log_user_activity
    @limiter.limit("5 per second")
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['subject']).first()
        if not user:
            return {"message": "User not found"}, 404
        new_permission = Permission(
            user_id=user.id,
            subject=data['subject'], 
            object=data['object'], 
            action=data['action'])
        db.session.add(new_permission)
        db.session.commit()
        return {"message": "Permission created"}, 201
        
@api.route('/<int:user_id>', methods=['GET'])
class UserPermission(Resource):
    @login_required
    def get(self, user_id):
        permissions = get_user_permissions(user_id)
        return permissions, 200
    
@api.route('/<int:permission_id>', methods=['PUT', 'DELETE'])
class ModifyPermission(Resource):
    @login_required
    def put(self, permission_id):
        permission = Permission.query.get(permission_id)
        if not permission:
            return {"message": "Permission not found"}, 404
        data = request.get_json()
        # Assuming user_id and subject should not be editable based on your requirements
        permission.object = data.get('object', permission.object)
        permission.action = data.get('action', permission.action)
        db.session.commit()
        return {"message": "Permission updated"}, 200
        
    @login_required
    def delete(self, permission_id):
        permission = Permission.query.get(permission_id)
        if permission:
            db.session.delete(permission)
            db.session.commit()
            return {"message": "Permission deleted"}, 200
        else:
            return {"message": "Permission not found"}, 404