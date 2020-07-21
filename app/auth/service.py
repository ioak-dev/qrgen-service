import os, datetime, time, requests
from pymongo import MongoClient
import secrets, jwt
from library.db_connection_factory import get_collection
import library.db_utils as db_utils
import library.jwt_utils as jwt_utils
import app.user.service as user_service

DATABASE_URI = os.environ.get('DATABASE_URI')
ONEAUTH_API = os.environ.get('ONEAUTH_API')
if ONEAUTH_API is None:
    ONEAUTH_API = 'http://127.0.0.1:8020/auth/'

self_space_id = 'qrgen'
domain="user"

def do_jwttest(tenant):
    tenant=get_collection('qrgen', 'tenant').find_one({'name': tenant})
    #tenant = db_utils.find(tenant, domain,{'name': tenant})
    jwtPassword = tenant.get('jwtPassword')
    return (200, jwt.encode({
            'userId': '4587439657496t',
            'name': 'test user display name',
            'email': 'q1@1.com',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        }, jwtPassword, algorithm='HS256').decode('utf-8'))

def do_signin_via_jwt(tenant, data):
    tenantData=get_collection('qrgen', 'tenant').find_one({'name': tenant})
    #tenantData = db_utils.find(tenant, domain, {'name': tenant})
    jwtPassword = tenantData.get('jwtPassword')
    jwtToken = data.get('jwtToken')
    tokenData = jwt.decode(jwtToken, jwtPassword, algorithm='HS256')
    user = get_collection(tenant, 'user').find_one({'email': tokenData.get('email')})
    #user = db_utils.find(tenant, domain,{'email': tokenData.get('email')})
    if user is None:
        """ get_collection(tenant, 'user').insert_one({
            'name': tokenData.get('name'),
            'email': tokenData.get('email'),
            'type': 'JWT_USER'
        }) """
        db_utils.upsert(tenant, domain,{
            'name': tokenData.get('name'),
            'email': tokenData.get('email'),
            'type': 'JWT_USER'
        })
    else:
        """ get_collection(tenant, 'user').update({'_id': user.get('_id')},
        {
            'name': tokenData.get('name'),
            'email': tokenData.get('email'),
            'type': 'JWT_USER'
        }, upsert=True) """
        db_utils.upsert(tenant, domain, {
            {'_id': user.get('_id')},
            {
                'name': tokenData.get('name'),
                'email': tokenData.get('email'),
                'type': 'JWT_USER'
            }
        })
    
    user = get_collection(tenant, 'user').find_one({'email': tokenData.get('email')})
    #user = db_utils.find(tenant, user, {'email': tokenData.get('email')})
    return (200, {
        'name': user.get('name'),
        'email': user.get('email'),
        'token': jwt.encode({
                'name': str(user.get('_id')),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8)
            }, jwtPassword, algorithm='HS256').decode('utf-8'),
        'tenant': tenant,
        'secret': 'none'
    })

def get_session(space_id, auth_key):
    start_time = int(round(time.time() * 1000))
    response = requests.get(ONEAUTH_API + space_id + '/session/' + auth_key)
    if response.status_code != 200:
        return (response.status_code, response.json())
    oa_response = jwt_utils.decode(response.json()['token'])
    existing_user_data = user_service.find_by_user_id(space_id, oa_response['userId'])
    if len(existing_user_data) == 1:
        updated_record = user_service.update_user(space_id, {
            '_id': existing_user_data[0]['_id'],
            'firstName': oa_response['firstName'],
            'lastName': oa_response['lastName'],
            'email': oa_response['email']
        })
        updated_record['token'] = response.json()['token']
        return (200, updated_record)
    else:
        new_data = user_service.insert_user(space_id, {
            '_id': oa_response['userId'],
            'firstName': oa_response['firstName'],
            'lastName': oa_response['lastName'],
            'email': oa_response['email']
        })
        new_data['token'] = response.json()['token']
        return (200, new_data)
