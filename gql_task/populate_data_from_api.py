import os
import django
import json
import time
import re
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import urlopen
from django.db import IntegrityError

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gql_task.settings')
django.setup()

from mil_records.models import UserRecord

def normalize_email(email):
    """Normalize the email by converting it to lowercase and removing any variations."""
    normalized_email = email.lower().strip()
    normalized_email = re.sub(r'\+.*@', '@', normalized_email)
    return normalized_email

def fetch_user_data(batch_size):
    """Fetch user data from the API."""
    url = f'https://randomuser.me/api/?results={batch_size}'
    retries = 5
    delay = 1  # Initial delay in seconds

    while retries > 0:
        try:
            with urlopen(url) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8')).get('results')
                    if data is None:
                        raise Exception("No results found in API response")
                    return data
                else:
                    raise Exception(f"API request failed with status code {response.status}")
        except HTTPError as e:
            if e.code == 429:  # Too Many Requests
                print(f"Rate limit exceeded. Retrying in {delay} seconds...")
                time.sleep(delay)
                retries -= 1
                delay += 1  # Increase delay for next retry
            else:
                raise e  # Re-raise other HTTP errors
        except Exception as e:
            print(f"Error fetching user data: {e}")
            retries -= 1
            time.sleep(delay)
            delay += 1  # Increase delay for next retry

    raise Exception("Failed to fetch user data after multiple retries")

def create_user_records(data):
    """Create user records from the fetched data."""
    records = []
    for user in data:
        name = f"{user['name']['first']} {user['name']['last']}"
        email = normalize_email(user['email'])
        age = user['dob']['age']
        created_at = datetime.strptime(user['registered']['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        record = UserRecord(name=name, email=email, age=age, created_at=created_at)
        records.append(record)
    return records

def main():
    batch_size = 1500  # Number of records to fetch per API call
    total_records = 100000000  # Total number of records to insert
    inserted_records = 0
    successful_emails = set()

    while inserted_records < total_records:
        try:
            data = fetch_user_data(batch_size)
            records = create_user_records(data)
            new_records = [record for record in records if record.email not in successful_emails]

            if not new_records:
                print("All records are already inserted. Exiting...")
                break

            UserRecord.objects.bulk_create(new_records, ignore_conflicts=True)
            inserted_records += len(new_records)
            successful_emails.update(record.email for record in new_records)
            print(f'Inserted {inserted_records} records')
        except IntegrityError as e:
            print(f"Skipped duplicate email: {e}")
            continue
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == '__main__':
    main()
