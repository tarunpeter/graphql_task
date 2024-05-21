# Django GraphQL API

This project is a Django-based GraphQL API for managing user records.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/tarunpeter/graphql_task.git
   cd graphql_task

2. Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3.Install the requirements:
pip install -r requirements.txt

4.Apply database migrations:
python manage.py makemigrations
python manage.py migrate

5.Create a superuser (optional but recommended):
python manage.py createsuperuser

6.Run the development server:
python manage.py runserver
Open your web browser and go to http://127.0.0.1:8000/admin
Log in to the django administration interface.


# Django GraphQL API

This project is a Django-based GraphQL API for managing user records.

GraphQL Queries and Mutations
Queries
1. Home

query {
  home
}
2. List User Records

query {
  listUserRecords {
    id
    name
    email
    age
    createdAt
  }
}
3. List Logged-in Users

query {
  listLoggedinUsers {
    id
    username
  }
}
4. Me Query

query {
  me {
    id
    username
  }
}
Mutations
1. Create User Record

mutation CreateUserRecord($input: UserRecordInput!) {
  createUserRecord(input: $input) {
    userRecord {
      id
      name
      email
      age
    }
  }
}
2. Update User Record

mutation UpdateUserRecord($id: Int!, $input: UserRecordInput!) {
  updateUserRecord(id: $id, input: $input) {
    userRecord {
      id
      name
      email
      age
    }
  }
}
3. Delete User Record

mutation DeleteUserRecord($ids: [ID!]!) {
  deleteUserRecord(ids: $ids) {
    userRecord {
      id
      name
      email
      age
    }
  }
}
4. Token Authentication

mutation {
  tokenAuth(username: "admin", password: "admin") {
    token
  }
}
Executing Queries and Mutations
Navigate to the GraphQL endpoint:

Open your web browser and go to http://127.0.0.1:8000/graphql. You should see the GraphiQL interface where you can run the queries and mutations.

Run Queries and Mutations:

Copy the desired query or mutation from above.
Paste it into the GraphiQL interface.
If a query or mutation requires variables (like CreateUserRecord or UpdateUserRecord), click on the "Query Variables" pane at the bottom of GraphiQL and provide the necessary JSON.

Example for CreateUserRecord:


mutation CreateUserRecord($input: UserRecordInput!) {
  createUserRecord(input: $input) {
    userRecord {
      id
      name
      email
      age
    }
  }
}

Variables:

{
  "input": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }
}

Example for UpdateUserRecord:

mutation UpdateUserRecord($id: Int!, $input: UserRecordInput!) {
  updateUserRecord(id: $id, input: $input) {
    userRecord {
      id
      name
      email
      age
    }
  }
}

Variables:

{
  "id":1,
  "input": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "age": 30
  }
}

Example for DeleteUserRecord:

mutation DeleteUserRecord($ids: [ID!]!) {
  deleteUserRecord(ids: $ids) {
    userRecord {
      id
      name
      email
      age
    }
  }
}

Variables:

  "ids":[50,60] 
