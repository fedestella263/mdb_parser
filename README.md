# MDBParser

Easy use Python library to read Microsoft Access (.mdb, .accdb) database files, this library use the mdb-tools command.

## Installing

Use pip:  `pip install mdb-parser`

Or install manually:
```
git clone https://github.com/fedestella263/mdb_parser
cd mdb_parser
python3 setup.py install
```

## Usage Example

```
from mdb_parser import MDBParser, MDBTable

db = MDBParser(file_path="db.accdb")

# Get and print the database tables
print(db.tables)

# Get a table from the DB.
table = db.get_table("MY_TABLE_NAME")

# Or you can use the MDBTable class.
table = MDBTable(file_path="db.accdb", table="MY_TABLE_NAME")

# Get and print the table columns.
print(table.columns)

# Iterate the table rows.
for row in table:
    print(row)
```