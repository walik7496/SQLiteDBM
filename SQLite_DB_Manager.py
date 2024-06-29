import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QLineEdit, QLabel, QMessageBox, QFileDialog, QTableWidget, QTableWidgetItem, QTextEdit, QComboBox, QInputDialog
)

class SQLiteManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.table_name = ""
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('SQLite DB Manager')
        self.setGeometry(100, 100, 800, 600)

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        
        self.dbNameLabel = QLabel('Database Name:')
        self.layout.addWidget(self.dbNameLabel)
        
        self.dbNameInput = QLineEdit(self)
        self.layout.addWidget(self.dbNameInput)
        
        self.createButton = QPushButton('Create Database', self)
        self.createButton.clicked.connect(self.create_db)
        self.layout.addWidget(self.createButton)
        
        self.openButton = QPushButton('Open Database', self)
        self.openButton.clicked.connect(self.open_db)
        self.layout.addWidget(self.openButton)
        
        self.tableNameLabel = QLabel('Select Table:')
        self.layout.addWidget(self.tableNameLabel)
        
        self.tableSelector = QComboBox(self)
        self.layout.addWidget(self.tableSelector)
        
        self.loadButton = QPushButton('Load Table', self)
        self.loadButton.clicked.connect(self.load_table)
        self.layout.addWidget(self.loadButton)
        
        self.resultTable = QTableWidget(self)
        self.resultTable.setEditTriggers(QTableWidget.DoubleClicked)
        self.resultTable.cellChanged.connect(self.cell_changed)
        self.layout.addWidget(self.resultTable)
        
        self.insertButton = QPushButton('Insert Row', self)
        self.insertButton.clicked.connect(self.insert_row)
        self.layout.addWidget(self.insertButton)
        
        self.deleteButton = QPushButton('Delete Row', self)
        self.deleteButton.clicked.connect(self.delete_row)
        self.layout.addWidget(self.deleteButton)
        
        self.createTableButton = QPushButton('Create Table', self)
        self.createTableButton.clicked.connect(self.create_table)
        self.layout.addWidget(self.createTableButton)
        
        self.logOutput = QTextEdit(self)
        self.logOutput.setReadOnly(True)
        self.layout.addWidget(self.logOutput)
        
    def log_message(self, message):
        self.logOutput.append(message)
        
    def create_db(self):
        db_name = self.dbNameInput.text().strip()
        if not db_name:
            QMessageBox.warning(self, 'Input Error', 'Please enter a database name.')
            return
        
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Database File", f"{db_name}.db", "SQLite Database Files (*.db);;All Files (*)", options=options)
        
        if file_path:
            try:
                conn = sqlite3.connect(file_path)
                conn.close()
                QMessageBox.information(self, 'Success', f'Database "{file_path}" created successfully.')
                self.log_message(f'Database "{file_path}" created successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error creating database: {str(e)}')
                self.log_message(f'Error creating database: {str(e)}')
        
    def open_db(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Database File", "", "SQLite Database Files (*.db);;All Files (*)", options=options)
        
        if file_path:
            try:
                self.connection = sqlite3.connect(file_path)
                self.log_message(f'Database "{file_path}" opened successfully.')
                QMessageBox.information(self, 'Success', f'Database "{file_path}" opened successfully.')
                self.load_table_names()
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error opening database: {str(e)}')
                self.log_message(f'Error opening database: {str(e)}')
    
    def load_table_names(self):
        if not self.connection:
            return
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            self.tableSelector.clear()
            for table in tables:
                self.tableSelector.addItem(table[0])
            self.log_message('Table names loaded successfully.')
        except Exception as e:
            self.log_message(f'Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))
    
    def load_table(self):
        if not self.connection:
            QMessageBox.warning(self, 'Connection Error', 'Please open a database first.')
            return
        
        self.table_name = self.tableSelector.currentText()
        if not self.table_name:
            QMessageBox.warning(self, 'Input Error', 'Please select a table.')
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            result = cursor.fetchall()
            
            self.resultTable.setColumnCount(len(cursor.description))
            self.resultTable.setRowCount(len(result))
            self.resultTable.setHorizontalHeaderLabels([desc[0] for desc in cursor.description])
            
            for row_idx, row_data in enumerate(result):
                for col_idx, col_data in enumerate(row_data):
                    self.resultTable.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            
            self.log_message(f'Table "{self.table_name}" loaded successfully.')
        except Exception as e:
            self.log_message(f'Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))
    
    def cell_changed(self, row, column):
        if not self.connection or not self.table_name:
            return
        
        item = self.resultTable.item(row, column)
        if item:
            new_value = item.text()
            column_name = self.resultTable.horizontalHeaderItem(column).text()
            primary_key_column = self.resultTable.horizontalHeaderItem(0).text()
            primary_key_value = self.resultTable.item(row, 0).text()
            
            update_query = f"UPDATE {self.table_name} SET {column_name} = ? WHERE {primary_key_column} = ?"
            
            try:
                cursor = self.connection.cursor()
                cursor.execute(update_query, (new_value, primary_key_value))
                self.connection.commit()
                self.log_message(f'Updated row {row + 1}, column "{column_name}" to "{new_value}"')
            except Exception as e:
                self.log_message(f'Error: {str(e)}')
                QMessageBox.critical(self, 'Error', str(e))
    
    def get_column_types(self):
        if not self.connection or not self.table_name:
            return []
        cursor = self.connection.cursor()
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = cursor.fetchall()
        return [(col[1], col[2]) for col in columns]
    
    def insert_row(self):
        if not self.connection or not self.table_name:
            return

        column_count = self.resultTable.columnCount()
        column_types = self.get_column_types()
        
        # Prepare values for the non-id columns
        values = []
        for column in column_types:
            column_name, column_type = column
            if column_name.lower() == 'id':
                continue  # Skip inserting id column
            if column_type.lower() in ['integer', 'int']:
                values.append(0)
            elif column_type.lower() in ['real', 'float', 'double']:
                values.append(0.0)
            else:
                values.append('')

        placeholders = ', '.join(['?'] * (column_count - 1))  # Exclude id column
        insert_query = f"INSERT INTO {self.table_name} VALUES (NULL, {placeholders})"

        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, values)
            self.connection.commit()
            self.log_message(f'Inserted new row into "{self.table_name}"')
            self.load_table()  # Refresh the table to show the new row
        except Exception as e:
            self.log_message(f'Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))

    def delete_row(self):
        if not self.connection or not self.table_name:
            return
        
        selected_items = self.resultTable.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Selection Error', 'Please select a row to delete.')
            return
        
        selected_row = selected_items[0].row()
        primary_key_column = self.resultTable.horizontalHeaderItem(0).text()
        primary_key_value = self.resultTable.item(selected_row, 0).text()
        
        delete_query = f"DELETE FROM {self.table_name} WHERE {primary_key_column} = ?"
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(delete_query, (primary_key_value,))
            self.connection.commit()
            self.log_message(f'Deleted row {selected_row + 1}')
            self.load_table()  # Refresh the table to remove the deleted row
        except Exception as e:
            self.log_message(f'Error: {str(e)}')
            QMessageBox.critical(self, 'Error', str(e))
    
    def create_table(self):
        if not self.connection:
            QMessageBox.warning(self, 'Connection Error', 'Please open a database first.')
            return
        
        table_name, ok = QInputDialog.getText(self, 'Table Name', 'Enter new table name:')
        if ok and table_name:
            columns, ok = QInputDialog.getText(self, 'Columns', 'Enter columns (e.g., id INTEGER PRIMARY KEY, name TEXT):')
            if ok and columns:
                create_table_query = f"CREATE TABLE {table_name} ({columns})"
                
                try:
                    cursor = self.connection.cursor()
                    cursor.execute(create_table_query)
                    self.connection.commit()
                    self.log_message(f'Table "{table_name}" created successfully.')
                    self.load_table_names()  # Refresh the table list to include the new table
                except Exception as e:
                    self.log_message(f'Error: {str(e)}')
                    QMessageBox.critical(self, 'Error', str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = SQLiteManager()
    manager.show()
    sys.exit(app.exec_())
