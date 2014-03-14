drop table if exists entries;

/* different entries can have the same title and category and others */
create table entries (
    id integer primary key autoincrement,
    title string not null,
    category string null,
    buydate string null,
    introduction string null
);

create table users (
    id integer primary key autoincrement,
    username string not null,
    password string not null
);

