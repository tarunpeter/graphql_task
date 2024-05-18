import graphene
from graphene_django import DjangoObjectType
from mil_records.schema import Query as user_Q 

class Query(user_Q,graphene.ObjectType):
    home = graphene.String()

    def resolve_home(self, info):
        return "Welcome to User"
    

class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)