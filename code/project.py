import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

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
#TODO need to make these dates dynamic from user input
start_date, end_date = '2021-08-31', '2021-11-25'

sql_customer_purchases = f"""
    SELECT S.sid, S.name, SUM(P.price)
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    AND (P.date_time BETWEEN {start_date} AND {end_date})
    GROUP BY S.sid
    ORDER BY S.sid;
    """
    
"## Products Produced By Manufacturer"
sql_products = """
    SELECT M.name, P.name, COUNT(P.name)
    FROM Product_produces_transaction P, Manufacturers M
    WHERE P.manufacturuer = M.mid
    GROUP BY M.name, P.name
    ORDER BY P.name;"""
try:
    products = query_db(sql_products).tolist()
except:
    throw_err()
if products:
    try:
        st.write(products)
    except:
        throw_err()

"## Products Purchased By Customer"
sql_customer_purchases = """
    SELECT C.cid, C.name, C.surname, P.name, P.price
    FROM Product_produces_transaction P, Customers C
    WHERE P.cid = C.cid
    ORDER BY C.cid;
    """
"## Products Sold By Seller"
sql_customer_purchases = """
    SELECT DISTINCT S.sid, S.name, P.name
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    ORDER BY S.sid, P.name;
    """

"## Query customers"
sql_customer_names = "SELECT name, surname FROM Customers;"
try:
    customer_names = query_db(sql_customer_names)["name"].tolist()
    customer_name = st.selectbox("Choose a customer", customer_names)
except:
    throw_err()

if customer_name:
    sql_customer = f"SELECT * FROM customers WHERE name = '{customer_name}';"
    try:
        customer_info = query_db(sql_customer).loc[0]
        c_address = (
            customer_info["address"]
        )
        st.write(
            f"{customer_name} lives at {c_address}."
        )
    except:
        throw_err()
