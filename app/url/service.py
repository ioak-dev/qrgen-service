import os, datetime, time
import library.db_utils as db_utils
from bson.objectid import ObjectId

domain = 'url'

# def find(request, tenant):
#     data = db_utils.find(tenant, domain, {}))
#     return (200, {'data': data})

def find_all(request, tenant):
    data = db_utils.find(tenant, domain, {})
    return (200, {'data': data})

def update_url(request, tenant):
    updated_record = db_utils.upsert(tenant, domain, request.body, None)
    return (200, {'data': updated_record})

# def find_by_user_id(space_id, user_id):
#     return db_utils.find(space_id, domain, {'_id': user_id})
