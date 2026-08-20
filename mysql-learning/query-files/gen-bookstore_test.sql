create table `blob`
(
    image mediumblob null
);

create table date_time
(
    publication_date date                                null,
    datetime         datetime                            null,
    timestamp        timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP
);

create table publisher
(
    publisher_id   varchar(40)                         not null
        primary key,
    publisher_name varchar(40)                         not null,
    contact        varchar(40)                         null,
    phone          varchar(40)                         not null,
    create_time    timestamp default CURRENT_TIMESTAMP null
);

create table books
(
    isbn             char(13)      not null
        primary key,
    book_name        varchar(200)  not null,
    price            decimal(8, 2) null,
    author           varchar(200)  null,
    publication_date date          null,
    publisher_id     varchar(40)   null,
    constraint fk_book_publisher
        foreign key (publisher_id) references publisher (publisher_id)
);

