<!--------------------------------------------------------------------------------- Database --->
# Database



<!--------------------------------------------------------------------------------- Install --->
<br><br>

## Install 
[Postgres](https://github.com/kashanimorteza/postgresql_documents/blob/main/install.md)



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
CREATE ROLE management WITH LOGIN CREATEDB PASSWORD '&WnA8v!(THG%)czK';
```



<!--------------------------------------------------------------------------------- Database --->
<br><br>

## Database 
<!-------------------------- Forex -->
forex
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'forex' AND pid <> pg_backend_pid();
```
```sql
Drop DATABASE forex;
```
```sql
CREATE DATABASE forex WITH OWNER = forex;
```
```sql
\c forex
```
```sql
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
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'management' AND pid <> pg_backend_pid();
```
```sql
Drop DATABASE management;
```
```sql
CREATE DATABASE management;
```
```sql
\c management
```
```sql
ALTER DATABASE management OWNER TO management;
ALTER SCHEMA public OWNER TO management;
GRANT ALL PRIVILEGES ON SCHEMA public TO management;
GRANT ALL PRIVILEGES ON SCHEMA public TO management;
GRANT USAGE ON SCHEMA public TO management;
GRANT CREATE ON SCHEMA public TO management;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO management;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO management;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO management;
GRANT pg_read_server_files TO management;
```
<!-------------------------- Log -->
log
```sql
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'log' AND pid <> pg_backend_pid();
```
```sql
Drop DATABASE log;
```
```sql
CREATE DATABASE log;
```
```sql
\c log
```
```sql
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



<!--------------------------------------------------------------------------------- Backup --->
<br><br>

## Backup 
<!-------------------------- simple -->
simple
```bash
sudo -u postgres pg_dump -v -O -d forex -f backup_2025-12-28.sql
```
```bash
sudo -u postgres pg_dump -v -O -d forex forex -t public.xauusd_t1 -f backup_xauusd_t1_2025-12-14.sql
```

<!-------------------------- gzip -->
gzip
```bash
sudo -i -u postgres
pg_dump --dbname=forex --verbose --no-owner | gzip > backup_2025-12-14.gz
pg_dump --dbname=forex --verbose --no-owner --table=public.xauusd_t1 | gzip > backup_xauusd_t1_2025-12-14.gz
```
<!-------------------------- pigz -->
pigz
```bash
sudo -i -u postgres
pg_dump --dbname=forex --verbose --no-owner | pigz > backup_2025-12-14.tar.gz
pg_dump --dbname=forex --verbose --no-owner --table=public.xauusd_t1 | pigz > backup_xauusd_t1_2025-12-14.tar.gz
```



<!--------------------------------------------------------------------------------- Restore --->
<br><br>

## Restore 
<!-------------------------- simple -->
simple
```bash
sudo -u postgres psql -d forex -v ON_ERROR_STOP=1 -f backup_2025-12-14.sql
```
```bash
sudo -u postgres psql -d forex -v ON_ERROR_STOP=1 -f backup_xauusd_t1_2025-12-14.sql
```

<!-------------------------- gzip -->
gzip
```bash
```

<!-------------------------- pigz -->
pigz
```bash
sudo -i -u postgres
pigz -dc backup_2025-12-14.tar.gz | psql -U postgres -d forex
pigz -dc backup_xauusd_t1_2025-12-14.tar.gz | psql -U forex -d forex
```



<!--------------------------------------------------------------------------------- Sql --->
<br><br>

## Sql
<!-------------------------- Size -->
Size
```bash
SELECT pg_size_pretty(pg_database_size('forex'));
```
```bash
\c forex
SELECT pg_size_pretty( pg_total_relation_size('xauusd_t1'));
```
<!-------------------------- Truncate-->
Truncate
```sql
DO $$
DECLARE
    sym    text;
    tf     text;
    prefix text;
    tbl    text;
BEGIN
    -- List of symbols
    FOR sym IN SELECT unnest(ARRAY[
        'EUR/USD','EUR/GBP','EUR/CHF','EUR/JPY','EUR/AUD','EUR/CAD','EUR/NZD',
        'GBP/USD','GBP/JPY','GBP/CHF','GBP/NZD','GBP/AUD','GBP/CAD',
        'AUD/USD','AUD/CAD','AUD/JPY','AUD/NZD','AUD/CHF',
        'NZD/USD','NZD/JPY','NZD/CHF','NZD/CAD',
        'USD/JPY','USD/CHF','USD/CAD',
        'CAD/JPY','CAD/CHF',
        'CHF/JPY',
        'USOil','UKOil','XAU/USD','XAG/USD'
    ])
    LOOP
        prefix := lower(replace(sym, '/', ''));

        -- Loop timeframes
        FOR tf IN SELECT unnest(ARRAY[
            'w1','d1','h8','h6','h4','h3','h2','h1','m30','m15','m5','m1','t1'
        ])
        LOOP
            tbl := prefix || '_' || tf;

            BEGIN
                EXECUTE format('TRUNCATE TABLE %I RESTART IDENTITY', tbl);
                RAISE NOTICE 'Truncated %', tbl;
            EXCEPTION WHEN undefined_table THEN
                RAISE NOTICE 'Table % does NOT exist - skipped', tbl;
            END;

        END LOOP;

    END LOOP;
END $$;
```
<!-------------------------- Count -->
Count
```sql
DROP TABLE IF EXISTS temp_symbol_counts;

CREATE TEMP TABLE temp_symbol_counts (
    symbol text,
    w1  int, d1  int,
    h8  int, h6  int, h4 int, h3 int, h2 int, h1 int,
    m30 int, m15 int, m5 int, m1 int,
    t1  int
);

DO $$
DECLARE
    sym    text;
    prefix text;
    c_w1  int; c_d1  int;
    c_h8  int; c_h6  int; c_h4 int; c_h3 int; c_h2 int; c_h1 int;
    c_m30 int; c_m15 int; c_m5 int; c_m1 int;
    c_t1  int;
BEGIN
    FOR sym IN
        SELECT unnest(ARRAY[
            'EUR/USD','EUR/GBP','EUR/CHF','EUR/JPY','EUR/AUD','EUR/CAD','EUR/NZD',
            'GBP/USD','GBP/JPY','GBP/CHF','GBP/NZD','GBP/AUD','GBP/CAD',
            'AUD/USD','AUD/CAD','AUD/JPY','AUD/NZD','AUD/CHF',
            'NZD/USD','NZD/JPY','NZD/CHF','NZD/CAD',
            'USD/JPY','USD/CHF','USD/CAD',
            'CAD/JPY','CAD/CHF',
            'CHF/JPY',
            'USOil','UKOil','XAU/USD','XAG/USD'
        ])
    LOOP
        prefix := lower(replace(sym, '/', ''));
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_w1')  INTO c_w1;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_d1')  INTO c_d1;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_h8')  INTO c_h8;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_h6')  INTO c_h6;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_h4')  INTO c_h4;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_h3')  INTO c_h3;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_h2')  INTO c_h2;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_h1')  INTO c_h1;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_m30') INTO c_m30;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_m15') INTO c_m15;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_m5')  INTO c_m5;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_m1')  INTO c_m1;
        EXECUTE format('SELECT count(id) FROM %I', prefix || '_t1')  INTO c_t1;
        INSERT INTO temp_symbol_counts
        VALUES (sym,
                c_w1, c_d1,
                c_h8, c_h6, c_h4, c_h3, c_h2, c_h1,
                c_m30, c_m15, c_m5, c_m1,
                c_t1);
    END LOOP;
END $$;

SELECT * FROM temp_symbol_counts;
```
<!-------------------------- Period -->
Period
```sql
DROP TABLE IF EXISTS temp_date_range;

CREATE TEMP TABLE temp_date_range (
    symbol     text,
    timeframe  text,
    table_name text,
    row_count  bigint,
    min_date   timestamp,
    max_date   timestamp
);

DO $$
DECLARE
    sym       text;
    tf        text;
    prefix    text;
    tbl       text;
    v_min     timestamp;
    v_max     timestamp;
    v_count   bigint;
BEGIN
    -- all symbols
    FOR sym IN SELECT unnest(ARRAY[
        'EUR/USD','EUR/GBP','EUR/CHF','EUR/JPY','EUR/AUD','EUR/CAD','EUR/NZD',
        'GBP/USD','GBP/JPY','GBP/CHF','GBP/NZD','GBP/AUD','GBP/CAD',
        'AUD/USD','AUD/CAD','AUD/JPY','AUD/NZD','AUD/CHF',
        'NZD/USD','NZD/JPY','NZD/CHF','NZD/CAD',
        'USD/JPY','USD/CHF','USD/CAD',
        'CAD/JPY','CAD/CHF',
        'CHF/JPY',
        'USOil','UKOil','XAU/USD','XAG/USD'
    ])
    LOOP
        prefix := lower(replace(sym, '/', ''));

        -- all timeframes
        FOR tf IN SELECT unnest(ARRAY[
            'w1','d1','h8','h6','h4','h3','h2','h1','m30','m15','m5','m1','t1'
        ])
        LOOP
            tbl := prefix || '_' || tf;

            BEGIN
                -- change 'date' if your column name is different
                EXECUTE format('SELECT count(id), min(date), max(date) FROM %I', tbl)
                    INTO v_count, v_min, v_max;

                INSERT INTO temp_date_range(symbol, timeframe, table_name, row_count, min_date, max_date)
                VALUES (sym, tf, tbl, v_count, v_min, v_max);

            EXCEPTION
                WHEN undefined_table THEN
                    RAISE NOTICE 'Table % does NOT exist, skipped.', tbl;

                WHEN undefined_column THEN
                    RAISE NOTICE 'Table % missing column "date" or "id", skipped.', tbl;
            END;

        END LOOP;
    END LOOP;
END $$;
SELECT * FROM temp_date_range;
```


<!--------------------------------------------------------------------------------- Config --->
<br><br>

## Config 
```bash
SELECT version();
SELECT count(*) FROM pg_stat_activity;
show max_connections;
show shared_buffers;
show max_locks_per_transaction;
show fsync;
show synchronous_commit;
show max_wal_size;
```



<!--------------------------------------------------------------------------------- Tune --->
<br><br>

## Tune 
```bash
ALTER SYSTEM SET shared_buffers TO '10240MB';
ALTER SYSTEM SET max_connections TO '1024';
ALTER SYSTEM SET max_locks_per_transaction TO '1024';
ALTER SYSTEM SET fsync TO 'off';
ALTER SYSTEM SET synchronous_commit TO 'off';
ALTER SYSTEM SET max_wal_size TO '1024';
VACUUM FULL VERBOSE;
```
Log
```bash
sudo sed -i 's/^[#[:space:]]*fsync.*/fsync = off/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*synchronous_commit.*/synchronous_commit = off/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*full_page_writes.*/full_page_writes = off/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*wal_level.*/wal_level = minimal/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*archive_mode.*/archive_mode = off/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*max_wal_senders.*/max_wal_senders = 0/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*autovacuum.*/autovacuum = on/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*log_statement.*/log_statement = none/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*log_min_duration_statement.*/log_min_duration_statement = -1/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*log_min_error_statement.*/log_min_error_statement = panic/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*logging_collector.*/logging_collector = off/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*log_destination.*/log_destination = stderr/' /etc/postgresql/18/main/postgresql.conf
```
Ram Cpu
```bash
sudo sed -i 's/^[#[:space:]]*shared_buffers.*/shared_buffers = 8GB/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*effective_cache_size.*/effective_cache_size = 24GB/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*work_mem.*/work_mem = 64MB/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*maintenance_work_mem.*/maintenance_work_mem = 1GB/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*max_worker_processes.*/max_worker_processes = 16/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*max_parallel_workers.*/max_parallel_workers = 16/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*max_parallel_workers_per_gather.*/max_parallel_workers_per_gather = 8/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*checkpoint_timeout.*/checkpoint_timeout = 30min/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*checkpoint_completion_target.*/checkpoint_completion_target = 0.9/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*max_wal_size.*/max_wal_size = 8GB/' /etc/postgresql/18/main/postgresql.conf
sudo sed -i 's/^[#[:space:]]*min_wal_size.*/min_wal_size = 2GB/' /etc/postgresql/18/main/postgresql.conf
```



<!--------------------------------------------------------------------------------- Download --->
<br><br>

## Download 
```bash
scp root@10.10.10.114:/var/lib/postgresql/forex.gz ./
scp root@10.10.10.114:/var/lib/postgresql/xauusd_t1.gz ./
```