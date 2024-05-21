import graphene
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import permission_required,login_required
from graphene_django import DjangoObjectType
from .models import *
class UserType(DjangoObjectType):
    class Meta:
        model=get_user_model()

class Query(graphene.ObjectType):
    list_users = graphene.List(UserType)
    list_loggedin_users=graphene.Field(UserType)
    me = graphene.Field(UserType)

    @login_required
    @permission_required("auth.view_user")
    def resolve_list_users(self,info):
        return get_user_model().objects.all()
    
    @login_required
    def resolve_list_loggedin_users(self, info, **kwargs):
        return info.context.user
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user