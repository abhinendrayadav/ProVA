from google.cloud import storage

storage_client = storage.Client()

buckets = list(storage_client.list_buckets())

print(buckets)