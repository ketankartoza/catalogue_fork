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
-- Name: catalogue_orderstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_orderstatus_id_seq', 8, true);


--
-- Data for Name: catalogue_orderstatus; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_orderstatus (id, name) FROM stdin;
1	Placed
2	In production
3	Completed
4	Cancelled
5	Awaiting info from client
6	Awaiting imagery from provider
7	Ready for download
8	Reopened due to issues
\.


--
-- PostgreSQL database dump complete
--

