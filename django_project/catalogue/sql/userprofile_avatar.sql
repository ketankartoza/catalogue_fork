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
-- Name: userprofile_avatar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('userprofile_avatar_id_seq', 1, false);


--
-- Data for Name: userprofile_avatar; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY userprofile_avatar (id, image, user_id, date, valid) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

