 echo Enter your NYU ID
 read id 
 psql -d ${id}_db -a -f ../code/schema.sql
 cat ./csv_files/customers.csv | psql -U ${id} -d ${id}_db -c "COPY Customers FROM STDIN CSV HEADER"
 cat ./csv_files/sellers.csv | psql -U ${id} -d ${id}_db -c "COPY Sellers FROM STDIN CSV HEADER"
 cat ./csv_files/manufacturers.csv | psql -U ${id} -d ${id}_db -c "COPY Manufacturers FROM STDIN CSV HEADER"
 cat ./csv_files/warehouses.csv | psql -U ${id} -d ${id}_db -c "COPY Warehouses FROM STDIN CSV HEADER"
 cat ./csv_files/transaction_times.csv | psql -U ${id} -d ${id}_db -c "COPY Time FROM STDIN CSV HEADER"
 cat ./csv_files/products.csv | psql -U ${id} -d ${id}_db -c "COPY Product_produces_transaction FROM STDIN CSV HEADER"
 cat ./csv_files/stored_in.csv | psql -U ${id} -d ${id}_db -c "COPY Stored_in FROM STDIN CSV HEADER"
 cat ./csv_files/inventory.csv | psql -U ${id} -d ${id}_db -c "COPY Inventory_manage FROM STDIN CSV HEADER"
 cat ./csv_files/stock.csv | psql -U ${id} -d ${id}_db -c "COPY Stock FROM STDIN CSV HEADER"