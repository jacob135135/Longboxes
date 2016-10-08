# -*- coding: utf-8 -*-

db = DAL('sqlite://longboxes.db')

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)


## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# table definitions

# authors table
db.define_table('authors', Field('id', 'integer'), Field('full_name', 'string'), Field('type', 'string'))

# users table
db.define_table('users', Field('id', 'integer'), Field('username', 'string'), Field('password', 'string'))

# boxes table
db.define_table('boxes', Field('id', 'integer'), Field('owner_id', 'integer', 'reference users'), Field('title', 'string'), Field('date_created', 'datetime', default=request.now), Field('is_public', 'boolean', default=False))

# comics table
db.define_table('comics', Field('id', 'integer'), Field('title', 'string'), Field('issue_number', 'integer'), Field('publisher', 'string'), Field('short_description', 'text'), Field('image', 'upload'))

# comic_authors table
db.define_table('comic_authors', Field('comic_id', 'integer', 'reference comics'), Field('author_id', 'integer', 'reference authors'))

# box_contents table
db.define_table('box_contents', Field('box_id', 'integer', 'reference boxes'), Field('comic_id', 'integer', 'reference comics'))

#Add user1 to user5
# db.users.insert(username='user1', password='password1')
# db.users.insert(username='user2', password='password2')
# db.users.insert(username='user3', password='password3')
# db.users.insert(username='user4', password='password4')
# db.users.insert(username='user5', password='password5')

#Add 'Unfiled' box to users1 to user5
# db.boxes.insert(title = 'Unfiled', owner_id = 1, is_public = False)
# db.boxes.insert(title = 'Unfiled', owner_id = 2, is_public = False)
# db.boxes.insert(title = 'Unfiled', owner_id = 3, is_public = False)
# db.boxes.insert(title = 'Unfiled', owner_id = 4, is_public = False)
# db.boxes.insert(title = 'Unfiled', owner_id = 5, is_public = False)
