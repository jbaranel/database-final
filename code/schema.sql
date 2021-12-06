drop table if exists Customers cascade;
drop table if exists Manufacturers cascade;
drop table if exists Sellers cascade;
drop table if exists Warehouses cascade;
drop table if exists Inventory_manage cascade;
drop table if exists Product_produces_transaction cascade;
drop table if exists Stock cascade;
drop table if exists Stored_in cascade;

create table Product_produces_transaction(
    serial_num char(32) primary key,
    cid integer not null,
    sid integer not null,
    timestamp timestamp not null,
    price integer not null,
    name varchar(128) not null,
    category varchar (32),
    manufacturuer integer not null,
    description varchar(512),
    foreign key (manufacturuer) references Manufacturers(mid),
    foreign key (cid) references Customers(cid),
    foreign key (sid) references Sellers(sid),
    foreign key (timestamp) references Time(timestamp)
);

create table Manufacturers(
    mid integer primary key,
    name varchar (128) not null,
);

create table Warehouses(
    name varchar(128) primary key,
    items_stored integer,
    capacity integer,
    address varchar(256), 
);

create table Sellers(
    sid integer primary key,
    name varchar(64),
    country varchar(64);
);

create table Customers(
    id integer primary key,
    name varchar(64),
    surname varchar(64),
    address varchar(256),
);

create table Time(
    time timestamp primary key,
);

create table Inventory_manage( 
    iid integer primary key,
    manager integer not null,
    quantity integer,
    foreign key (manager) references Sellers(sid)
);

create table Stock(
    serial_num char(32)
    iid integer,
    primary key(serial_num, iid);
    foreign key (serial_num) references Product,
    foreign key (iid) references Inventory
);

create table Stored_in(
    serial_num integer
    name varchar(64)
    primary key(serial_num, name)
    foreign key (serial_num) references Product
    foreign key (name) references Warehouses
)
