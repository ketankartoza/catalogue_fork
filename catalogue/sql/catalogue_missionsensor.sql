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
-- Name: catalogue_missionsensor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_missionsensor_id_seq', 4, true);


--
-- Data for Name: catalogue_missionsensor; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_missionsensor (id, abbreviation, name, description, has_data) FROM stdin;
1	AVH	NOAA AVHRR		t
2	AMI	ERS AMI SAR		t
3	TM	Landsat 4,5 TM		t
4	MSS	Landsat 1,2,3,4,5 MSS		t
\.


--
-- PostgreSQL database dump complete
--

