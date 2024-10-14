# Test Web Platform for Machine Manufacturer (SILANT)

## Overview
This project is a test web platform for a machine manufacturer. The realized roles include:
- Managers
- Admins
- Unauthorized Users
- Clients
- Service Companies

The purpose is to enable the machine manufacturer to:
- Create machine instances
- Add clients
- Assign service companies
- Track warranty claims
- Track technical maintenance

Registration is only possible through the admins.

## Technologies Used
- **Framework**: Django
- **Front-end**: HTML, CSS, JavaScript

## Setup and Installation
1. **Clone the project** along with the test database.

2. **Navigate to the project directory.**

3. **Create a virtual environment.**
```sh
python -m venv venv
```
4. **Activate the virtual environment.**

```sh
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```
5. **Install the required packages.**

```sh
pip install -r requirements.txt
```
6. **Run the project and test its functionality.**

## Usage
If you wish to use the project under the MIT license, you are free to do so. For production usage, follow these steps:

1. **Delete the test database.**

2. **Run migrations to create a fresh database instance.**
```sh

python manage.py makemigrations
python manage.py migrate
```
3. **Create Roles and Permissions.**

Depending on the type of database, you should use the SQL queries from the starter_ki_permissions folder (adjust based on the database solution) to create instances of users with roles and relevant permissions. These are hardcoded in the project and cannot be modified freely without sufficiently updating the code.

Creation and maintenance of additional roles will require development work.

## License

This project is licensed under the MIT License.