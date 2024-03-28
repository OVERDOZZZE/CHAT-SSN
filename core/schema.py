import graphene
from graphene_django import DjangoObjectType
from room.models import Room, Message
from graphene import Enum


class SortDirection(Enum):
    ASC = "ASC"
    DESC = "DESC"


class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = '__all__'


class RoomType(DjangoObjectType):
    class Meta:
        model = Room
        fields = ['id', 'name', 'slug']


class Query(graphene.ObjectType):
    list_message = graphene.List(
        MessageType, sortBy=graphene.String(),
        sortOrder=SortDirection()
    )

    list_room = graphene.List(RoomType)
    read_room = graphene.Field(RoomType, id=graphene.Int())

    def resolve_list_room(root, info):
        return Room.objects.all()

    def resolve_list_message(root, info, sortBy=None, sortOrder=None, **kwargs):
        queryset = Message.objects.all()

        if sortBy:
            if sortOrder == SortDirection.ASC:
                queryset = queryset.order_by(sortBy)
            elif sortOrder == SortDirection.DESC:
                queryset = queryset.order_by('-'+sortBy)

        return queryset

    def resolve_read_room(root, info, id):
        return Room.objects.get(id=id)


class RoomMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        slug = graphene.String()

    room = graphene.Field(RoomType)

    @classmethod
    def mutate(cls, root, info, name, slug, id=None):
        if id:
            room = Room.objects.get(id=id)
            room.name = name
            room.slug = slug
            room.save()
        else:
            room = Room(name=name, slug=slug)
            room.save()

        return RoomMutation(room=room)


class RoomDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    room = graphene.Field(RoomType)

    @classmethod
    def mutate(cls, root, info, id):
        room = Room.objects.get(id=id)
        room.delete()
        return RoomDelete(room=None)


class Mutation(graphene.ObjectType):
    create_room = RoomMutation.Field()
    update_room = RoomMutation.Field()
    delete_room = RoomDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
