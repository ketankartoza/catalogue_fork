--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

--
-- Name: catalogue_datum_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_datum_id_seq', 1, true);


--
-- Data for Name: catalogue_datum; Type: TABLE DATA; Schema: public; Owner: timlinux
--

INSERT INTO catalogue_datum (id, name) VALUES (1, 'WGS84');


--
-- PostgreSQL database dump complete
--

