--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: catalogue_marketsector; Type: TABLE; Schema: public; Owner: timlinux; Tablespace: 
--

CREATE TABLE catalogue_marketsector (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.catalogue_marketsector OWNER TO timlinux;

--
-- Name: catalogue_marketsector_id_seq; Type: SEQUENCE; Schema: public; Owner: timlinux
--

CREATE SEQUENCE catalogue_marketsector_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.catalogue_marketsector_id_seq OWNER TO timlinux;

--
-- Name: catalogue_marketsector_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: timlinux
--

ALTER SEQUENCE catalogue_marketsector_id_seq OWNED BY catalogue_marketsector.id;


--
-- Name: catalogue_marketsector_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_marketsector_id_seq', 8, true);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: timlinux
--

ALTER TABLE catalogue_marketsector ALTER COLUMN id SET DEFAULT nextval('catalogue_marketsector_id_seq'::regclass);


--
-- Data for Name: catalogue_marketsector; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_marketsector (id, name) FROM stdin;
1	Decline to say
2	Government
3	Academic - Staff Research
4	Academic - Student Research
5	Commercial
6	Non profit organisation
7	Private Individual
8	Other
\.


--
-- Name: catalogue_marketsector_name_key; Type: CONSTRAINT; Schema: public; Owner: timlinux; Tablespace: 
--

ALTER TABLE ONLY catalogue_marketsector
    ADD CONSTRAINT catalogue_marketsector_name_key UNIQUE (name);


--
-- Name: catalogue_marketsector_pkey; Type: CONSTRAINT; Schema: public; Owner: timlinux; Tablespace: 
--

ALTER TABLE ONLY catalogue_marketsector
    ADD CONSTRAINT catalogue_marketsector_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

alter table catalogue_order add column market_sector_id integer not null references catalogue_marketsector(id) default 1;
