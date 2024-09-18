import graphene
from schema.query.definition import Query


schema = graphene.Schema(query=Query)
