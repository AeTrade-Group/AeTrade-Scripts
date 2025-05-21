#!/bin/bash

# Exit on any error
set -e

# Set server timezone to Kigali
echo "Setting server timezone to Kigali..."
sudo timedatectl set-timezone Africa/Kigali

# Create domain directory
echo "Creating domain directory..."
sudo mkdir -p /var/www/aetrade.gov.rw

# Create user for DHIS2
echo "Creating 'dhis_tl' user..."
sudo useradd dhis_tl -s /bin/false
echo "Setting password for 'dhis_tl' user..."
echo "dhis_tl:P@ssw0rd" | sudo chpasswd

# Create configuration directory
echo "Creating configuration directory..."
sudo mkdir /var/www/aetrade.gov.rw/config
sudo chown dhis_tl:dhis_tl /var/www/aetrade.gov.rw/config

# Install PostgreSQL and PostGIS
echo "Updating package list..."
sudo apt-get update
echo "Installing PostgreSQL..."
sudo apt-get install -y postgresql postgresql-contrib
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql.service
echo "Installing PostGIS..."
sudo apt-get install -y postgis

# Configure PostgreSQL
echo "Creating PostgreSQL user 'dhis_tl'..."
echo "P@ssw0rd" | sudo -u postgres createuser -SDRP dhis_tl
echo "Creating PostgreSQL database 'dhis2'..."
sudo -u postgres createdb -O dhis_tl dhis2
echo "Creating PostGIS extension..."
sudo -u postgres psql -c "create extension if not exists postgis;" dhis2
sudo -u postgres psql -c "create extension if not exists pg_trgm;" dhis2

echo "PostgreSQL setup complete."
