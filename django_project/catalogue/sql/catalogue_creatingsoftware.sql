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
-- Name: catalogue_creatingsoftware_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_creatingsoftware_id_seq', 1, true);


--
-- Data for Name: catalogue_creatingsoftware; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_creatingsoftware (id, name, version) FROM stdin;
1	Unknown	None
\.


--
-- PostgreSQL database dump complete
--

