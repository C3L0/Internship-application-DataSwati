###Importation of the Libraries
##FastApi to create the Api object - HTTPExecption to haddle the error
from fastapi import FastAPI, HTTPException
##mysql.connector to connect the Api to the MySQL database
import mysql.connector
from mysql.connector import errorcode
##pydantic to define the data model
from pydantic import BaseModel
##Pandas datetime os to manipulate the data
import pandas as pd
from datetime import date
import os

###Setup of the environment
#Creation of the Api object
app = FastAPI()
##Set the database configuration
config = {
    'user': 'root',
    'password': '',
    #'host': '127.0.0.1', 
    'host': 'host.docker.internal',
    #'host': 'mysql-container',
    #'host': 'db',
    'database': 'dataswati_test',
    'raise_on_warnings': True
}
##Setup Pydantic models
class sales(BaseModel):
    ID: int
    Date: str  #date
    Produit: str 
    Prix: int
    Quantite: int
    Categorie: str
    Vendeur: int
    Remise: float 
    PrixReel: float

class employees(BaseModel):
    ID: int
    Nom: str
    Equipe: str
##Execute a first connection to the database to make sure there is no problem between the API and the database
try:
    #we create the connexion
    connexion = mysql.connector.connect(**config)
except mysql.connector.Error as err:
    #if the login information are not good
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("'user' or 'password' uncorrect")
    #if the database doesn't exist
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("'database' doesn't exist")
    #otherwise we return the error
    else:
        print(err)
    #impossible connexion we exit the code
    exit()
#We close the connexion
connexion.close()


###Queries
##Root query
@app.get("/")  #@app refers to the api object, .get defines a GET route for the root URL ("/").
def root():
    return{"Micorsoft": "Word"}

##Get Employee
@app.get("/employees/{employee_id}", response_model = employees)
def get_employee(employee_id: int):
    """This function  take in parameter an employee ID
    
    It returns all the characteristic of the corresponding employee"""
    try:
        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor(dictionary=True)#create a cursor object, 'dictionary=True' is use to return a dictionary
        cursor.execute("SELECT * FROM employees WHERE ID = %s", (employee_id,))#executes an SQL query that selects all columns from the "employees" table where the "ID" matches the given employee_id
        employee = cursor.fetchone()#fetches the first row of the query result
        connexion.close()
        
        if employee is None:
            raise HTTPException(status_code=404, detail="sale not found")
        
        return employee

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Database error: " + str(err))
    
##Get Sale
@app.get("/sales/{sale_id}", response_model=sales)
def get_sale(sale_id: int):
    """This function  take in parameter a sale ID
    
    It returns all the characteristic of the corresponding sale"""
    try:
        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sales WHERE ID = %s", (sale_id,))#executes an SQL query that selects all columns from the "sales" table where the "ID" matches the provided sale_id
        sale = cursor.fetchone()
        connexion.close()
        
        if sale is None:
            raise HTTPException(status_code=404, detail="sale not found")
        
        return sale

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Database error: " + str(err))

##Get the sales from a category
@app.get("/sales_categorie/{sale_categorie}")
def get_sale_per_categorie(sale_categorie: str, selected_columns: str = '*'):
    """This function  take in parameter a sale category and it also
    take the columns that you want in output. If you don't precise any
    you get all of them.
    
    It returns the characteristic selectioned of the corresponding sale"""
    try:
        if selected_columns != '*':#if the user has specified specific columns
            columns = [column.strip() for column in selected_columns.split(',')]#split the input string by commas, remove any extra spaces around the column names, and store them in a list
            columns_str = ', '.join(columns)#join the list of columns into a string separated by commas
        else:
            columns_str = selected_columns#columns_str = *

        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor(dictionary=True)
        query = f"SELECT {columns_str} FROM sales WHERE Categorie = %s"#create a query that return the specific columns of sales where is category fits with the parameter
        cursor.execute(query, (sale_categorie,))
        sale = cursor.fetchall()
        connexion.close()
        
        if not sale:
            raise HTTPException(status_code=404, detail="Sale not found")
        
        return sale

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Database error: " + str(err))
    

@app.get("/sales_in_date_range")
def sales_in_date_range(start_date: str, end_date: str, selected_columns: str = '*'):
    """This function  take in parameter a start date and a end date and it also
    take the columns that you want in output. If you don't precise any
    you get all of them.
    
    It returns the characteristic selectioned of the corresponding sale between the 
    date you choose"""
    try:
        if selected_columns != '*':
            columns = [column.strip() for column in selected_columns.split(',')]
            columns_str = ', '.join(columns)
        else:
            columns_str = selected_columns
        start_date_obj = date.fromisoformat(start_date)#put the date to the right format to manpulate them
        end_date_obj = date.fromisoformat(end_date)

        if start_date_obj > end_date_obj:#check the continuity of the date
            raise HTTPException(status_code=400, detail="Start date must be before the end date")

        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor(dictionary=True)
        query = f"""
            SELECT {columns_str} 
            FROM sales 
            WHERE Date BETWEEN %s AND %s
            ORDER BY Date;
        """#create a query that return the sales between the date
        cursor.execute(query, (start_date, end_date))
        result = cursor.fetchall()
        connexion.close()

        if not result:
            raise HTTPException(status_code=404, detail="No sales found in the given date range")

        return result

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Database error: " + str(err))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use 'YYYY-MM-DD'")

##Get the daily sales revenue per vendeur
@app.get("/sales_revenue_per_day_and_vendeur")
def sales_revenue_per_day_and_vendeur():
    """This function doesn't take any parameter
    
    It returns the daily sales revenue per vendeur order in 
    the descending order (from the biggest to the biggest)"""
    try:

        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor(dictionary=True)
        query = """
            SELECT Date, Vendeur, SUM(IFNULL(PrixReel, 0) * IFNULL(Quantite, 0)) AS total_revenue
            FROM sales
            GROUP BY Date, Vendeur
            ORDER BY Date, total_revenue DESC;
        """#we create a query that return the date, the vendeur (grouped) with the calculated sales revenue order in the descending order
        cursor.execute(query)
        result = cursor.fetchall()#return all tuple
        connexion.close()

        if not result:
            raise HTTPException(status_code=404, detail="No sales data found")

        return result

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Database error: " + str(err))

##Add a sale in the database
@app.post("/add_sale")
def add_sale(sale: sales):
    """This function takes a sale in parameter
    
    It returns a message of success and add the sale in 
    the MySQL database"""
    try:
        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM sales WHERE ID = %s", (sale.ID,))#make a query to chec if the ID already exists
        id_exists = cursor.fetchone()[0]
        
        if id_exists > 0:
            raise HTTPException(status_code=400, detail=f"Sale with ID {sale.ID} already exists.")

        query = """
            INSERT INTO sales (ID, Date, Produit, Prix, Quantite, Categorie, Vendeur, Remise, PrixReel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """#we create a query that insert the sale object into the database
        cursor.execute(query, (
            sale.ID, sale.Date, sale.Produit, sale.Prix, sale.Quantite, 
            sale.Categorie, sale.Vendeur, sale.Remise, sale.PrixReel
        ))

        connexion.commit()
        connexion.close()

        return {"message": "Sale added successfully"}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail="Database error: " + str(err))

##Add a new table in the database
@app.post("/upload_csv/{file_name}")
def upload_csv(file_name: str):
    """This function takes the name of the csv file in parameter
    (without the extension)
    
    It returns a message of success, and create/fill the new table 
    in the MySQL database"""
    try:
        csv_file_path = file_name + '.csv'
        if not os.path.exists(csv_file_path):#we check teh existance of the csv file
            raise FileNotFoundError(f"The file '{csv_file_path}' does not exist.")

        df = pd.read_csv(csv_file_path)#we load the csv file
        df = df.drop_duplicates()#can't set the primary key because I don't know it we delete the duplicate

        connexion = mysql.connector.connect(**config)
        cursor = connexion.cursor()

        columns = df.columns
        feature_type = []

        for column in columns:#we associate the python type to the right sql type
            dtype = str(df[column].dtype)
            if "int" in dtype:
                col_type = "INT"
            elif "float" in dtype:
                col_type = "FLOAT"
            elif "datetime" in dtype:
                col_type = "DATETIME"
            else:
                col_type = "VARCHAR(255)" 
            
            feature_type.append(f"`{column}` {col_type}")

        create_table_sql = f"""
            CREATE TABLE IF NOT EXISTS `{file_name}` (
                {', '.join(feature_type)}
            );
        """#we create the table and all the columns that goes with it

        cursor.execute(create_table_sql)

        for _, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(columns))
            sql = f"""
                INSERT INTO `{file_name}` ({', '.join(columns)})
                VALUES ({placeholders})
            """#insert the data in the table we've just created
            cursor.execute(sql, tuple(row))
        connexion.commit()
        connexion.close()

        return {"status": f"Table '{file_name}' created and CSV data inserted successfully!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {e}")