import graphene
from graphene_django.types import DjangoObjectType
from .models import Project, User

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project

# UserType definition
class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    project = graphene.Field(ProjectType, id=graphene.Int())

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_project(root, info, id):
        return Project.objects.get(pk=id)

class ModalDetailInput(graphene.InputObjectType):
    project = graphene.String(required=True)
    client = graphene.String(required=True)
    language = graphene.String(required=True)
    preview = graphene.String(required=True)
    link = graphene.String(required=True)

class CreateProject(graphene.Mutation):
    class Arguments:
        type = graphene.String(required=True)
        image = graphene.String(required=True)
        tag = graphene.List(graphene.String, required=True)
        delayAnimation = graphene.String()
        modalDetails = graphene.List(ModalDetailInput, required=True)
        user_id = graphene.Int(required=True)  # foreign key

    project = graphene.Field(ProjectType)

    def mutate(self, info, type, image, tag, delayAnimation, modalDetails, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Exception("User not found")

        # Convert modalDetails to list of dictionaries
        modal_details_data = [
            {
                'project': detail.project,
                'client': detail.client,
                'language': detail.language,
                'preview': detail.preview,
                'link': detail.link
            } for detail in modalDetails
        ]

        project = Project.objects.create(
            type=type,
            image=image,
            tag=tag,
            delayAnimation=delayAnimation,
            modalDetails=modal_details_data,
            user=user
        )
        return CreateProject(project=project)

# CreateUser mutation
class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, email):
        user = User(username=username, email=email)
        user.save()
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_project = CreateProject.Field()
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)