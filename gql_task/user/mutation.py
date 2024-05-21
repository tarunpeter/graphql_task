import graphene
from graphql_auth.bases import Output
from graphene import InputObjectType
from .schema import *
from .models import *
import graphql_jwt
from graphql import GraphQLError
from django.core.exceptions import ObjectDoesNotExist
from graphql_jwt.decorators import login_required,superuser_required

class UserInput(InputObjectType):
    email = graphene.String(required=True)
    username=graphene.String()
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)

class CreateUser(Output, graphene.Mutation):
    class Arguments:
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, **input):
        if input is None:
            raise GraphQLError("Input data is missing.")

        input_data = input.get('input')
        if input_data is None:
            raise GraphQLError("Input data is missing or improperly formatted.")

        app_user = User

        existing_user = app_user.objects.filter(email=input_data['email']).first()
        
        if existing_user:
            raise GraphQLError("A user with this email already exists.")

        user = app_user(
            username=input_data['username'],
            email=input_data['email'],
            first_name=input_data['first_name'],
            last_name=input_data['last_name'],
        )        
        user.set_password(input_data['password'])
        user.save()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        input = UserInput(required=True)

    user = graphene.Field(UserType)

    @login_required
    def mutate(self, info, user_id, **input):
        input_data = input.get('input')
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise GraphQLError("User not found.")
    
        if 'email' in input_data and input_data['email'] != user.email:
            if User.objects.filter(email=input_data['email']).exists():
                raise GraphQLError("A user with this email already exists.")
        user.username=input_data['username']
        user.email = input_data['email']
        user.first_name = input_data['first_name']
        user.last_name = input_data['last_name']
        user.set_password(input_data['password'])
        user.save()
        return UpdateUser(user=user)

        
class DeleteUser(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
    user = graphene.List(UserType)
    success = graphene.Boolean()

    @login_required
    @superuser_required
    def mutate(self, info, user_id):
        try:
            user = User.objects.get(pk=user_id)
            user.delete()
            return DeleteUser(success=True, user=User.objects.all())
        except ObjectDoesNotExist:
            raise GraphQLError("User not found.")
        
class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()