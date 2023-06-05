-- Create the database
CREATE DATABASE aspex1_db;

-- Create the user
CREATE USER aspex1_user WITH ENCRYPTED PASSWORD 'qwerty';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON DATABASE aspex1_db TO aspex1_user;
