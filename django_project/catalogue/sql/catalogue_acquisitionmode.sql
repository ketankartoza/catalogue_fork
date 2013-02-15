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
-- Name: catalogue_acquisitionmode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_acquisitionmode_id_seq', 3, true);


--
-- Data for Name: catalogue_acquisitionmode; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_acquisitionmode (id, abbreviation, name, geometric_resolution, band_count) FROM stdin;
1	MS	Multispectral	0	0
2	VV	Vertical / Vertical Polarisation	0	0
3	HRT	Multispectral and Thermal	0	0
\.


--
-- PostgreSQL database dump complete
--

