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
-- Name: catalogue_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_order_id_seq', 2, true);


--
-- Data for Name: catalogue_order; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_order (id, user_id, notes, processing_level_id, projection_id, datum_id, resampling_method_id, file_format_id, order_status_id, delivery_method_id, order_date) FROM stdin;
2	1	Test	3	3	1	1	1	3	1	2010-07-12 00:10:52.71928+02
\.


--
-- PostgreSQL database dump complete
--

