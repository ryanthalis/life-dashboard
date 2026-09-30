CREATE TABLE users (
    user_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    CONSTRAINT users_username_trimmed_nonblank
        CHECK (username = btrim(username) AND username <> ''),
    CONSTRAINT users_email_trimmed_nonblank
        CHECK (email = btrim(email) AND email <> '')
);

CREATE UNIQUE INDEX users_username_lower_uq
    ON users (lower(username));

CREATE UNIQUE INDEX users_email_lower_uq
    ON users (lower(email));
