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

--
-- Name: catalogue_processinglevel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_processinglevel_id_seq', 11, true);


--
-- Data for Name: catalogue_processinglevel; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_processinglevel (id, abbreviation, name) FROM stdin;
1	2A	Level 2A
2	RCC	RCC
3	ORP	ORP
4	1G	1G Path or Map orientated
5	1R	1R Radiometric
6	0	0
7	5	5 Feature extraction
8	4	4 Classification
9	3	3 Mosaic
10	3O	3 Ortho
11	1	1A
\.


--
-- PostgreSQL database dump complete
--

