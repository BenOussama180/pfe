from import_export import resources
from .models import Users

class UsersResource(resources.ModelResource):
    class meta:
        model : Users

