from models.models import Permission


# This function fetches permissions and returns them as a list of dictionaries.
def get_user_permissions(user_id):
    permissions = Permission.query.filter_by(user_id=user_id).all()
    permissions_list = [
        {
            "id": p.id,
            "user_id": p.user_id,
            "subject": p.subject,
            "object": p.object,
            "action": p.action,
        }
        for p in permissions
    ]
    return permissions_list
