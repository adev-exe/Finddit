CREATE TABLE IF NOT EXISTS user (
    username TEXT NOT NULL UNIQUE PRIMARY KEY,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email     TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS event (
    e_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT UNIQUE NOT NULL,
    event_date INTEGER NOT NULL,
    event_time time NOT NULL,
    event_desc TEXT NOT NULL
);