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


"## Total Sales By Seller"
start_date = st.date_input(
     "Select a start date",
     date.date(2020,1,1))

end_date = st.date_input(
     "Select an end date",
     date.today())

if start_date > end_date:
    st.write('Please select and end date after the start date')
else:
    st.write('Date range selected:', start_date, end_date)

sql_sales_range = f"""
    SELECT S.name as Seller_Name, SUM(P.price) as Total_sales($)
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    AND (P.date_time BETWEEN '{start_date}' AND '{end_date}')
    GROUP BY S.sid
    ORDER BY Total_sales($);
    """
if start_date and end_date:
    try:
        total_sales = query_db(sql_sales_range)        
        #TODO Need to fix bug here where sales are returned as int and not decimal    
        st.table(total_sales)
        sales = query_db(f"""
            SELECT SUM(P.price) as sum, DATE(P.date_time)
            FROM Product_produces_transaction P, Sellers S
            WHERE P.sid = S.sid
            AND (P.date_time BETWEEN '{start_date}' AND '{end_date}')
            GROUP BY P.date_time
            ORDER BY P.date_time;
            """)

        st.table(sales)
    except Exception as e:
        throw_err()
        print(e)


"## Products Produced By Manufacturer"
sql_products = """
    SELECT M.name as manufacturer, P.name as product, COUNT(P.name)
    FROM Product_produces_transaction P, Manufacturers M
    WHERE P.manufacturuer = M.mid
    GROUP BY M.name, P.name
    ORDER BY M.name, P.name;"""
try:
    products = query_db(sql_products)    
    st.table(products)
except Exception as e:
        throw_err()
        print(e)

"## Products Purchased By Customer"
sql_customer_names = """
    SELECT cid, name, surname 
    FROM Customers
    ORDER BY name, surname;"""
try:
    customers = query_db(sql_customer_names)
    first_name = customers['name']
    surname = customers['surname']
    customer_names = first_name + " " + surname

    customer_name = st.selectbox("Choose a customer", customer_names)
    #TODO hard coded for now
    #cid = customers[customers['name'] = first_name]
    try:
        customer_purchases = query_db(f"""            
        SELECT C.cid, C.name, C.surname, P.name, P.price
        FROM Product_produces_transaction P, Customers C
        WHERE P.cid = C.cid
        AND C.cid = {cid}
        ORDER BY P.name;"""
        ).values.tolist()
        #TODO Need to fix bug, not sure why this isnt working    
        st.write(customer_purchases)
    except Exception as e:
        throw_err()
        print(e)
except Exception as e:
        throw_err()
        print(e)



"## Products Sold By Seller"
sql_products_sold = """
    SELECT DISTINCT S.sid, S.name, P.name
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    ORDER BY S.sid, P.name;
    """

sql_seller_names = """
    SELECT sid, name
    FROM Sellers
    ORDER BY name;"""
try:
    sellers = query_db(sql_seller_names)  
    seller_names = sellers['name']

    seller_name = st.selectbox("Choose a customer", seller_names)
except Exception as e:
        throw_err()
        print(e)

"## Total Sales By Country"
sql_country_sales = """
    SELECT S.country, SUM(P.price) as Sales, COUNT(P.serial_num) as Goods_Sold
    FROM Product_produces_transaction P, Sellers S
    WHERE P.sid = S.sid
    GROUP BY S.country
    ORDER BY Sales desc;
    """
try:
    country_sales = query_db(sql_country_sales)  
    st.table(country_sales)
except Exception as e:
        throw_err()
        print(e)
