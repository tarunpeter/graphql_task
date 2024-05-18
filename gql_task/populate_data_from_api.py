import os
from urllib.error import HTTPError
import django
import json
from urllib.request import urlopen
from datetime import datetime
from django.db import IntegrityError
import time
import re
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gql_task.settings')
django.setup()

def normalize_email(email):
    # Convert the email to lowercase and remove any whitespace
    normalized_email = email.lower().strip()
    # Remove any characters after '+' in the email (for email variations)
    normalized_email = re.sub(r'\+.*@', '@', normalized_email)
    return normalized_email

from mil_records.models import UserRecord

def fetch_user_data(batch_size):
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


fake = Faker()

def create_user_records(data):
    records = []
    for user in data:
        name = fake.name()
        email = fake.email()
        age = user['dob']['age']
        record = UserRecord(name=name, email=email, age=age)
        records.append(record)
    return records

def main():
    batch_size = 100  # Number of records to fetch per API call
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
            UserRecord.objects.bulk_create(new_records)
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
