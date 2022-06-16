from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
import uvicorn
import pika

app = FastAPI(title="Subscription service", description="This is the subscription service. You can add/delete subscription")

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

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

def callback(ch, method, properties, body):
    print("Forget: " + str(body))
    Subscription.detele(body)

channel.basic_consume(
    queue='forgetme', on_message_callback=callback, auto_ack=True)

channel.start_consuming()

class Subscription(HashModel):
    email: str
    listing_id: int

    class Meta:
        database = redis


@app.get('/listings', tags=["Listing Service"], summary="Get all the listings in the database")
def all():
    return [format(pk) for pk in Subscription.all_pks()]


def format(pk: str):
    listing = Subscription.get(pk)

    return {
        'id': listing.pk,
        'email': listing.email,
        'listing_id' : listing.listing_id,
    }


@app.post('/subscriptions', tags=["Subscription Service"], summary="Add a new subscription in the database")
def create(subscription: Subscription):
    return subscription.save()


# @app.get('/listings/{pk}', tags=["Listing Service"], summary="Get a specific listing based on the primarykey")
# def get(pk: str):
#     return Listing.get(pk)


@app.delete('/subscriptions/{email}/{listing_id}', tags=["Subscription Service"], summary="Delete a specific subscription based on the email")
def delete(email: str, listing_id: str):
    return Subscription.delete(email, listing_id)

@app.delete('/subscriptions/forget-me/{email}', tags=["Subscription Service"], summary="Delete all information based on the email")
def delete(email: str):
    channel.queue_declare(queue='forgetme')
    channel.basic_publish(exchange='',
                        routing_key='hello',
                        body=str(email))

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
