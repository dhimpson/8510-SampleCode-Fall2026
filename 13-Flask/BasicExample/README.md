# Simple Flask App Demo

This is a very simple Flask application that demonstrates basic web development concepts using the SC Gay Guides database.

## What this app does

- Displays a list of venues from the `sc_gay_guides.db` database
- Shows full details for one venue at `/venue/<id>` (for example, `http://localhost:5001/venue/1`)
- Lists every city in the database at `/cities`
- Demonstrates Flask routing, templates, and database connections

## Setup (do this once)

A virtual environment is a folder that holds this project's own copy of Python and its packages, so the Flask version here doesn't clash with anything else on your computer. You'll create one inside this folder.

1. Open a terminal and move into this folder (`13-Flask/BasicExample` in the class repository):
   ```bash
   cd 13-Flask/BasicExample
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
   http://localhost:5001
   ```

4. When you're finished, stop the server with `Ctrl+C` and leave the virtual environment:
   ```bash
   deactivate
   ```

## If something goes wrong

- **`no such table: venues`**: you started the app from a different folder. The app looks for `sc_gay_guides.db` in whatever folder your terminal is in, and SQLite quietly creates an empty file with that name when it can't find one. Delete the empty `sc_gay_guides.db` it made, `cd` into `BasicExample`, and run `python app.py` again.
- **`ModuleNotFoundError: No module named 'flask'`**: the virtual environment isn't active. Run `source .venv/bin/activate` (Windows: `.venv\Scripts\activate`) and try again.
- **`Address already in use`**: another app is already using port 5001, often a copy of this one in another terminal. Stop it with `Ctrl+C`.

## What you'll see

- A list of 10 venues from the database
- Each venue shows title, description, address, location, year, and type
- Clean, simple styling to make it easy to read

## Key Flask concepts demonstrated

- **Routes**: `/` (home page), `/venue/<id>` (venue details) and `/cities` (list of cities)
- **Templates**: HTML templates with Jinja2 templating
- **Database connections**: SQLite3 integration
- **Template inheritance**: Base template with child templates
- **Error handling**: 404 error for non-existent venues

This is a great starting point for understanding how Flask works!
