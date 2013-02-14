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
-- Name: catalogue_fileformat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_fileformat_id_seq', 4, true);


--
-- Data for Name: catalogue_fileformat; Type: TABLE DATA; Schema: public; Owner: timlinux
--

INSERT INTO catalogue_fileformat (id, name) VALUES (1, 'GeoTiff');
INSERT INTO catalogue_fileformat (id, name) VALUES (2, 'ECW - ERMapper Compressed Wavelet');
INSERT INTO catalogue_fileformat (id, name) VALUES (3, 'JP2 - JPEG 2000');
INSERT INTO catalogue_fileformat (id, name) VALUES (4, 'ESRI -ShapeFile (Vector products only)');


--
-- PostgreSQL database dump complete
--

