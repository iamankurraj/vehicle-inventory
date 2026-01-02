CREATE TABLE country (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE region (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    country_id INT NOT NULL REFERENCES country(id) ON DELETE CASCADE,
    UNIQUE (name, country_id)
);

CREATE TABLE provider (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    region_id INT NOT NULL REFERENCES region(id) ON DELETE CASCADE
);

CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    provider_id INT NOT NULL REFERENCES provider(id) ON DELETE CASCADE,
    part_name TEXT NOT NULL,
    quantity INT NOT NULL CHECK (quantity >= 0)
);



CREATE TABLE vehicle (
    vin TEXT PRIMARY KEY
);
