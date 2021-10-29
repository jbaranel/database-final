-- The participation constraints on product and manufacturer cannot be captured in this implementation (keep this comment in the final submittions, only remove the parentheses)

create table Product_produces(
    serial_num char(32) primary key,
    name varchar(128) not null,
    category varchar (32),
    date_produced date not null, --we don't have this as attribute in our ER, need to be removed)
    manufacturuer integer not null,
    description varchar(512),
    foreign key (manufacturuer) references Manufacturuer(mid), --(you only include the primary key of the other entity set, not all attributes). 
);

create table Manufacturuer(
    mid integer primary key,
    name varchar (128) not null,
);

create table Warehouse(
    name varchar(128) primary key,
    items_stored integer,
    total_capacity integer
    address varchar(256) --You added multiple attributes we don't have in our implementation    
);

create table Seller(
    sid integer primary key,
    name varchar(64),
);

create table Customer(
    id integer primary key,
    name varchar(64),
    surname varchar(64),
    address varchar(256) --again, if you want to add multiple attributes, add them in the implementation on the doc too (see slide 50 lec 2)
);

create table Time(
    time timestamp primary key -- you made it primary key here but not on the ER diagram. 
);

create table Transaction(
    serial_num char(32),
    customer integer,
    seller integer,
    timestamp timestamp, --do we need to include this? not sure as it's not a primary key. 
    primary key(serial_num, customer, serial_num, timestamp),
    foreign key (serial_num) references Product(serial_num),
    foreign key (seller) references Seller(sid),
    foreign key (customer) references Customer(cid),
    foreign key (timestamp) references Time(timestamp),
);

create table Inventory_manage( --this type of names are preferred as make it more clear I believe
    iid integer primary key,
    manager integer not null, -- only not null is needed for a one sided total constraint
    quantity integer,
    foreign key (manager) references Seller(sid)
);

create table Stock(
    serial_num char(32)
    iid integer,
    primary key(serial_num, iid);
    foreign key (serial_num) references Product,
    foreign key (iid) references Inventory
);

create table List( -- let's keep the name consistent to our ER diag
    serial_num char(32) ,
    sid integer,
    primary key(serial_num, sid),
    price integer not null, -- debating about this, make sure to change it if you choose to move prime to product
    foreign key (serial_num) references Product(serial_num),
    foreign key (sid) references Seller(sid)    
);
