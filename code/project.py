import pandas as pd
import psycopg2
import streamlit as st
from configparser import ConfigParser
from datetime import date, datetime
from collections import deque

"# Ecommerce Management Platform"


def throw_err():    
    st.write("Sorry! Something went wrong with your query, please try again.")

@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    return {k: v for k, v in parser.items(section)}


@st.cache(allow_output_mutation=True)
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

"## Total Sales By Date & Seller"
start_date = st.date_input(
     "Select a start date",
     date(2020,1,1))

end_date = st.date_input(
     "Select an end date",
     date.today())

#getting user input for seller
sql_seller_names = "SELECT name FROM Sellers;"
try:
    #add the option to see all seller
    seller_names1 = deque(query_db(sql_seller_names)["name"]) 
    seller_names1.appendleft('See all sellers')
    seller_name1 = st.selectbox("Choose a seller", seller_names1)
except:    
    throw_err()

if start_date > end_date:
    st.write('Please select and end date after the start date')
elif start_date > date.today():
    st.write('You cannot select a date in the future')
elif end_date > date.today():
    st.write('You cannot select a date in the future')
else:
    st.write('Date range selected:', start_date, end_date)
    #check if user selected to see all sellers or not
    #retrieve user selection
    if start_date and end_date and seller_name1:
        if seller_name1 != 'See all sellers': 
            sql_sales_range = f"""
                SELECT S.name as seller, SUM(P.price) as sum
                FROM Product_produces_transaction P, Sellers S
                WHERE S.name = '{seller_name1}' AND P.sid = S.sid
                AND (P.date_time BETWEEN '{start_date}' AND '{end_date}')
                GROUP BY S.sid
                ORDER BY sum DESC;
                """
        else:
            sql_sales_range = f"""
                SELECT S.name as seller, SUM(P.price) as sum
                FROM Product_produces_transaction P, Sellers S
                WHERE S.name = S.name AND P.sid = S.sid
                AND (P.date_time BETWEEN '{start_date}' AND '{end_date}')
                GROUP BY S.sid
                ORDER BY sum DESC;
                """

        try:
            total_sales = query_db(sql_sales_range)
            if not total_sales.empty:
                st.table(total_sales.style.format({'sum': '${:.2f}'}))
            else:
                st.write("No results for your query")
        except Exception as e:
            throw_err()
            print(e)


'## Number of stock of product by sellers'
sql_product_names = "SELECT name FROM Product_produces_transaction;"
try:
    product_names = set(query_db(sql_product_names)["name"])
    product_name = st.selectbox("Choose a product", product_names)
except:
    throw_err()

#TODO need to check this query
if product_name:
    sql_product = f"""
        SELECT P.name as Product_name, I.quantity, SE.name as Seller_name
        FROM product_produces_transaction P, stock S, inventory_manage I, sellers SE
        WHERE P.name = '{product_name}' and P.serial_num = S.serial_num and S.iid = I.iid and SE.sid = I.manager
        Order by p.name; 
        """
    try:
        product_info = query_db(sql_product)
        st.table(product_info)
    except:
        throw_err()


"## Products Produced By Manufacturer"
sql_manu_names = "SELECT name FROM Manufacturers;"
try:
    manu_names = set(query_db(sql_manu_names)["name"])
    manu_name = st.selectbox("Choose a manufacturer", manu_names)
except:
    throw_err()

if manu_name:
    sql_product = f"""
        SELECT DISTINCT P.name as name
        FROM product_produces_transaction P, Manufacturers M
        WHERE P.manufacturuer = M.mid AND M.name = '{manu_name}'; 
        """
    try:
        products_list = query_db(sql_product)['name'].tolist()
        
        if products_list == []:
            st.write(f"{manu_name} is not producing any product at the moment")
        else:
            #choose output depending on number of products produces
            s = 's' if len(products_list) >1 else ''
            st.write(f"{manu_name} is producing the following product{s}: {' and '.join(products_list)}.")
    except:
        throw_err()

"## Transactions By Customer"
sql_custo_names = "SELECT cid FROM Customers;"
try:
    custo_names = set(query_db(sql_custo_names)["cid"])
    custo_name = st.selectbox("Choose a customer ID", custo_names)
except:
    throw_err()

if custo_name:
    sql_custo_prod = f"""
            SELECT C.name customer, C.surname, S.name seller, P.name as product, T.date_time date_time, p.price
            FROM product_produces_transaction P, Customers C, Sellers S, time T
            WHERE P.cid = C.cid AND P.sid = S.sid AND t.date_time = P.date_time AND C.cid = {custo_name}
            ORDER BY T.date_time; 
        """
    try:               
        custo_list = query_db(sql_custo_prod)
        if not custo_list.empty:
            st.table(custo_list.style.format({'price': '${:.2f}'}))
        else:
            st.write("No results for your query")
        
    except Exception as e:
        throw_err()

"## Best Selling Products"
try:
    order = st.selectbox("Order", ['DESC','ASC'])
except Exception as e:
    throw_err()
if order:
    sql_best_selling = f"""
    SELECT P.name, COUNT(T.date_time) sold
    FROM product_produces_transaction P, Customers C, Sellers S, time T
    WHERE P.cid = C.cid AND P.sid = S.sid AND t.date_time = P.date_time
    GROUP BY P.name
    ORDER BY sold {order};
    """
    try:
        best_list = query_db(sql_best_selling)
        st.table(best_list)
    except Exception as e:
        throw_err()
        print(e)

"## Seller Warehouse Storage"
sql_seller_warehouse = """
    SELECT S.name as seller, COUNT(P.name) as products_stored, W.name as warehouse, W.address
    FROM product_produces_transaction P, Sellers S, Stored_in SI, Warehouses W
    WHERE P.serial_num = SI.serial_num
    AND P.sid = S.Sid
    AND W.name = SI.name
    GROUP BY S.name, W.name
    ORDER BY S.name, warehouse;
    """
try:
    seller_warehouse = query_db(sql_seller_warehouse) 
     
    st.table(seller_warehouse)
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
     
    st.table(country_sales.style.format({'sales': '${:.2f}'}))
except Exception as e:
        throw_err()
        print(e)
