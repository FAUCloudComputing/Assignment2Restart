from google.cloud import datastore, storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './keyfile.json'

datastore_client = datastore.Client()
storage_client = storage.Client()

bucket_name = "main-bucket-for-my-first-project"


def list_db_entries():
    query = datastore_client.query(kind="images")

    images = []
    for image in query.fetch():
        images.append(image)

    return images


def add_db_entry(image_name, image_size):
    size = len(image_name)

    entity = datastore.Entity(key=datastore_client.key("images"))
    entity.update({
        'Name': image_name,
        # 'Owner': user,
        'Size': image_size
    })

    datastore_client.put(entity)


def upload_file(blob_name, file):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    file.seek(0)

    print("made bucket and blob")
    print(file)

    blob.upload_from_file(file)

    print("uploaded")

    return

# def download_file(blob_name, file):
#     bucket = storage_client.bucket(bucket_name)
#
#     blob = bucket.blob(blob_name)
#     blob.download_to_file(file)
#     blob.reload()
#
#     print(f"Blob: {blob.name}")
#     print(f"Bucket: {blob.bucket.name}")
#     print(f"Size: {blob.size}")
#     print(f"Public URL: {blob.public.url}")
#
#     return

# list_db_entries()
