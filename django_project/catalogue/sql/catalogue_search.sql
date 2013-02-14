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
-- Name: catalogue_search_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_search_id_seq', 1, true);


--
-- Data for Name: catalogue_search; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_search (id, user_id, keywords, k_orbit_path_min, j_frame_row_min, k_orbit_path_max, j_frame_row_max, search_date, start_date, end_date, guid, deleted, use_cloud_cover, cloud_mean, geometry, ip_position) FROM stdin;
1	1		\N	\N	\N	\N	2010-07-10 12:10:40.609624+02	1990-07-01	2010-07-09	2eb6b2a2-0420-4651-8429-c2e50ce16e2f	f	f	5	\N	0101000020E610000000000000000000000000000000000000
\.


--
-- PostgreSQL database dump complete
--

