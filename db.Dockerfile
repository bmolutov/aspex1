# Base image
FROM postgres:15.3

# Copy the initialization scripts to the container
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the port on which the database will run (if required)
# EXPOSE 5432
