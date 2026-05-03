import requests
import config


_quiz_web_cache = None


def load_quiz_web_dataset():
    global _quiz_web_cache

    if _quiz_web_cache is not None:
        return _quiz_web_cache

    url = f"{config.SUPABASE_URL}/rest/v1/cloud_images"

    headers = {
        "apikey": config.SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {config.SUPABASE_ANON_KEY}"
    }

    params = {
        "select": "cloud_type,image_url"
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    rows = response.json()

    dataset = {}

    for row in rows:
        cloud_type = row["cloud_type"]
        image_url = row["image_url"]

        if cloud_type not in dataset:
            dataset[cloud_type] = []

        dataset[cloud_type].append(image_url)

    _quiz_web_cache = dataset
    return dataset


def get_quiz_classes():
    dataset = load_quiz_web_dataset()
    return list(dataset.keys())


def get_quiz_images(cloud_type):
    dataset = load_quiz_web_dataset()
    return dataset.get(cloud_type, [])