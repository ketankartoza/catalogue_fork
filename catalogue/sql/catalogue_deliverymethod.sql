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
-- Name: catalogue_deliverymethod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_deliverymethod_id_seq', 4, true);


--
-- Data for Name: catalogue_deliverymethod; Type: TABLE DATA; Schema: public; Owner: timlinux
--

INSERT INTO catalogue_deliverymethod (id, name) VALUES (1, 'Courier + External Hard Disk');
INSERT INTO catalogue_deliverymethod (id, name) VALUES (2, 'Download via FTP or HTTP');
INSERT INTO catalogue_deliverymethod (id, name) VALUES (3, 'DVD(s)');
INSERT INTO catalogue_deliverymethod (id, name) VALUES (4, 'Other (please specify in notes)');


--
-- PostgreSQL database dump complete
--

