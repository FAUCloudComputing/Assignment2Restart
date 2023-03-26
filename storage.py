from google.cloud import datastore, storage
from google.oauth2 import service_account
import os


# Set the environment variable for the service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account.Credentials.from_service_account_info("cicd-service-account@vernal-landing-376714.iam.gserviceaccount.com")

datastore_client = datastore.Client()
storage_client = storage.Client()

bucket_name = "main-bucket-for-my-first-project"


def list_db_entries(user_id):
    # Create a query to fetch all images for the given user ID
    query = datastore_client.query(kind='images')
    query.add_filter('Owner', '=', user_id)

    # Iterate through the query results and append each image to a list
    images = []
    for image in query.fetch():
        images.append(image)

    # Return the list of images
    return images


def add_db_entry(user_id, image_name, image_size):
    # Calculate the length of the image name
    size = len(image_name)

    # Create a new entity with the given properties
    entity = datastore.Entity(key=datastore_client.key("images"))
    entity.update({
        'Name': image_name,
        'Owner': user_id,
        'Size': image_size
    })

    # Store the entity in the Datastore
    datastore_client.put(entity)


def upload_file(user_id, blob_name, file):
    # Get the bucket and blob for the given user ID and blob name
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{user_id}/{blob_name}")

    # If the user's blob directory doesn't exist, create it
    if not bucket.blob(f"{user_id}").exists():
        sub_blob = bucket.blob(f"{user_id}")
        sub_blob.create_resumable_upload_session()

    # Reset the file read pointer to the beginning of the file
    file.seek(0)

    # Upload the file to the blob
    blob.upload_from_file(file)

    # Return
    return


def download_file(user_id, blob_name):
    # Get the bucket and blob for the given user ID and blob name
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(f"{user_id}/{blob_name}")

    # Download the file from the blob as bytes
    image_data = blob.download_as_bytes()

    # Return the image data
    return image_data

