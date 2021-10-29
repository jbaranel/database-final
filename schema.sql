-- The participation constraints on product and manufacturer cannot be captured in this implementation 

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
    foreign key (manufacturuer) references Manufacturuer(mid),
    foreign key (cid) references Customer(cid),
    foreign key (sid) references Seller(sid),
    foreign key (timestamp) references Time(timestamp)
);

create table Manufacturuer(
    mid integer primary key,
    name varchar (128) not null,
);

create table Warehouse(
    name varchar(128) primary key,
    items_stored integer,
    capacity integer,
    address varchar(256), 
);

create table Seller(
    sid integer primary key,
    name varchar(64),
);

create table Customer(
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
    foreign key (manager) references Seller(sid)
);

create table Stock(
    serial_num char(32)
    iid integer,
    primary key(serial_num, iid);
    foreign key (serial_num) references Product,
    foreign key (iid) references Inventory
);
