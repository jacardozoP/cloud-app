import os
import requests

SUPABASE_URL = "https://yuslpcidllsexfbncqpb.supabase.co"
SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SERVICE_ROLE_KEY:
    raise ValueError("Falta SUPABASE_SERVICE_ROLE_KEY")
BUCKET_NAME = "cloud-images"
DATASET_DIR = "dataset_original/train"

VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def upload_file(local_path, storage_path):
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{storage_path}"

    headers = {
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "apikey": SERVICE_ROLE_KEY,
        "Content-Type": "image/jpeg",
        "x-upsert": "true"
    }

    with open(local_path, "rb") as file:
        response = requests.post(url, headers=headers, data=file)

    if response.status_code not in (200, 201):
        print("Error subiendo:", local_path)
        print(response.status_code, response.text)
        return None

    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{storage_path}"


def insert_record(cloud_type, image_url):
    url = f"{SUPABASE_URL}/rest/v1/cloud_images"

    headers = {
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
        "apikey": SERVICE_ROLE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    data = {
        "cloud_type": cloud_type,
        "image_url": image_url
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code not in (200, 201):
        print("Error insertando registro:")
        print(response.status_code, response.text)


def main():
    for cloud_type in os.listdir(DATASET_DIR):
        class_dir = os.path.join(DATASET_DIR, cloud_type)

        if not os.path.isdir(class_dir):
            continue

        for filename in os.listdir(class_dir):
            if not filename.lower().endswith(VALID_EXTENSIONS):
                continue

            local_path = os.path.join(class_dir, filename)
            storage_path = f"{cloud_type}/{filename}"

            print(f"Subiendo {storage_path}...")

            public_url = upload_file(local_path, storage_path)

            if public_url:
                insert_record(cloud_type, public_url)

    print("Carga terminada.")


if __name__ == "__main__":
    main()