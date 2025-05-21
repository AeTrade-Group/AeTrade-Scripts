  GNU nano 6.2                                                       install_dhis2.sh                                                                 
#!/bin/bash

# Exit on any error
set -e

# Install OpenJDK 11
echo "Installing OpenJDK 11..."
sudo apt-get install -y openjdk-11-jdk

# Install Tomcat
echo "Installing Tomcat..."
sudo apt-get install -y tomcat9-user

# Create Tomcat instance
echo "Creating Tomcat instance..."
cd /var/www/aetrade.gov.rw/
sudo tomcat9-instance-create tomcat-dhis
sudo chown -R dhis_tl:dhis_tl tomcat-dhis/

# Set environment variables for Tomcat
echo "Configuring Tomcat..."
cat << EOF | sudo tee /var/www/aetrade.gov.rw/tomcat-dhis/bin/setenv.sh
#!/bin/sh
export JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64/'
export JAVA_OPTS='-Xmx2000m -Xms1000m'
export DHIS2_HOME='/var/www/aetrade.gov.rw/config'
EOF

sudo chmod +x /var/www/aetrade.gov.rw/tomcat-dhis/bin/setenv.sh

# Download DHIS2 WAR file
echo "Downloading DHIS2 WAR file..."
wget -O dhis.war https://releases.dhis2.org/40/dhis2-stable-40.3.0.war
sudo mv dhis.war /var/www/aetrade.gov.rw/tomcat-dhis/webapps/ROOT.war

# Configure Tomcat startup script
echo "Configuring Tomcat startup script..."
cat << EOF | sudo tee /var/www/aetrade.gov.rw/tomcat-dhis/bin/startup.sh
#!/bin/sh
set -e

if [ "\$(id -u)" -eq "0" ]; then
   echo "This script must NOT be run as root" 1>&2
   exit 1
fi

export CATALINA_BASE="/var/www/aetrade.gov.rw/tomcat-dhis"
/usr/share/tomcat9/bin/startup.sh
echo "Tomcat started"
EOF

sudo chmod +x /var/www/aetrade.gov.rw/tomcat-dhis/bin/startup.sh

echo "DHIS2 installation complete."
