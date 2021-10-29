create table Product(
    serial_num char(32) primary key,
    name varchar(128) not null,
    category varchar (32),
    date_produced date not null, 
    manufacturuer integer not null unique,
    brand varchar (128) not null,
    description varchar(512),
    foreign key (manufacturuer, brand) references Manufacturuer(mid, name)
);

create table Manufacturuer(
    mid integer primary key,
);

create table Warehouse(
    items_stored integer,
    total_capacity integer
    street varchar(64),
    city varchar(64),
    state varchar(64),
    zip integer,
    foreign key (street, city, state, zip) references Address(street, city, state, zip)
);

create table Seller(
    sid integer primary key,
    name varchar(64),
);

create table Customer(
    customer_id integer primary key,
    name varchar(64),
);

create table Address(
    street varchar(64),
    city varchar(64),
    state varchar(64),
    zip integer,
    primary key(street, city, state, zip)
);

create table Sale(
    customer_id,
    sid,
    serial_num,
);