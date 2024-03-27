import graphene
from graphene_django import DjangoObjectType
from room.models import Room

class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        field = ['id', 'name']

class Query(graphene.ObjectType):
    list_room = graphene.List(RoomType)

    def resolve_list_room(root, info):
        return Room.objects.all()

schema = graphene.Schema(query=Query)
