import subprocess

COL_DELIMITER = "@@@"
ROW_DELIMITER = "###\n"

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
        header (bool): Flag to show the header
    """
    def __init__(self, file_path:str, table:str, header:bool=True):
        self.__file_path = file_path
        self.__table = table
        self.__header = header
        self.__process = None
        self.__command = f"mdb-export {self.__file_path} {self.__table} -d '{COL_DELIMITER}' -R '{ROW_DELIMITER}'"
    
    @property
    def columns(self):
        """Returns the columns of the table"""
        output = subprocess.check_output(f"{self.__command} | head -1", shell=True).decode("utf-8")
        return output[:-len(ROW_DELIMITER)].split(COL_DELIMITER)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.__process is None:
            self.__process = subprocess.Popen(
                self.__command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                shell=True
            )

            # Skip the header.
            if not self.__header:
                self.__process.stdout.readline()
        
        line = self.__process.stdout.readline()
        if line == "":
            self.__process = None
            raise StopIteration
        
        row = line.split(COL_DELIMITER)
        
        # Concat splited rows.
        while not row[-1].endswith(ROW_DELIMITER):
            new_row = self.__process.stdout.readline().split(COL_DELIMITER)
            row[-1] += new_row[0]
            row += new_row[1:]

        # Remove row delimiter and quotes.
        row[-1] = row[-1][:-len(ROW_DELIMITER)]
        for idx in range(len(row)):
            row[idx] = row[idx].strip('"')
        
        return row

