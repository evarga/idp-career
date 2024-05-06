import json
import argparse
import os
import requests

CLIENT_ID = os.environ["PORT_CLIENT_ID"]
CLIENT_SECRET = os.environ["PORT_CLIENT_SECRET"]
API_URL = 'https://api.getport.io/v1'
BLUEPRINTS_DIR = 'assets/blueprints'
# The list of blueprints in topologically sorted order.
BLUEPRINT_NAMES = ['pattern', 'technology', 'data_structure', 'method', 'problem', 'domain', 'problems_collection']
ENTITIES_DIR = 'assets/entities'
# The list of entities in topologically sorted order.
ENTITY_NAMES = [('cpp', 'technology'),
                ('hash_table', 'data_structure'),
                ('sliding_window', 'method'),
                ('leetcode_30', 'problem'),
                ('computer_science', 'domain'),
                ('demo_collection', 'problems_collection')]

credentials = {'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
token_response = requests.post(f'{API_URL}/auth/access_token', json=credentials)
access_token = token_response.json()['accessToken']
headers = {"Authorization": f"Bearer {access_token}"}


def create_blueprints():
    print("Creating blueprints...")
    for blueprint_name in BLUEPRINT_NAMES:
        with open(os.path.join(BLUEPRINTS_DIR, blueprint_name + '.json'), encoding='utf-8') as data_file:
            blueprint = json.load(data_file)
            response = requests.post(f"{API_URL}/blueprints", json=blueprint, headers=headers)
            if response.status_code != 200:
                print(f"Created blueprint {blueprint['title']} with identifier {blueprint['identifier']}.")
            else:
                print(f"Failed creating blueprint {blueprint['identifier']}, skipping")
                print(f"Error: {response.status_code}, {response.text}")


def create_sample_data():
    print("Creating sample data...")
    for entity_name, blueprint_id in ENTITY_NAMES:
        with open(os.path.join(ENTITIES_DIR, entity_name + '.json'), encoding='utf-8') as data_file:
            entity = json.load(data_file)
            response = requests.post(f"{API_URL}/blueprints/{blueprint_id}/entities?upsert=true&merge=true",
                                     json=entity,
                                     headers=headers)
            if response.status_code != 200:
                print(f"Created entity {entity['title']} with identifier {entity['identifier']}.")
            else:
                print(f"Failed creating entity {entity['identifier']}, skipping")
                print(f"Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--install-sample-data', action='store_true', help='Install also a sample software catalog.')
    args = parser.parse_args()

    create_blueprints()
    print("Completed creating the data model.")

    if args.install_sample_data:
        create_sample_data()
        print("Completed creating sample data.")
