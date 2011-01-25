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
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 14, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
5	30	8
6	30	148
7	30	149
8	30	150
9	30	7
10	18	8
11	18	148
12	18	149
13	18	22
14	18	150
\.


--
-- PostgreSQL database dump complete
--

