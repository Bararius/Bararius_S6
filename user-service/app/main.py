from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redis_om import get_redis_connection, HashModel
import uvicorn
import requests
import pika

app = FastAPI(title="User service", description="This is the user service. You can add/delete/get/update users")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-12840.c56.east-us.azure.cloud.redislabs.com",
    port=12840,
    password="sxsXIYXuBJ0MfHCzjSIHEpetTA7ohjRM",
    decode_responses=True
)

class User(HashModel):
    googleId: int
    fName: str
    lName: str
    email: str
    password: str

    class Meta:
        database = redis

class UserGoogle(HashModel):
    googleId: int
    givenName: str
    familyName: str
    email: str

    class Meta:
        database = redis

class GoogleData(BaseModel):
    email: str
    familyName: str
    givenName: str
    googleId: str
    imageUrl: str
    name: str


@app.get('/users', tags=["User Service"], summary="Get all the users in the database")
def all():
    return [format(pk) for pk in User.all_pks()]

@app.get('/users/goauth', tags=["User Service"], summary="Get all the users registered in the database via google")
def all():
    return [formatGoauth(pk) for pk in UserGoogle.all_pks()]

@app.post('/login-verify', tags=["Google Verification OAuth"], summary="This is an endpoint where we check the token from the google log in")
async def google_login(data : Request):
    # print(data)
    # received_data = jsonable_encoder(data)
    received_data = await data.json()
    token = received_data[0]
    google_login_data = received_data[1]

    oauth_url = 'https://oauth2.googleapis.com/tokeninfo'
    token_obj = {'access_token': token}

    oauth_request = requests.post(oauth_url, data=token_obj)

    if(oauth_request.status_code == 200):
        # add_user(received_data[1])
        print('success')
        return('success')
    else:
        print('declined')
        return('declined')


def formatGoauth(pk: str):
    user = UserGoogle.get(pk)

    return {
        'id': user.pk,
        'googleId': user.googleId,
        'fName' : user.givenName,
        'lName': user.familyName,
        'email': user.email
    }

def format(pk: str):
    user = User.get(pk)

    return {
        'id': user.pk,
        'googleId': user.googleId,
        'fName' : user.fName,
        'lName': user.lName,
        'email': user.email,
        'password': user.password
    }


@app.post('/users', tags=["User Service"], summary="Add a new user in the database")
def create(user: User):
    return user.save()

@app.post('/users/goauth', tags=["User Service"], summary="Add a new user in the database via google oauth")
def create(user: UserGoogle):
    return user.save()


# @app.get('/listings/{pk}', tags=["Listing Service"], summary="Get a specific listing based on the primarykey")
# def get(pk: str):
#     return Listing.get(pk)


@app.delete('/users/{pk}', tags=["USer Service"], summary="Delete a specific user based on the primarykey")
def delete(pk: str):
    return User.delete(pk)


# @app.put('/listings/rented/{pk}', tags=["Listing Service"], summary="Update the renting status of a specific listing based on the primarykey")
# def update(pk: str, status: str):
#     listing = Listing.get(pk)
#     listing.rented = status
#     return listing.update()


# @app.put('/listings/update/{pk}', tags=["Listing Service"], summary="Update a specific listing based on the primarykey")
# def update(pk: str, listing: Listing):
#     listing_to_update = Listing.get(pk)
#     listing.pk = listing_to_update.pk
#     return listing.update()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
