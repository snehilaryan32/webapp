# Setup Postgres
sudo postgresql-setup initdb
PG_HBA_CONF="/var/lib/pgsql/data/pg_hba.conf"
cp $PG_HBA_CONF ${PG_HBA_CONF}.backup
sudo sed -i 's/ident/md5/g' $PG_HBA_CONF
# sudo sed -i 's/peer/md5/g' $PG_HBA_CONF
cd /tmp 
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "ALTER USER $DB_USER WITH SUPERUSER;"
cd /home/packer