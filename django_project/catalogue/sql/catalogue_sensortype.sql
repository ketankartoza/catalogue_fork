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
-- Name: catalogue_sensortype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_sensortype_id_seq', 3, true);


--
-- Data for Name: catalogue_sensortype; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_sensortype (id, abbreviation, name) FROM stdin;
1	AVHR	Advanced Very High Resolution Radiometer
2	AMI	AMI
3	MST	Multispectral + Thermal
\.


--
-- PostgreSQL database dump complete
--

