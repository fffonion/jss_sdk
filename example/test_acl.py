from jss.connection import JssClient


jss = JssClient('ACCESS_KEY', 'SECRET_KEY',
                        'storage.jcloud.com')
buc_name = 'BUCKET_NAME'
jss.bucket(buc_name).acl().internetVisible().allowAnyoneRead().set()
print(jss.bucket(buc_name).acl().get())