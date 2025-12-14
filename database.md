<!--------------------------------------------------------------------------------- Database --->
# Database



<!--------------------------------------------------------------------------------- Install --->
<br><br>

## Install 
[Here](https://github.com/kashanimorteza/postgresql_documents/blob/main/install.md)



<!--------------------------------------------------------------------------------- Connect --->
<br><br>

## Connect 
Linux
```bash
sudo -u postgres psql
```
Mac
```bash
psql -d postgres
```



<!--------------------------------------------------------------------------------- User --->
<br><br>

## User 
```sql
ALTER USER postgres WITH PASSWORD '&WnA8v!(THG%)czK';
CREATE ROLE forex WITH LOGIN CREATEDB PASSWORD '&WnA8v!(THG%)czK';
```



<!--------------------------------------------------------------------------------- Database --->
<br><br>

## Database 
<!-------------------------- Forex -->
forex
```sql
CREATE DATABASE forex WITH OWNER = forex;
\c forex
ALTER ROLE forex WITH CONNECTION LIMIT -1;
ALTER DATABASE forex OWNER TO forex;
ALTER SCHEMA public OWNER TO forex;
GRANT ALL PRIVILEGES ON SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON SCHEMA public TO forex;
GRANT USAGE ON SCHEMA public TO forex;
GRANT CREATE ON SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO forex;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO forex;
```
<!-------------------------- Management -->
management
```sql
CREATE DATABASE management;
\c management
ALTER DATABASE management OWNER TO forex;
ALTER SCHEMA public OWNER TO forex;
GRANT ALL PRIVILEGES ON SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON SCHEMA public TO forex;
GRANT USAGE ON SCHEMA public TO forex;
GRANT CREATE ON SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO forex;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO forex;
GRANT pg_read_server_files TO forex;
```
<!-------------------------- Log -->
log
```sql
CREATE DATABASE log;
\c log
ALTER DATABASE log OWNER TO forex;
ALTER SCHEMA public OWNER TO forex;
GRANT ALL PRIVILEGES ON SCHEMA public TO forex;

GRANT ALL PRIVILEGES ON SCHEMA public TO forex;
GRANT USAGE ON SCHEMA public TO forex;
GRANT CREATE ON SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO forex;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO forex;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO forex;
GRANT pg_read_server_files TO forex;
```