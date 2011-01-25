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
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('django_content_type_id_seq', 71, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	log entry	admin	logentry
9	registration profile	registration	registrationprofile
10	mission	catalogue	mission
11	mission sensor	catalogue	missionsensor
12	acquisition mode	catalogue	acquisitionmode
13	sensor type	catalogue	sensortype
14	Processing Level	catalogue	processinglevel
15	Projection	catalogue	projection
16	institution	catalogue	institution
17	license	catalogue	license
18	quality	catalogue	quality
19	creating software	catalogue	creatingsoftware
20	generic product	catalogue	genericproduct
21	optical product	catalogue	opticalproduct
22	radar product	catalogue	radarproduct
23	Datums	catalogue	datum
24	Resampling Method	catalogue	resamplingmethod
25	File Format	catalogue	fileformat
26	Order Status	catalogue	orderstatus
27	Delivery Method	catalogue	deliverymethod
28	Order	catalogue	order
29	Record	catalogue	searchrecord
30	Order Status History	catalogue	orderstatushistory
31	Search	catalogue	search
32	Clip	catalogue	clip
33	Visit	catalogue	visit
34	visitor report	catalogue	visitorreport
35	User Profile	catalogue	sacuserprofile
36	Sensor	acscatalogue	sensor
37	Data Mode	acscatalogue	datamode
38	Ellipsoid Type	acscatalogue	ellipsoidtype
39	Ers Comp Mode	acscatalogue	erscompmode
40	File Type	acscatalogue	filetype
41	Satellite	acscatalogue	satellite
42	Spot Acquisition Mode	acscatalogue	spotacquisitionmode
43	Station	acscatalogue	station
44	Superclass	acscatalogue	superclass
45	Header Type	acscatalogue	headertype
46	Medium	acscatalogue	medium
47	Localization	acscatalogue	localization
48	Segment Common	acscatalogue	segmentcommon
49	Model	acscatalogue	scene
50	Aux File	acscatalogue	auxfile
51	Spot Segment	acscatalogue	spotsegment
52	Landsat Segment	acscatalogue	landsatsegment
53	Ers Segment 	acscatalogue	erssegment
54	Noaa Segment	acscatalogue	noaasegment
55	Orbview Segment	acscatalogue	orbviewsegment
56	Frame Common	acscatalogue	framecommon
57	Spot Frame	acscatalogue	spotframe
58	Landsat Frame	acscatalogue	landsatframe
59	ErsFrame	acscatalogue	ersframe
60	Noaa Frame	acscatalogue	noaaframe
61	Orbview Frame	acscatalogue	orbviewframe
62	Other Frame	acscatalogue	otherframe
63	Ers Calibration Noise	acscatalogue	erscalnoise
64	Ers Doppler Center	acscatalogue	ersdopcent
65	Ers Quality	acscatalogue	ersquality
66	Ers Sample Time	acscatalogue	erssamptime
67	Ers State Vector	acscatalogue	ersstatevector
68	Satellite Relation	acscatalogue	satrelation
69	acs frame	acscatalogue	acsframe
70	avatar	userprofile	avatar
71	email validation	userprofile	emailvalidation
\.


--
-- PostgreSQL database dump complete
--

