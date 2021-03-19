import csv
import subprocess

class MDBParser():
    """Class to read Microsoft Access database files

    Args:
        file_path (str): Route to database file
    """
    def __init__(self, file_path:str):
        self.__file_path = file_path
    
    @property
    def tables(self):
        """Returns the tables in the database

        Returns:
            (list): List with the table names
        """
        output = subprocess.check_output(f"mdb-tables {self.__file_path} -d '|'", shell=True).decode("utf-8")
        return output.strip(" \n|").split("|")
    
    def get_table(self, table:str):
        """Returns a MDBTable instance of the table

        Args:
            table (str): Name of the table
        
        Returns:
            (MDBTable): Instance of the class to manage the table
        """
        if table not in self.tables:
            raise Exception(f"Table {table} doesn't exists in the file {self.__file_path}")
        
        return MDBTable(self.__file_path, table)

class MDBTable():
    """Class to read a determinated table in the database file

    Args:
        file_path (str): Route to the database file
        table (str): Name of the table
    """
    def __init__(self, file_path:str, table:str):
        self.__file_path = file_path
        self.__table = table
    
    @property
    def columns(self):
        """Returns the columns of the table"""
        output = subprocess.check_output(f"mdb-export {self.__file_path} {self.__table} | head -1", shell=True).decode("utf-8")
        return output.strip().split(",")
    
    def __iter__(self):
        """Returns all data of the table without header"""
        output = subprocess.check_output(f"mdb-export {self.__file_path} {self.__table} -H", shell=True).decode("utf-8")
        return csv.reader(output.splitlines())

