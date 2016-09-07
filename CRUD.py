from __init__ import db, User, Request
import datetime

# Mock_Users, Mock_Requests = [], []

# with open('documents/User_Data.csv') as f:
#     freader = csv.reader(f)
#     Mock_Users = list(freader)

# with open('documents/Request_Data.csv') as g:
#     greader = csv.reader(g)
#     Mock_Requests = list(greader)

def create_user(db, User, user):
    new_user = User(username=user[0], email=user[1], password=user[2], isAdmin=False, client_id=user[4])
    db.session.add(new_user)


def create_request(db, Request, request):
    tdate = datetime.datetime.strptime(request[4], "%Y-%m-%d")
    new_request = Request(title=request[0], description=request[1], client_id=request[2], priority=request[3], targetdate=tdate, ticketurl=request[5], productarea_id=request[6], user_id=request[7])
    db.session.add(new_request)
