create table guilds
(
    id           bigint                                 not null primary key,
    name         varchar(255)                           not null,
    registration timestamp  default current_timestamp() not null,
    is_active    tinyint(1) default 1                   not null,
    db_name      varchar(255)                           not null
);

create table test(
    name varchar (250)
);

insert into test (name) values ('Hello');
insert into test (name) values ('World');