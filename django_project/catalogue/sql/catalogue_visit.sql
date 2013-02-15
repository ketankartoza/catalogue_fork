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
-- Name: catalogue_visit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_visit_id_seq', 343, true);


--
-- Data for Name: catalogue_visit; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_visit (id, city, country, ip_address, visit_date, user_id, ip_position) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

