--dump do schema apenas: pg_dump --host 127.0.0.1 --port 5432 --username postgres --format custom --verbose --schema ipea postech > Downloads/dump_04-01-24.backup

CREATE TABLE ipea.preco_brent(
    data date,
    preco float
)

CREATE TABLE ipea.preco_previsto_brent(
    data date,
    preco_previsto float
)

CREATE TABLE ipea.wmape(
    data date,
    wmape float
)

CREATE TABLE ipea.preco_dolar(
    data date,
    preco float
)