import graphene
from graphene_django.types import DjangoObjectType
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination
from graphene_django_extras.fields import DjangoFilterPaginateListField
from .models import UserRecord
from graphql_jwt.decorators import login_required

class UserRecordType(DjangoObjectType):
    class Meta:
        model = UserRecord
        fields = "__all__"
        filter_fields = {
            "id": ("exact",),
            "name": ("icontains", "iexact"),
        }

class Query(graphene.ObjectType):
    list_users = DjangoFilterPaginateListField(UserRecordType,  search=graphene.String(),pagination = LimitOffsetGraphqlPagination(default_limit=10, ordering="name"))

    @login_required
    def resolve_list_users(root, info, search=None, **kwargs):
        queryset = UserRecord.objects.all()
        
        # Apply search filter if provided
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        
        
        return queryset
