# import-correios-database
Python script to import correios database.

To be able to use, set 'GENERAL_CONFIG' with your database connection info and root directory where your all files are.
'FILE_TO_TABLE' is a map of file name -> table name. This is used to parse 'insert into table_name' statement.

# Example
```
CREATE TABLE public.endereco_bairro
(
    id bigint NOT NULL,
    uf character varying(255) COLLATE pg_catalog."default" NOT NULL,
    localidade_id bigint NOT NULL,
    nome_bairro character varying(255) COLLATE pg_catalog."default" NOT NULL,
    sigla_nome_bairro character varying(255) COLLATE pg_catalog."default",
    CONSTRAINT endereco_bairro_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.endereco_bairro
    OWNER to root;
```

Move file 'LOG_BAIRRO.TXT' to your 'root_dir' set on 'GENERAL_CONFIG'.

Make sure you have installed psycopg2

Run .py.
