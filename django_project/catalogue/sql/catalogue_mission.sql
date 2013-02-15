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
-- Name: catalogue_mission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_mission_id_seq', 4, true);


--
-- Data for Name: catalogue_mission; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_mission (id, abbreviation, name) FROM stdin;
1	N14	Noaa 14
2	N11	Noaa 11
3	E1	E-Ers 1
4	L5	Landsat 5
\.


--
-- PostgreSQL database dump complete
--

