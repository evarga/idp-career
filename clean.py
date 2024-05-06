import argparse
import os
import time

import requests

CLIENT_ID = os.environ["PORT_CLIENT_ID"]
CLIENT_SECRET = os.environ["PORT_CLIENT_SECRET"]
API_URL = 'https://api.getport.io/v1'
BLUEPRINTS_DIR = 'assets/blueprints'

credentials = {'clientId': CLIENT_ID, 'clientSecret': CLIENT_SECRET}
token_response = requests.post(f'{API_URL}/auth/access_token', json=credentials)
access_token = token_response.json()['accessToken']
headers = {"Authorization": f"Bearer {access_token}"}


def get_blueprint_names():
    blueprint_names = []
    for blueprint_file in os.listdir(BLUEPRINTS_DIR):
        if blueprint_file.endswith('.json'):
            name, _ = os.path.splitext(blueprint_file)
            blueprint_names.append(name)
    return blueprint_names


def delete_all_resources(should_delete_blueprints=False):
    if should_delete_blueprints:
        print("Deleting everything...")
    else:
        print("Deleting only entities...")

    pending = []
    for blueprint_id in get_blueprint_names():
        response = requests.delete(f"{API_URL}/blueprints/{blueprint_id}/all-entities"
                                   + f"?delete_blueprint={'true' if should_delete_blueprints else 'false'}",
                                   headers=headers)
        if response.status_code == 202:
            print(f"Started deletion of resources associated with blueprint {blueprint_id}...")
            pending.append(response.json()['migrationId'])
        else:
            print(f"Failed to delete resources associated with blueprint {blueprint_id}.")
            print(f"Error: {response.status_code}, {response.text}")

    time.sleep(5)
    while pending:
        migration_id = pending.pop()
        response = requests.get(f"{API_URL}/migrations/{migration_id}", headers=headers)
        if response.status_code == 200:
            status = response.json()['migration']['status']
            if status == 'COMPLETED':
                print(f"Deletion of resources associated with migration {migration_id} completed.")
            else:
                print(f"Waiting for deletion of resources associated with migration {migration_id} to complete...")
                pending.append(migration_id)
                time.sleep(2)
        else:
            print(f"Failed to get status of migration {migration_id}.")
            print(f"Error: {response.status_code}, {response.text}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--retain-data-model', action='store_true', help='Retain the data model.')
    args = parser.parse_args()

    delete_all_resources(not args.retain_data_model)
    print("Completed deleting resources.")
