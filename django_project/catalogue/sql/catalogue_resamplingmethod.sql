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
-- Name: catalogue_resamplingmethod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_resamplingmethod_id_seq', 2, true);


--
-- Data for Name: catalogue_resamplingmethod; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_resamplingmethod (id, name) FROM stdin;
1	Nearest Neighbour
2	Cubic convolution
\.


--
-- PostgreSQL database dump complete
--

