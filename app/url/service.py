import os, datetime, time
import library.db_utils_nospace as db_utils
from bson.objectid import ObjectId

domain = 'url'

def create(request):
    data = db_utils.create(domain)
    return (200, {'data': data})

#def find_get_url_key(urlkey) :
 #   data = db_utils.find({'urlkey':urlkey})
  #   return (200, {'data': data})

#def find_by_key( acesskey):
 #   data = db_utils.find_by_key(domain, {'acesskey':acesskey})
 #   return (200, {'data':data})


#def update_by_key(acesskey):
#    data = db_utils.upsert( domain, {'acesskey': acesskey})
  #  return (200, {'data': updated_record})

#def delete_by_key(acesskey):
#    data = db_utils.delete(domain, {'acesskey':acesskey})
  #  return (200, {'deleted_count': data.deleted_count})