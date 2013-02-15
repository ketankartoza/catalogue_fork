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
-- Name: catalogue_orderstatushistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_orderstatushistory_id_seq', 2, true);


--
-- Data for Name: catalogue_orderstatushistory; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_orderstatushistory (id, user_id, order_id, order_change_date, notes, old_order_status_id, new_order_status_id) FROM stdin;
1	1	2	2010-07-12 00:10:42.341785+02	Testing	1	2
2	1	2	2010-07-12 00:10:52.65599+02	Testing	2	3
\.


--
-- PostgreSQL database dump complete
--

