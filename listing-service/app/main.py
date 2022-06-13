from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import uvicorn

app = FastAPI(title="Listing service", description="This is the listing service. You can add/delete/get/update listings")

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


class Listing(HashModel):
    street: str
    number: int
    price: float
    city: str
    rented: str

    class Meta:
        database = redis


@app.get('/listings', tags=["Listing Service"], summary="Get all the listings in the database")
def all():
    return [format(pk) for pk in Listing.all_pks()]


def format(pk: str):
    listing = Listing.get(pk)

    return {
        'id': listing.pk,
        'street': listing.street,
        'number' : listing.number,
        'price': listing.price,
        'city': listing.city,
        'rented': listing.rented
    }


@app.post('/listings', tags=["Listing Service"], summary="Add a new listing in the database")
def create(listing: Listing):
    return listing.save()


@app.get('/listings/{pk}', tags=["Listing Service"], summary="Get a specific listing based on the primarykey")
def get(pk: str):
    return Listing.get(pk)


@app.delete('/listings/{pk}', tags=["Listing Service"], summary="Delete a specific listing based on the primarykey")
def delete(pk: str):
    return Listing.delete(pk)


@app.put('/listings/rented/{pk}', tags=["Listing Service"], summary="Update the renting status of a specific listing based on the primarykey")
def update(pk: str, status: str):
    listing = Listing.get(pk)
    listing.rented = status
    return listing.update()


@app.put('/listings/update/{pk}', tags=["Listing Service"], summary="Update a specific listing based on the primarykey")
def update(pk: str, listing: Listing):
    listing_to_update = Listing.get(pk)
    listing.pk = listing_to_update.pk
    return listing.update()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
