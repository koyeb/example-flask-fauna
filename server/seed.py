import os
from dotenv import load_dotenv
from faunadb import query as q
from faunadb.client import FaunaClient

load_dotenv()
FAUNA_ADMIN_SECRET = os.getenv("FAUNA_ADMIN_SECRET")

fauna = FaunaClient(secret=FAUNA_ADMIN_SECRET)


def create_collection(client):
    client.query(q.create_collection({"name": "users"}))


def create_indexes(client):
    index = {
        "name": "user_by_email",
        "source": q.collection("users"),
        "terms": [{"field": ["data", "email"]}],
    }

    client.query(q.create_index(index))


def seed_users(client):
    client.query(q.map_(
        lambda userRef: q.delete(userRef),
        q.paginate(q.documents(q.collection('users')))
    ))
    users = [
        {"data": {"email": "foo@koyeb.com", "type": "admin"},
            "credentials": {"password": "verysecure"}},
        {"data": {"email": "bar@koyeb.com", "type": "user"},
            "credentials": {"password": "thebestpasswordever"}},
        {"data": {"email": "foobar@koyeb.com", "type": "user"},
            "credentials": {"password": "theanswertoallquestions"}},
    ]

    client.query(q.map_(
        lambda user: q.create(q.collection('users'), user),
        users
    ))


def create_roles(client):
    roles = [
        {
            "name": "admin",
            "membership": [
                {
                    "resource": q.collection("users"),
                    "predicate": q.query(lambda ref: q.equals(q.select(["data", "type"], q.get(ref)), "admin"))
                }
            ],
            "privileges":[
                {
                    "resource": q.collection("users"),
                    "actions": {
                        "read": True,
                        "create": True,
                        "write": True
                    }
                }
            ]
        },
        {
            "name": "user",
            "membership": [
                {
                    "resource": q.collection("users"),
                    "predicate": q.query(lambda ref: q.equals(q.select(["data", "type"], q.get(ref)), "user"))
                }
            ],
            "privileges":[
                {
                    "resource": q.collection("users"),
                    "actions": {
                        "read": q.query(lambda ref: q.equals(q.current_identity(), ref)),
                        "write": q.query(lambda ref: q.equals(q.current_identity(), ref)),
                    }
                }
            ]

        }
    ]
    client.query(q.map_(
        lambda role: q.create_role(role),
        roles
    ))


create_collection(fauna)
create_indexes(fauna)
seed_users(fauna)
create_roles(fauna)
