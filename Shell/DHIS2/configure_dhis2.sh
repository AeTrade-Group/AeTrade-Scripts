#!/bin/bash

# Exit on any error
set -e

# Creating DHIS2 configuration file
echo "Creating DHIS2 configuration file..."
cat << EOF | sudo -u dhis_tl tee /var/www/aetrade.gov.rw/config/dhis.conf
# Hibernate SQL dialect
connection.dialect = org.hibernate.dialect.PostgreSQLDialect

# JDBC driver class
connection.driver_class = org.postgresql.Driver

# Database connection URL
connection.url = jdbc:postgresql:dhis2

# Database username
connection.username = dhis_tl

# Database password
connection.password = P@ssw0rd

# Database schema behavior, can be validate, update, create, create-drop
connection.schema = update

# Encryption password (sensitive)
encryption.password = P@ssw0rd
EOF

echo "DHIS2 configuration complete."
