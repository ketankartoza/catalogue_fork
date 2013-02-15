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
-- Name: catalogue_searchrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_searchrecord_id_seq', 3, true);


--
-- Data for Name: catalogue_searchrecord; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_searchrecord (id, user_id, order_id, product_id) FROM stdin;
1	1	2	9
3	1	2	2
\.


--
-- PostgreSQL database dump complete
--

