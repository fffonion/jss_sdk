# -*- coding: utf-8 -*- 
'''
Created on 2014-12-01
@author: fffonion
'''
from jss.util import error_handler
import json

class acl_policy(object):
    def __init__(self, bucket_name, data = None):
        self.Bucket = bucket_name
        self.CreationDate = ''
        self.InternetVisible = False
        self._AccessControlList = []
        if data:
            self.deserialize(data)

    def serialize(self):
        dic = dict([(x, self.__dict__[x]) for x in self.__dict__ if not x.startswith('_')])
        dic['AccessControlList'] = []
        for g, p in self._AccessControlList:
            dic['AccessControlList'].append({'Grantee':g, 'Permission':p})
        return json.dumps(dic)

    def deserialize(self, data):
        dic = json.loads(data)
        dic['_AccessControlList'] = []
        for g, p in dic['AccessControlList']:
            dic['_AccessControlList'].append({'Grantee':g, 'Permission':p})
        del dic['AccessControlList']
        self.__dict__.update(dic)

    def grant(self, grantee, permission):
        self._AccessControlList.append((grantee, permission))#not checking duplicate

class acl(object):
    def __init__(self, bucket_name, jss_client):
        self.bucket_name = bucket_name
        self.jss_client = jss_client
        self.policy = acl_policy(bucket_name)

    def allowAnyoneRead(self):
        self.policy.grant('*', 'READ')
        return self
   
    def internetVisible(self):
        self.policy.InternetVisible = True
        return self
   
    def grant(self, grantee, permission):
        self.policy.grant(grantee, permission)
        return self
   
   
    def set(self):
        entity = self.policy.serialize()
        if len(entity) > 4096:
            error_handler("Access control policy entity must less than 4096 byte,current size:%d" % len(entity)) 
        headers = {'Content-Type':'application/json; charset=UTF-8'}
        return self.jss_client.make_request('PUT', 
            bucket_name = self.bucket_name, 
            headers = headers,
            subresource = 'acl',
            query_args = 'acl',
            data = entity)
        
   
    def delete(self):
        response = self.jss_client.make_request('DELETE', 
            bucket_name = self.bucket_name, 
            subresource = 'acl',
            query_args = 'acl')
        if response.status/100!=2:
            error_handler(response)
        return  response.read()
   
    def get(self):
        response = self.jss_client.make_request('GET', 
            bucket_name = self.bucket_name, 
            subresource = 'acl',
            query_args = 'acl')
        if response.status/100!=2:
            error_handler(response)
        data = response.read()
        self.policy.deserialize(data)

   