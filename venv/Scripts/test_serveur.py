import requests
import json

def test_root():
    #send a get request to the root end point of the fastapi server
    response = requests.get("http://127.0.0.1:5000/")
    #indicate the success the query
    assert response.status_code == 200
     #print the json response
    print(response.json()) 

def test_get_employee(employee_id):
    #send a get request to the "/employees/{employee_id}" endpoint
    response = requests.get(f"http://127.0.0.1:5000/employees/{employee_id}")
    assert response.status_code == 200
    print(response.json()) 

def test_get_sale(sale_id):
    response = requests.get(f"http://127.0.0.1:5000/sales/{sale_id}")
    assert response.status_code == 200
    print(response.json())

def test_get_sale_per_categorie(sale_categorie):
    selected_columns = "ID,Date,Produit" 
    response = requests.get(f"http://127.0.0.1:5000/sales_categorie/{sale_categorie}?selected_columns={selected_columns}")
    print(response.json())

def test_sales_in_date_range(start_date, end_date):
    selected_columns = "ID,Date,Produit,Vendeur" 
    response = requests.get(f"http://127.0.0.1:5000/sales_in_date_range?start_date={start_date}&end_date={end_date}?selected_columns={selected_columns}")
    print(response.json())

def test_sales_revenue_per_day_and_vendeur():
    response = requests.get("http://127.0.0.1:5000/sales_revenue_per_day_and_vendeur")
    assert response.status_code == 200
    print(response.json())

def test_add_sale():
    #create the sales that we will integrate to the database
    sale_data = {
        "ID": 96,
        "Date": "2025-10-06",
        "Produit": "Poulet",
        "Prix": 30,
        "Quantite": 5,
        "Categorie": "Viande",
        "Vendeur": 1,
        "Remise": 10.0,
        "PrixReel": 4500.0
    }
    response = requests.post("http://127.0.0.1:5000/add_sale", json=sale_data)
    print(response.json())

def test_upload_csv(file_name):
    response = requests.post(f"http://127.0.0.1:5000/upload_csv/{file_name}")
    #print the status code of the query
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")


print('root_test\n')
test_root()
print('\n')

print('get_employee_test\n')
##existing employee
test_get_employee(1)
##non-existing employee
#test_get_employee(10)
print('\n')

print('get_sale_test\n')    
##existing sales
test_get_sale(1)
##non-existing sale
#test_get_sale(100)
print('\n')

print('get_sale_from_categorie_test\n') 
##existing cateforie
test_get_sale_per_categorie("Informatique")
##non-existing categorie
#test_get_sale_per_categorie("Transport")
print('\n')

print('get_sale_in_a_given_period_test\n') 
##existing sales in the period
test_sales_in_date_range("2023-10-01", "2023-10-31")
##non-existing sales in the period
#test_sales_in_date_range("2027-10-01", "2027-10-31")
##inverted start and end date
#test_sales_in_date_range("2023-10-31", "2023-10-01")
print('\n')

print('get_revenueper_day_and_per_vendeur_test\n') 
test_sales_revenue_per_day_and_vendeur()
print('\n')

print('add_one_sale_test\n') 
test_add_sale()
print('\n')

print("upload_csv_file_test\n")
test_upload_csv("emp")
print('\n')
