import os
from dotenv import load_dotenv
from faunadb import query as q
from faunadb.client import FaunaClient

load_dotenv()
FAUNA_SERVER_SECRET = os.getenv("FAUNA_SERVER_SECRET")

fauna = FaunaClient(secret=FAUNA_SERVER_SECRET)


def get_users(secret):
    client = FaunaClient(secret=secret)
    data = client.query(q.map_(
        lambda ref: q.get(ref),
        q.paginate(q.documents(q.collection('users')))
    ))['data']
    return list(map(lambda user: user['data'], data))


def login(email, password):
    return fauna.query(
        q.login(q.match(q.index('user_by_email'), email),
                {"password": password})
    )


def logout(secret, status=False):
    client = FaunaClient(secret=secret)
    return client.query(
        q.logout(status)
    )


def signup(email, password):
    return fauna.query(
        q.create(
            q.collection("users"),
            {
                "credentials": {"password": password},
                "data": {
                    "email": email,
                    "type": "user"
                },
            }
        )
    )
