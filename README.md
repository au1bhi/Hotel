# MIS-300-90-G1-Hotel Management System

This project is a hotel management system built using Flask (a Python web framework) and MySQL for database management. It provides a simple interface to manage rooms, customers, reservations, and services.

## Project Structure

The project has the following structure:

-   `app.py`: The main application file containing Flask routes and logic.
-   `establish.sql`: SQL script to create the necessary database tables.
-   `GenerateSampleData.py`: Python script to generate sample data for the database.
-   `templates/`: Directory containing HTML templates for the web interface.
    -   `index.html`: Home Page.
    -   `rooms.html`: Rooms Management Page.
    -   `customers.html`: Customers Management Page.
    -   `reservations.html`: Reservations Management Page.
    -   `services.html`: Services Management Page.
    -   `members.html`: Members Management Page.
    -   `transactions.html`: Transactions Management Page.
    -   `edit_rooms.html`: Edit Room Page.
    -   `edit_customers.html`: Edit Customer Page.
    -   `edit_reservations.html`: Edit Reservation Page.
    -   `edit_services.html`: Edit Service Page.
    -   `edit_members.html`: Edit Member Page.
    -   `edit_transactions.html`: Edit Transaction Page.
    -   `terminal.html`: SQL Terminal Page (Disabled due to security concerns).
-   `hotel.log`: Log file for error logging.
-   `README.md`: This file, providing a project overview.

## Setup Instructions

1.  **Install Dependencies:**

    ```bash
    pip install Flask Flask-MySQLdb Faker
    ```

2.  **Create Database:**

    Run the `establish.sql` script to create the necessary tables in your MySQL database.

3.  **Configuration:**

    Modify the database configuration in `app.py` to match your MySQL settings.

4.  **Run the Application:**

    ```bash
    python app.py
    ```

## Usage

The application provides the following functionalities:

-   **Rooms Management:** Add, delete, and view rooms.
-   **Customers Management:** Add, delete, and view customers.
-   **Reservations Management:** Add, delete, and view reservations.
-   **Services Management:** Add, delete, and view services.
-   **Members Management:** Add, delete, and view members.
-   **Transactions Management:** Add, delete, and view transactions.
-   **Search:** Search across all tables.

## Parameterized Queries

To prevent SQL injection vulnerabilities, the application uses parameterized queries. Instead of directly embedding user input into SQL queries, data is passed as parameters. This ensures that the database treats the input as data, not as executable code.

Example:

```python
cur.execute("SELECT * FROM Rooms WHERE RoomID LIKE %s OR RoomType LIKE %s OR Status LIKE %s", 
            ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
```


## Error Logging

The application logs errors to the `hotel.log` file.

## Sample Data Generation

The `GenerateSampleData.py` script can be used to generate sample data for testing. Run the script using the following command:

```bash
python GenerateSampleData.py
```
