 psql -d jb7607_db -a -f ../code/schema.sql
 cat ./csv_files/customers.csv | psql -U jb7607 -d jb7607_db -c "COPY Customers FROM STDIN CSV HEADER"
 cat ./csv_files/sellers.csv | psql -U jb7607 -d jb7607_db -c "COPY Sellers FROM STDIN CSV HEADER"
 cat ./csv_files/manufacturers.csv | psql -U jb7607 -d jb7607_db -c "COPY Manufacturers FROM STDIN CSV HEADER"
 cat ./csv_files/warehouses.csv | psql -U jb7607 -d jb7607_db -c "COPY Warehouses FROM STDIN CSV HEADER"