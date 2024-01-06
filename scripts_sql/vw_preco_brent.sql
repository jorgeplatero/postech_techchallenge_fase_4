-- View: public.vw_preco_brent

-- DROP VIEW public.vw_preco_brent;

CREATE OR REPLACE VIEW public.vw_preco_brent
 AS
 SELECT data,
    EXTRACT(year FROM data) AS ano,
    preco AS preco_atual,
    lag(preco, 1) OVER (ORDER BY data) AS preco_anterior,
    round(((preco - lag(preco, 1) OVER (ORDER BY data)) / lag(preco, 1) OVER (ORDER BY data) * 100::double precision)::numeric, 2) AS variacao,
    previsto
   FROM ( SELECT preco_brent.data,
            preco_brent.preco,
            0 AS previsto
           FROM ipea.preco_brent
        UNION ALL
         SELECT preco_previsto_brent.data,
            preco_previsto_brent.preco_previsto,
            1 AS previsto
           FROM ipea.preco_previsto_brent) tb
  ORDER BY data;

ALTER TABLE public.vw_preco_brent
    OWNER TO postgres;

