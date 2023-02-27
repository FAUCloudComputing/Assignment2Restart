from google.cloud import datastore, storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".\\keyfile.json"

datastore_client = datastore.Client()
storage_client = storage.Client()

bucket_name = "main-bucket-for-my-first-project"


def list_db_entries():
    query = datastore_client.query(kind="images")

    for image in query.fetch():
        print(image.items())


def add_db_entry(image_data):
    size = len(image_data)

    print(f"Size: {size}")

    entity = datastore.Entity(key=datastore_client.key("images"))
    entity.update({
        'Filename': 'image2.jpg',
        'Size': size
    })

    datastore_client.put(entity)


def upload_file(blob_name, file):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    print("made bucket and blob")
    print(file)

    blob.upload_from_file(file)

    print("uploaded")

    return


list_db_entries()