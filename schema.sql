create table Product(
    serial_num char(32) primary key,
    name varchar(128) not null,
    category varchar (32),
    date_produced date not null, 
    manufacturuer integer not null unique,
    brand varchar (128) not null,
    description varchar(512),
    foreign key (manufacturuer, brand) references Manufacturuer(mid, name),    
);

create table Manufacturuer(
    mid integer primary key,
    name varchar (128) not null,
);

create table Warehouse(
    items_stored integer,
    total_capacity integer
    street varchar(64),
    city varchar(64),
    state varchar(64),
    zip integer,    
);

create table Seller(
    sid integer primary key,
    name varchar(64),
);

create table Customer(
    customer_id integer primary key,
    name varchar(64),
    surname varchar(64),
    street varchar(64),
    city varchar(64),
    state varchar(64),
    zip integer,  
);

create table Time(
    time timestamp primary key
);

create table Transaction(
    serial_num char(32),
    customer integer,
    seller integer,
    timestamp timestamp,
    primary key(serial_num, customer, serial_num, timestamp),
    foreign key (serial_num) references Product(serial_num),
    foreign key (seller) references Seller(sid),
    foreign key (customer) references Customer(cid),
    foreign key (timestamp) references Time(timestamp),
);

create table Inventory(
    iid integer primary key,
    manager integer unique not null,
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

create table Listing(
    serial_num char(32) ,
    sid integer,
    primary key(serial_num, sid),
    price integer not null,
    foreign key (serial_num) references Product(serial_num),
    foreign key (sid) references Seller(sid)    
);