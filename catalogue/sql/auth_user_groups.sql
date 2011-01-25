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
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- PostgreSQL database dump complete
--

