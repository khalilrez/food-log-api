# Food Log API

This is a simple API that allows users to log their food entries and track their daily caloric intake. The API supports creating, updating, and deleting food entries, as well as retrieving a user's food log and displaying it in an HTML format.

## Features

- Create a new food entry with the user's information, food details, and number of servings.
- Check the user's daily caloric allowance and prevent overeating by validating the total calories consumed.
- Retrieve a user's food log entries for a specific day and display them in an HTML table.
- Update an existing food entry with new information.
- Delete a food entry from the log.
- Manage food items by creating, updating, and deleting food details.
- Secure the API endpoints using JWT authentication.

## Endpoints

Food Entry Endpoints:
- `POST /`: Create a new food entry.
- `GET /users/{user_id}`: Retrieve a user's food entries.
- `GET /{username}`: Retrieve a user's food log and display it in an HTML format.
- `PUT /{entry_id}`: Update an existing food entry.
- `DELETE /{entry_id}`: Delete a food entry.

Food Endpoints:
- `POST /food`: Create a new food item.
- `GET /food/all`: Retrieve all food items.
- `GET /food/{food_id}`: Retrieve a specific food item.
- `PUT /food/{food_id}`: Update an existing food item.
- `DELETE /food/{food_id}`: Delete a food item.

Authentication Endpoints:
- `POST /token`: Get an access token by providing the username and password.

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. When a user successfully logs in by providing their username and password, they receive an access token. This token needs to be included in the `Authorization` header of subsequent requests to access the authenticated endpoints. The access token is valid for a certain duration (30 minutes in this case) and must be refreshed to continue accessing the protected endpoints.


## Data Models

- `User`: Represents a user with an ID, username, password, and maximum daily caloric allowance.
- `Food`: Represents a type of food with a name, calories per serving, and serving size.
- `FoodEntry`: Represents a logged food entry with an ID, user information, food details, date added, number of servings, and total calories.

## Technologies Used

- FastAPI: A modern, fast (high-performance), web framework for building APIs with Python.
- Pydantic: A data validation and parsing library used for data models.
- Passlib: A password hashing library used for securely hashing user passwords.
- Starlette: A lightweight ASGI framework used for handling HTTP requests and responses.
- JWT: JSON Web Tokens used for authentication and authorization.


## Setup and Installation

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the API server using `uvicorn main:app --reload`.
4. Access the API endpoints using a web client or an API testing tool (e.g., curl, Postman).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
