-- Table: public.airport

-- DROP TABLE IF EXISTS public.airport;

CREATE TABLE IF NOT EXISTS public.airport
(
    airport_id integer NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    location character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT airport_pkey PRIMARY KEY (airport_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airport
    OWNER to postgres;

-- Table: public.aircraft

-- DROP TABLE IF EXISTS public.aircraft;

CREATE TABLE IF NOT EXISTS public.aircraft
(
    aircraft_id integer NOT NULL,
    pilot character varying(50) COLLATE pg_catalog."default" NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    owner character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT aircraft_pkey PRIMARY KEY (aircraft_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.aircraft
    OWNER to postgres;

-- Table: public.airport

-- DROP TABLE IF EXISTS public.airport;

CREATE TABLE IF NOT EXISTS public.airport
(
    airport_id integer NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    location character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT airport_pkey PRIMARY KEY (airport_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.airport
    OWNER to postgres;

-- Table: public.airport/aircraft

-- DROP TABLE IF EXISTS public."airport/aircraft";

CREATE TABLE IF NOT EXISTS public."airport/aircraft"
(
    aicraft_id integer NOT NULL,
    airport_id integer NOT NULL,
    CONSTRAINT aircraft_id FOREIGN KEY (aicraft_id)
        REFERENCES public.aircraft (aircraft_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT airport_id FOREIGN KEY (airport_id)
        REFERENCES public.airport (airport_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."airport/aircraft"
    OWNER to postgres;

-- Table: public.ticket

-- DROP TABLE IF EXISTS public.ticket;

CREATE TABLE IF NOT EXISTS public.ticket
(
    ticket_id integer NOT NULL,
    price integer NOT NULL,
    class character varying(20) COLLATE pg_catalog."default" NOT NULL,
    date date NOT NULL,
    duration time with time zone NOT NULL,
    aircraft_id integer NOT NULL,
    user_acc_id integer NOT NULL,
    CONSTRAINT ticket_pkey PRIMARY KEY (ticket_id),
    CONSTRAINT aircraft_id FOREIGN KEY (aircraft_id)
        REFERENCES public.aircraft (aircraft_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT user_acc_id FOREIGN KEY (user_acc_id)
        REFERENCES public.user_account (user_acc_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ticket
    OWNER to postgres;

-- Table: public.user_account

-- DROP TABLE IF EXISTS public.user_account;

CREATE TABLE IF NOT EXISTS public.user_account
(
    user_acc_id integer NOT NULL,
    name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    mailbox character varying(50) COLLATE pg_catalog."default" NOT NULL,
    bank_card character varying(20) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT user_account_pkey PRIMARY KEY (user_acc_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_account
    OWNER to postgres;
