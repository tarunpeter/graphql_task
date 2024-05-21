import graphene
from graphql_auth.bases import Output
from graphene import InputObjectType
from graphql import GraphQLError
from .models import *
from .schema import *
from graphql_jwt.decorators import login_required
#Ecclesia Region
class UserRecordInput(InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    age = graphene.Int()
   
class CreateUserRecord(Output, graphene.Mutation):
    class Arguments:
        input = UserRecordInput(required=True)

    user_record = graphene.List(UserRecordType)
    
    @login_required
    def mutate(self, info, **input):
        input = input['input']
        user_record = UserRecord(**input)
        user_record.save()
        return CreateUserRecord(user_record=UserRecord.objects.all())

class UpdateUserRecord(Output, graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UserRecordInput(required=True)

    user_record = graphene.List(UserRecordType)
    
    @login_required
    def mutate(self, info, id, **input):
        input = input['input']
        user_record = UserRecord.objects.filter(id=id).exists()
        if user_record:
            UserRecord.objects.filter(id=id).update(**input)
        else:
            raise GraphQLError("Record not found")

        return UpdateUserRecord(user_record=UserRecord.objects.all())
    
class DeleteUserRecord(Output, graphene.Mutation):
    class Arguments:
        ids = graphene.List(graphene.ID)

    user_record = graphene.List(UserRecordType)
    
    @login_required
    def mutate(root, info, ids):
        user_record = UserRecord.objects.filter(id__in=ids)
        if user_record:
            user_record.delete()
        return DeleteUserRecord(user_record=UserRecord.objects.all())

class Mutation(graphene.ObjectType):
#Ecclesia Region
    create_user_record = CreateUserRecord.Field()
    update_user_record = UpdateUserRecord.Field()
    delete_user_record = DeleteUserRecord.Field()