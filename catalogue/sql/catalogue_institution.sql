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
-- Name: catalogue_institution_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_institution_id_seq', 1, true);


--
-- Data for Name: catalogue_institution; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_institution (id, name, address1, address2, address3, post_code) FROM stdin;
1	Satellite Applications Centre	Hartebeeshoek	Gauteng	South Africa	0000
\.


--
-- PostgreSQL database dump complete
--

