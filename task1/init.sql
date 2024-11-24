DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS status;
DROP TABLE IF EXISTS users;
DROP SEQUENCE IF EXISTS status_id_seq;
DROP SEQUENCE IF EXISTS tasks_id_seq;
DROP SEQUENCE IF EXISTS users_id_seq;

-- Table: users
CREATE TABLE users
(
    id           SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL
);

-- Table: status
CREATE TABLE status
(
    id         SERIAL PRIMARY KEY,
    name   VARCHAR(255) UNIQUE NOT NULL
);

-- Table: tasks
CREATE TABLE tasks
(
    id          SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status_id     INTEGER    NOT NULL,
    user_id       INTEGER NOT NULL,
    FOREIGN KEY (status_id) REFERENCES status (id)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);