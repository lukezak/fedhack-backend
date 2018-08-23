# -*- coding: utf-8 -*-

"""
    eve-demo settings
    ~~~~~~~~~~~~~~~~~

    Settings file for our little demo.

    PLEASE NOTE: We don't need to create the two collections in MongoDB.
    Actually, we don't even need to create the database: GET requests on an
    empty/non-existant DB will be served correctly ('200' OK with an empty
    collection); DELETE/PATCH will receive appropriate responses ('404' Not
    Found), and POST requests will create database and collections when needed.
    Keep in mind however that such an auto-managed database will most likely
    perform poorly since it lacks any sort of optimized index.

    :copyright: (c) 2016 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""

import os

# We want to seamlessy run our API both locally and on Heroku. If running on
# Heroku, sensible DB connection settings are stored in environment variables.
MONGO_URI = os.environ.get('MONGODB_URI', 'mongodb://bioadmin:b1omedic@ds129762.mlab.com:29762/biomedic')

# Base API URI
URL_PREFIX="data"

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# Enable reads (GET), edits (PATCH) and deletes of individual items
# (defaults to read-only item access).
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']

# We enable standard client cache directives for all resources exposed by the
# API. We can always override these global settings later.
CACHE_CONTROL = 'max-age=20'
CACHE_EXPIRES = 20



# Our API will expose two resources (MongoDB collections): 'people' and
# 'works'. In order to allow for proper data validation, we define beaviour
# and structure.
people = {
    # 'title' tag used in item links.
    'item_title': 'person',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>/'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform GET
    # requests at '/people/<lastname>/'.
    'additional_lookup': {
        'url': 'regex(".*\-[\w]+\-.*")',
        'field': 'photoId'
    },

    # Schema definition, based on Cerberus grammar. Check the Cerberus project
    # (https://github.com/pyeve/cerberus) for details.
    'schema': {
        'photoId': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 256,
            # 'accountname' is an API entry-point, so we need it to be unique.
            'unique': True,
        },
        'firstName': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 156,
        },
        'lastName': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 500
        },
        'dateOfBirth': {
            'type': 'datetime',
        },
        # 'role' is a list, and can only contain values from 'allowed'.
        # 'role': {
        #     'type': 'list',
        #     'allowed': ["author", "contributor", "copy"],
        # },
        # An embedded 'strongly-typed' dictionary.
        'address': {
            'type': 'dict',
            'schema': {
                'addressLineOne': {'type': 'string'},
                'addressLineTwo': {'type': 'string'},
                'city': {'type': 'string'},
                'postcode': {'type': 'string'}
            },
        },
        'homePhone' : {
            'type': 'string'
        },
        'nextOfKinName' : {
            'type': 'string'
        },
        'nextOfKinPhone' : {
            'type': 'string'
        },
        'bloodType' : {
            'type': 'string'
        },
        'alergens' : {
            'type' : 'list'
        },
        'medicalHistory' : {
            'type': 'string'
        },
        'familyHistory' : {
            'type': 'string'
        },
        'habits' : {
            'type': 'list'
        },
        'vacinations' : {
            'type': 'list'
        },
        'occupation' : {
            'type': 'string'
        }
    }
}

# The DOMAIN dict explains which resources will be available and how they will
# be accessible to the API consumer.
DOMAIN = {
    'people': people
}