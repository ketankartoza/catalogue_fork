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
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 29, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2010-07-11 22:37:44.838707+02	1	14	2	RCC	1	
2	2010-07-11 22:37:55.474251+02	1	14	3	ORP	1	
3	2010-07-11 22:38:11.686491+02	1	14	4	1G Path or Map orientated	1	
4	2010-07-11 22:38:56.411157+02	1	14	5	1R Radiometric	1	
5	2010-07-11 22:39:09.376869+02	1	14	6	0	1	
6	2010-07-11 22:39:43.559645+02	1	14	7	5 Feature extraction	1	
7	2010-07-11 22:39:57.443051+02	1	14	8	4 Classification	1	
8	2010-07-11 22:40:22.935632+02	1	14	9	3 Mosaic	1	
9	2010-07-11 22:41:41.034493+02	1	14	10	3 Ortho	1	
10	2010-07-11 22:42:14.360663+02	1	14	11	1A	1	
11	2010-07-11 23:27:00.149355+02	1	23	1	WGS84	1	
12	2010-07-11 23:28:44.998355+02	1	24	1	Nearest Neighbour	1	
13	2010-07-11 23:28:55.095419+02	1	24	2	Cubic convolution	1	
14	2010-07-11 23:31:38.442699+02	1	25	1	GeoTiff	1	
15	2010-07-11 23:32:02.670637+02	1	25	2	ECW - ERMapper Compressed Wavelet	1	
16	2010-07-11 23:32:25.026504+02	1	25	3	JP2 - JPEG 2000	1	
17	2010-07-11 23:32:49.13265+02	1	25	4	ESRI -ShapeFile (Vector products only)	1	
18	2010-07-11 23:34:40.42424+02	1	27	1	Courier + External Hard Disk	1	
19	2010-07-11 23:35:01.633993+02	1	27	2	Download via FTP or HTTP	1	
20	2010-07-11 23:35:12.330152+02	1	27	3	DVD(s)	1	
21	2010-07-11 23:35:27.790183+02	1	27	4	Other (please specify in notes)	1	
22	2010-07-12 00:04:58.691043+02	1	26	1	Placed	1	
23	2010-07-12 00:05:08.20381+02	1	26	2	In production	1	
24	2010-07-12 00:05:15.845526+02	1	26	3	Completed	1	
25	2010-07-12 00:05:25.869176+02	1	26	4	Cancelled	1	
26	2010-07-12 00:05:38.394879+02	1	26	5	Awaiting info from client	1	
27	2010-07-12 00:05:51.225868+02	1	26	6	Awaiting imagery from provider	1	
28	2010-07-12 00:06:20.71237+02	1	26	7	Ready for download	1	
29	2010-07-12 00:06:38.380908+02	1	26	8	Reopened due to issues	1	
\.


--
-- PostgreSQL database dump complete
--

