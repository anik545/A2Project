drop table if exists users;
    create table users (
    id integer primary key autoincrement,
    Fname text not null,
    Lname text not null,
    email text not null,
    password text not null
);
