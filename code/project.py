import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser

"# Demo: Streamlit + Postgres"


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


"## Read tables"

sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
try:
    all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    table_name = st.selectbox("Choose a table", all_table_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

if table_name:
    f"Display the table"

    sql_table = f"SELECT * FROM {table_name};"
    try:
        df = query_db(sql_table)
        st.dataframe(df)
    except:
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )

"## Query customers"

sql_customer_names = "SELECT name FROM Customers;"
try:
    customer_names = query_db(sql_customer_names)["name"].tolist()
    customer_name = st.selectbox("Choose a customer", customer_names)
except:
    st.write("Sorry! Something went wrong with your query, please try again.")

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
        st.write(
            "Sorry! Something went wrong with your query, please try again."
        )
