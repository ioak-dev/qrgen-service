import os, datetime, time
import library.db_utils as db_utils
from bson.objectid import ObjectId

domain = 'user'
domain_role_permissions = 'role_permissions'

def find(request, tenant):
    data = remove_sensitive_data(db_utils.find(tenant, domain, {'_id': request.user_id}))
    return (200, {'data': data})

def find_all(request, tenant):
    data = remove_sensitive_data(db_utils.find(tenant, domain, {}))
    return (200, {'data': data})

def expand_authors(tenant, data):
    for item in data:
        last_modified_by = db_utils.find(tenant, domain, {'_id': item.get('lastModifiedBy')})
        created_by = db_utils.find(tenant, domain, {'_id': item.get('createdBy')})
        item['lastModifiedByEmail'] = last_modified_by[0].get('email')
        item['createdByEmail'] = created_by[0].get('email')
    return data

def update_user(request, tenant):
    print(request.body)
    updated_record = db_utils.upsert(tenant, domain, request.body, request.user_id)
    return (200, {'data': updated_record})


def find_permitted_actions(tenant, user_id):
    roles = db_utils.find(tenant, domain, {'_id': user_id})[0].get('roles')
    roles.append('open')
    return db_utils.find(tenant, domain_role_permissions, {'role': {'$in': roles}})

def can_i_perform(permitted_actions, action, domain, condition, group=None):
    for item in permitted_actions:
        if item.get('action') == action and item.get('domain') == domain and item.get('condition') == condition:
            if group == None or item.get('group') == group:
                return True
    return False

def who_can_perform(permitted_actions, action, domain, condition):
    group_list = []
    for item in permitted_actions:
        if item.get('action') == action and item.get('domain') == domain and item.get('condition') == condition and item.get('group') != None:
                group_list.append(item.get('group'))
    return group_list

def remove_sensitive_data(data):
    # for item in data:
    #     del item['problem']
    #     del item['solution']
    return data

def find_by_user_id(space_id, user_id):
    return db_utils.find(space_id, domain, {'_id': user_id})

def update_user(space_id, data, user_id=None):
    return db_utils.upsert(space_id, domain, data, user_id)

def insert_user(space_id, data, user_id=None):
    data['_id'] = ObjectId(data['_id'])
    return db_utils.insert(space_id, domain, data, user_id)

