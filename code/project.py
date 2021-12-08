import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser
from datetime import date, datetime
def throw_err():    
    st.write("Sorry! Something went wrong with your query, please try again.")

@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()

    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

"## Total Sales By Seller"
start_date = st.date_input(
     "Select a start date",
     date.today())

end_date = st.date_input(
     "Select an end date",
     date.today())

if start_date > end_date:
    st.write('Please select and end date after the start date')
else:
    st.write('Date range selected:', start_date, end_date)

sql_sales_range = f"""
    SELECT S.name as seller, SUM(P.price)
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    AND (P.date_time BETWEEN '{start_date}' AND '{end_date}')
    GROUP BY S.sid
    ORDER BY S.name;
    """
if start_date and end_date:
    try:
        total_sales = query_db(sql_sales_range)   
        #TODO Need to fix bug here where sales are returned as int and not decimal    
        st.table(total_sales)
    except:
        throw_err()


"## Products Produced By Manufacturer"
sql_products = """
    SELECT M.name as manufacturer, P.name as product, COUNT(P.name)
    FROM Product_produces_transaction P, Manufacturers M
    WHERE P.manufacturuer = M.mid
    GROUP BY M.name, P.name
    ORDER BY P.name;"""
try:
    products = query_db(sql_products)
    st.table(products)
except:
    throw_err()

"## Products Purchased By Customer"
sql_customer_purchases = """
    SELECT C.cid, C.name, C.surname, P.name, P.price
    FROM Product_produces_transaction P, Customers C
    WHERE P.cid = C.cid
    AND C.cid = 45
    ORDER BY P.name;"""

sql_customer_names = """
    SELECT cid, name, surname 
    FROM Customers
    ORDER BY name, surname;"""
try:
    customer_names = query_db(sql_customer_names).values.tolist()
    #TODO want to concat 2 columns for first and lastname
    customer_name = st.selectbox("Choose a customer", customer_names)
except:
    throw_err()

try:
    customer_purchases = query_db(sql_customer_purchases)  
    #TODO Need to fix bug, not sure why this isnt working    
    st.table(customer_purchases)
except:
    throw_err()


"## Products Sold By Seller"
sql_products_sold = """
    SELECT DISTINCT S.sid, S.name, P.name
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    ORDER BY S.sid, P.name;
    """

