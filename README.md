# NYPflask
For my juniors
For app development project 

pip install:

1) flask_uploads.py
2)	flask_sqlachemy
3)	flask
4)	flask_bcrypt
5)	flask_uploads
6)	flask_msearch
7)	flask_login
8)	flask_migrate
9)	wtforms
10)	flask_wtf
11)	zmq
12)	email_validators
13)	stripe

npm install @splinetool/runtime

press run for run.py
go to the routeing page for werkzeug
change

from werkzeug import secure_filename, filestorage

to

from werkzeug.utils import secure_filename
from werkzeug.datastructurre import file storage

run run.py again and go the path with principle error, go to that line and delete that line

(if admin not accessable )
go to customer / routes.py
remove if checker for admin, use naveen@site.com , darkignitor@site.com, sam@site.com, nigel@site.com, jasper@site.com with any password.

validator should look like line 83
if...
	if..(@site.com) -> remove this line
.
.
.
	else:
		... -> delete else

original creator
https://github.com/samuelyuoh/Agrgracefully-flask
 go and tell only those you trust or have problems for app dev o7
