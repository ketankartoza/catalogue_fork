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
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- PostgreSQL database dump complete
--

