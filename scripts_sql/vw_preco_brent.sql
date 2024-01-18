CREATE OR REPLACE VIEW ipea.vw_preco_brent
 AS
 SELECT tb2.data,
    tb2.ano,
    tb2.preco_atual_brent,
    tb2.preco_anterior_brent,
    tb2.variacao_preco_brent,
    tb2.previsto,
    COALESCE(COALESCE(COALESCE(preco_dolar.preco, lag(preco_dolar.preco, 1) OVER (ORDER BY tb2.data)), lag(preco_dolar.preco, 3) OVER (ORDER BY tb2.data)), lag(preco_dolar.preco, 1) OVER (ORDER BY tb2.data)) AS preco_dolar
   FROM ( SELECT tb.data,
            EXTRACT(year FROM tb.data) AS ano,
            tb.preco AS preco_atual_brent,
            lag(tb.preco, 1) OVER (ORDER BY tb.data) AS preco_anterior_brent,
            round(((tb.preco - lag(tb.preco, 1) OVER (ORDER BY tb.data)) / lag(tb.preco, 1) OVER (ORDER BY tb.data) * 100::double precision)::numeric, 2) AS variacao_preco_brent,
            tb.previsto
           FROM ( SELECT preco_brent.data,
                    preco_brent.preco,
                    0 AS previsto
                   FROM ipea.preco_brent
                UNION ALL
                 SELECT preco_previsto_brent.data,
                    preco_previsto_brent.preco_previsto,
                    1 AS previsto
                   FROM ipea.preco_previsto_brent) tb
          ORDER BY tb.data) tb2
     LEFT JOIN ipea.preco_dolar ON tb2.data = preco_dolar.data;

ALTER TABLE ipea.vw_preco_brent
    OWNER TO postgres;