from __init__ import db, User
import csv

Mock_Users, Mock_Requests = [], []

with open('documents/User_Data.csv') as f:
    freader = csv.reader(f)
    Mock_Users = list(freader)

with open('documents/Request_Data.csv') as g:
    greader = csv.reader(g)
    Mock_Requests = list(greader)

# user_counter = 2
for user in Mock_Users:
    new_user = User(user[0], user[1], user[2], user[3], user[4])
    db.session.add(new_user)

db.session.commit()


for request in Mock_Requests[1:]:
    new_request = Request(request[0], request[1], request[2], request[3], request[4], request[5], request[6], request[7])
    db.session.add(new_request)

db.session.commit()
