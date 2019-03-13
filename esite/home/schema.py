from __future__ import unicode_literals
import graphene
from django.db import models
from graphene_django import DjangoObjectType
from esite.home import graphene_wagtail
from esite.home.models import HomePage, Button, User
from graphene.types.generic import GenericScalar
from .graphene_wagtail import DefaultStreamBlock, create_stream_field_type

class UserNode(DjangoObjectType):
    class Meta:
        model = User


# Blocks
class HeaderBlock(DefaultStreamBlock):
    pass

class SectionBlock(DefaultStreamBlock):
    pass

class FooterBlock(DefaultStreamBlock):
    pass

class ButtonBlock(graphene.ObjectType):
    value = GenericScalar()
    button = graphene.Field(UserNode)

    def resolve_user(self, info):
        return User.objects.get(id=self.value)

class UserBlock(graphene.ObjectType):
    value = GenericScalar()
    user = graphene.Field(UserNode)

    def resolve_user(self, info):
        return User.objects.get(id=self.value)


# Objects
class HomePageBody(graphene.Union):
    class Meta:
        types = (HeaderBlock, SectionBlock, FooterBlock, ButtonBlock, UserBlock)

class HomePageNode(DjangoObjectType):
    headers = graphene.List(HomePageBody)
    sections = graphene.List(HomePageBody)
    footers = graphene.List(HomePageBody)

    class Meta:
        model = HomePage
        only_fields = [
            'id',
            'title',
            'city',
            'zip_code',
            'address',
            'telephone',
            'telefax',
            'vat_number',
            'tax_id',
            'trade_register_number',
            'court_of_registry',
            'place_of_registry',
            'trade_register_number',
            'ownership',
            'email',
            'sociallinks'
        ]
    
    def resolve_headers(self, info):
        repr_headers = []
        for block in self.headers.stream_data:
            block_type = block.get('type')[0]
            value = block.get('value')
            if block_type == 'h':
                repr_headers.append(HeaderBlock(value=value))
        return repr_headers

    def resolve_sections(self, info):
        repr_sections = []
        for block in self.sections.stream_data:
            block_type = block.get('type')[0]
            value = block.get('value')
            if block_type == 's':
                repr_sections.append(SectionBlock(value=value))
        return repr_sections

    def resolve_footers(self, info):
        repr_footers = []
        for block in self.footers.stream_data:
            block_type = block.get('type')[0]
            value = block.get('value')
            if block_type == 'f':
                repr_footers.append(FooterBlock(value=value))
        return repr_footers


# Query
class Query(graphene.AbstractType):
    homepage = graphene.List(HomePageNode)

    @graphene.resolve_only_args
    def resolve_homepage(self):
        return HomePage.objects.live()
