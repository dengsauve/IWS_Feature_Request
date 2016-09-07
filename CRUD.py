from __init__ import db, User, Request
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
    new_user = User(username=user[0], email=user[1], password=user[2], client_id=user[4])
    db.session.add(new_user)

db.session.flush()

for request in Mock_Requests[1:]:
    new_request = Request(title=request[0], description=request[1], client_id=request[2], priority=request[3], targetdate=request[4], ticketurl=request[5], productarea_id=request[6], user_id=request[7])
    db.session.add(new_request)

db.session.commit()
