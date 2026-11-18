# Flask Data Entry Application Demo

This Flask application demonstrates how to create web forms that allow users to add new data to a database. It's designed to show students the fundamentals of data entry in web applications.

## What this app demonstrates

- **GET requests**: Displaying forms to users
- **POST requests**: Processing form submissions
- **Form validation**: Checking user input before saving
- **Database INSERT operations**: Adding new records to the database
- **Flash messages**: Providing user feedback
- **Redirects**: Sending users to different pages after actions
- **Foreign key relationships**: Linking venues to cities

## Setup (do this once)

A virtual environment is a folder that holds this project's own copy of Python and its packages, so the Flask version here doesn't clash with anything else on your computer. You'll create one inside this folder.

1. Open a terminal and move into this folder (`13-Flask/DataEntryExample` in the class repository):
   ```bash
   cd 13-Flask/DataEntryExample
   ```

2. Create a virtual environment named `.venv`:
   ```bash
   python3 -m venv .venv
   ```
   On Windows, use `python -m venv .venv`.

3. Activate it:
   ```bash
   source .venv/bin/activate
   ```
   On Windows, use `.venv\Scripts\activate`. Your terminal prompt should now start with `(.venv)`.

4. Install Flask into the virtual environment:
   ```bash
   pip install -r requirements.txt
   ```

## How to run the app

1. Open a terminal in this folder and activate the virtual environment if your prompt doesn't already start with `(.venv)`:
   ```bash
   source .venv/bin/activate
   ```

2. Run the application from inside this folder:
   ```bash
   python app.py
   ```
   While the environment is active, `python` and `pip` use the copies in `.venv`.

3. Open your web browser and go to:
   ```
   http://localhost:5002
   ```

4. When you're finished, stop the server with `Ctrl+C` and leave the virtual environment:
   ```bash
   deactivate
   ```

This app runs on port 5002, so you can run it at the same time as `BasicExample` (port 5001) in a second terminal.

**Adding a venue changes `sc_gay_guides.db` in this folder.** If you want to be able to undo your test entries, make a copy of the database before you start:
```bash
cp sc_gay_guides.db sc_gay_guides_backup.db
```

## If something goes wrong

- **`no such table: venues`** (or `no such table: cities`): you started the app from a different folder. The app looks for `sc_gay_guides.db` in whatever folder your terminal is in, and SQLite quietly creates an empty file with that name when it can't find one. Delete the empty `sc_gay_guides.db` it made, `cd` into `DataEntryExample`, and run `python app.py` again.
- **`ModuleNotFoundError: No module named 'flask'`**: the virtual environment isn't active. Run `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) and try again.
- **`Address already in use`**: another app is already using port 5002, often a copy of this one in another terminal. Stop it with `Ctrl+C`.

## What you can do

### View Venues
- See a list of all venues in the database
- Click "View Details" to see full information for any venue

### Add New Venues
- Click "Add New Venue" button
- Fill out the form with venue information:
  - **Title** (required): Name of the venue
  - **Description**: Details about the venue
  - **Type**: Category (Nightclub, Bar, Restaurant, etc.)
  - **Street Address**: Physical address
  - **City** (required): Select from existing cities
  - **Year**: When the venue was established
- Submit the form to add the venue to the database

## Key Flask concepts demonstrated

### Routes with Multiple Methods
```python
@app.route('/add_venue', methods=['GET', 'POST'])
def add_venue():
    if request.method == 'POST':
        # Handle form submission
    else:
        # Display the form
```

### Form Data Handling
```python
title = request.form.get('title', '').strip()
city_id = request.form.get('city_id', '').strip()
```

### Database INSERT Operations
```python
conn.execute('''
    INSERT INTO venues (title, description, type, street_address, city_id, year)
    VALUES (?, ?, ?, ?, ?, ?)
''', (title, description, venue_type, street_address, city_id, year))
```

### User Feedback
```python
flash(f'Successfully added venue: {title}', 'success')
```

### Redirects
```python
return redirect(url_for('index'))
```

## Database Structure

The app works with two main tables:
- **venues**: Contains venue information (title, description, type, address, etc.)
- **cities**: Contains city information (city_name, state)

Venues are linked to cities through a foreign key relationship (`city_id`).

## Educational Value

This example shows students:
1. How web forms work in Flask
2. The difference between GET and POST requests
3. How to validate user input
4. How to insert data into databases
5. How to provide user feedback
6. How to handle errors gracefully
7. How to use redirects to improve user experience

Perfect for understanding the basics of data entry in web applications!
