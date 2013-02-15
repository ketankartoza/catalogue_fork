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
-- Name: catalogue_projection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_projection_id_seq', 6, true);


--
-- Data for Name: catalogue_projection; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_projection (id, epsg_code, name) FROM stdin;
1	32737	UTM37S
2	32733	UTM33S
3	32738	UTM38S
4	32734	UTM34S
5	32735	UTM35S
6	32736	UTM36S
\.


--
-- PostgreSQL database dump complete
--

