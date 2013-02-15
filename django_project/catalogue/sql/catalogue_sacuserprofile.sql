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
-- Name: catalogue_sacuserprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('catalogue_sacuserprofile_id_seq', 1, true);


--
-- Data for Name: catalogue_sacuserprofile; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY catalogue_sacuserprofile (id, user_id, date, country, latitude, longitude, location, strategic_partner, firstname, surname, url, about, address1, address2, address3, address4, post_code, organisation, contact_no) FROM stdin;
1	1	2010-07-11 17:50:29.904445+02	\N	\N	\N		f	Tim 	Sutton			Foo	Bar			1234	Linfiniti Consulting CC	1234567
\.


--
-- PostgreSQL database dump complete
--

