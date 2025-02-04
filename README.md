# SQLite DB Manager

A simple GUI application to create, open, and manage SQLite databases using Python and PyQt5.

## Features
- **Create Database:** Create new SQLite database files.
- **Open Database:** Open existing SQLite databases.
- **Table Management:**
  - View and load tables from the database.
  - Insert, edit, and delete rows in tables.
  - Create new tables with custom columns.
- **Real-Time Logging:** Track actions and errors in the log output.

## Technologies Used
- **Python 3**
- **SQLite** (via `sqlite3` module)
- **PyQt5** (for GUI components)

## Installation
1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies:**
   Make sure you have Python 3 installed. Then install PyQt5:
   ```bash
   pip install PyQt5
   ```

3. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage
1. **Create/Open Database:**
   - Enter a database name and click **"Create Database"** or click **"Open Database"** to load an existing one.

2. **Manage Tables:**
   - Select a table from the dropdown and click **"Load Table"**.
   - Double-click any cell to edit its value (auto-saves changes).
   - Click **"Insert Row"** to add a new row (default values are inserted).
   - Select a row and click **"Delete Row"** to remove it.

3. **Create New Table:**
   - Click **"Create Table"** and specify the table name and columns (e.g., `id INTEGER PRIMARY KEY, name TEXT`).

4. **Logs:**
   - Monitor the log section at the bottom for status updates and errors.

## Example
1. **Creating a Database:**
   - Enter `my_database` and click **"Create Database"**.
2. **Creating a Table:**
   - Click **"Create Table"**.
   - Enter `users` as the table name.
   - Enter `id INTEGER PRIMARY KEY, name TEXT, age INTEGER` as columns.
3. **Managing Data:**
   - Load the `users` table, insert rows, update cells, or delete rows.

## Contributing
Feel free to submit issues, fork the repository, and send pull requests to improve the app.

## License
This project is licensed under the MIT License.
