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
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: timlinux
--

SELECT pg_catalog.setval('auth_permission_id_seq', 246, true);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: timlinux
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add registration profile	9	add_registrationprofile
26	Can change registration profile	9	change_registrationprofile
27	Can delete registration profile	9	delete_registrationprofile
28	Can add mission	10	add_mission
29	Can change mission	10	change_mission
30	Can delete mission	10	delete_mission
31	Can add mission sensor	11	add_missionsensor
32	Can change mission sensor	11	change_missionsensor
33	Can delete mission sensor	11	delete_missionsensor
34	Can add acquisition mode	12	add_acquisitionmode
35	Can change acquisition mode	12	change_acquisitionmode
36	Can delete acquisition mode	12	delete_acquisitionmode
37	Can add sensor type	13	add_sensortype
38	Can change sensor type	13	change_sensortype
39	Can delete sensor type	13	delete_sensortype
40	Can add Processing Level	14	add_processinglevel
41	Can change Processing Level	14	change_processinglevel
42	Can delete Processing Level	14	delete_processinglevel
43	Can add Projection	15	add_projection
44	Can change Projection	15	change_projection
45	Can delete Projection	15	delete_projection
46	Can add institution	16	add_institution
47	Can change institution	16	change_institution
48	Can delete institution	16	delete_institution
49	Can add license	17	add_license
50	Can change license	17	change_license
51	Can delete license	17	delete_license
52	Can add quality	18	add_quality
53	Can change quality	18	change_quality
54	Can delete quality	18	delete_quality
55	Can add creating software	19	add_creatingsoftware
56	Can change creating software	19	change_creatingsoftware
57	Can delete creating software	19	delete_creatingsoftware
58	Can add generic product	20	add_genericproduct
59	Can change generic product	20	change_genericproduct
60	Can delete generic product	20	delete_genericproduct
61	Can add optical product	21	add_opticalproduct
62	Can change optical product	21	change_opticalproduct
63	Can delete optical product	21	delete_opticalproduct
64	Can add radar product	22	add_radarproduct
65	Can change radar product	22	change_radarproduct
66	Can delete radar product	22	delete_radarproduct
67	Can add Datums	23	add_datum
68	Can change Datums	23	change_datum
69	Can delete Datums	23	delete_datum
70	Can add Resampling Method	24	add_resamplingmethod
71	Can change Resampling Method	24	change_resamplingmethod
72	Can delete Resampling Method	24	delete_resamplingmethod
73	Can add File Format	25	add_fileformat
74	Can change File Format	25	change_fileformat
75	Can delete File Format	25	delete_fileformat
76	Can add Order Status	26	add_orderstatus
77	Can change Order Status	26	change_orderstatus
78	Can delete Order Status	26	delete_orderstatus
79	Can add Delivery Method	27	add_deliverymethod
80	Can change Delivery Method	27	change_deliverymethod
81	Can delete Delivery Method	27	delete_deliverymethod
82	Can add Order	28	add_order
83	Can change Order	28	change_order
84	Can delete Order	28	delete_order
85	Can add Record	29	add_searchrecord
86	Can change Record	29	change_searchrecord
87	Can delete Record	29	delete_searchrecord
88	Can add Order Status History	30	add_orderstatushistory
89	Can change Order Status History	30	change_orderstatushistory
90	Can delete Order Status History	30	delete_orderstatushistory
91	Can add Search	31	add_search
92	Can change Search	31	change_search
93	Can delete Search	31	delete_search
94	Can add Clip	32	add_clip
95	Can change Clip	32	change_clip
96	Can delete Clip	32	delete_clip
97	Can add Visit	33	add_visit
98	Can change Visit	33	change_visit
99	Can delete Visit	33	delete_visit
100	Can add visitor report	34	add_visitorreport
101	Can change visitor report	34	change_visitorreport
102	Can delete visitor report	34	delete_visitorreport
103	Can add User Profile	35	add_sacuserprofile
104	Can change User Profile	35	change_sacuserprofile
105	Can delete User Profile	35	delete_sacuserprofile
106	Can add Sensor	36	add_sensor
107	Can change Sensor	36	change_sensor
108	Can delete Sensor	36	delete_sensor
109	Can add Data Mode	37	add_datamode
110	Can change Data Mode	37	change_datamode
111	Can delete Data Mode	37	delete_datamode
112	Can add Ellipsoid Type	38	add_ellipsoidtype
113	Can change Ellipsoid Type	38	change_ellipsoidtype
114	Can delete Ellipsoid Type	38	delete_ellipsoidtype
115	Can add Ers Comp Mode	39	add_erscompmode
116	Can change Ers Comp Mode	39	change_erscompmode
117	Can delete Ers Comp Mode	39	delete_erscompmode
118	Can add File Type	40	add_filetype
119	Can change File Type	40	change_filetype
120	Can delete File Type	40	delete_filetype
121	Can add Satellite	41	add_satellite
122	Can change Satellite	41	change_satellite
123	Can delete Satellite	41	delete_satellite
124	Can add Spot Acquisition Mode	42	add_spotacquisitionmode
125	Can change Spot Acquisition Mode	42	change_spotacquisitionmode
126	Can delete Spot Acquisition Mode	42	delete_spotacquisitionmode
127	Can add Station	43	add_station
128	Can change Station	43	change_station
129	Can delete Station	43	delete_station
130	Can add Superclass	44	add_superclass
131	Can change Superclass	44	change_superclass
132	Can delete Superclass	44	delete_superclass
133	Can add Header Type	45	add_headertype
134	Can change Header Type	45	change_headertype
135	Can delete Header Type	45	delete_headertype
136	Can add Medium	46	add_medium
137	Can change Medium	46	change_medium
138	Can delete Medium	46	delete_medium
139	Can add Localization	47	add_localization
140	Can change Localization	47	change_localization
141	Can delete Localization	47	delete_localization
142	Can add Segment Common	48	add_segmentcommon
143	Can change Segment Common	48	change_segmentcommon
144	Can delete Segment Common	48	delete_segmentcommon
145	Can add Model	49	add_scene
146	Can change Model	49	change_scene
147	Can delete Model	49	delete_scene
148	Can add Aux File	50	add_auxfile
149	Can change Aux File	50	change_auxfile
150	Can delete Aux File	50	delete_auxfile
151	Can add Spot Segment	51	add_spotsegment
152	Can change Spot Segment	51	change_spotsegment
153	Can delete Spot Segment	51	delete_spotsegment
154	Can add Landsat Segment	52	add_landsatsegment
155	Can change Landsat Segment	52	change_landsatsegment
156	Can delete Landsat Segment	52	delete_landsatsegment
157	Can add Ers Segment 	53	add_erssegment
158	Can change Ers Segment 	53	change_erssegment
159	Can delete Ers Segment 	53	delete_erssegment
160	Can add Noaa Segment	54	add_noaasegment
161	Can change Noaa Segment	54	change_noaasegment
162	Can delete Noaa Segment	54	delete_noaasegment
163	Can add Orbview Segment	55	add_orbviewsegment
164	Can change Orbview Segment	55	change_orbviewsegment
165	Can delete Orbview Segment	55	delete_orbviewsegment
166	Can add Frame Common	56	add_framecommon
167	Can change Frame Common	56	change_framecommon
168	Can delete Frame Common	56	delete_framecommon
169	Can add Spot Frame	57	add_spotframe
170	Can change Spot Frame	57	change_spotframe
171	Can delete Spot Frame	57	delete_spotframe
172	Can add Landsat Frame	58	add_landsatframe
173	Can change Landsat Frame	58	change_landsatframe
174	Can delete Landsat Frame	58	delete_landsatframe
175	Can add ErsFrame	59	add_ersframe
176	Can change ErsFrame	59	change_ersframe
177	Can delete ErsFrame	59	delete_ersframe
178	Can add Noaa Frame	60	add_noaaframe
179	Can change Noaa Frame	60	change_noaaframe
180	Can delete Noaa Frame	60	delete_noaaframe
181	Can add Orbview Frame	61	add_orbviewframe
182	Can change Orbview Frame	61	change_orbviewframe
183	Can delete Orbview Frame	61	delete_orbviewframe
184	Can add Other Frame	62	add_otherframe
185	Can change Other Frame	62	change_otherframe
186	Can delete Other Frame	62	delete_otherframe
187	Can add Ers Calibration Noise	63	add_erscalnoise
188	Can change Ers Calibration Noise	63	change_erscalnoise
189	Can delete Ers Calibration Noise	63	delete_erscalnoise
190	Can add Ers Doppler Center	64	add_ersdopcent
191	Can change Ers Doppler Center	64	change_ersdopcent
192	Can delete Ers Doppler Center	64	delete_ersdopcent
193	Can add Ers Quality	65	add_ersquality
194	Can change Ers Quality	65	change_ersquality
195	Can delete Ers Quality	65	delete_ersquality
196	Can add Ers Sample Time	66	add_erssamptime
197	Can change Ers Sample Time	66	change_erssamptime
198	Can delete Ers Sample Time	66	delete_erssamptime
199	Can add Ers State Vector	67	add_ersstatevector
200	Can change Ers State Vector	67	change_ersstatevector
201	Can delete Ers State Vector	67	delete_ersstatevector
202	Can add Satellite Relation	68	add_satrelation
203	Can change Satellite Relation	68	change_satrelation
204	Can delete Satellite Relation	68	delete_satrelation
205	Can add acs frame	69	add_acsframe
206	Can change acs frame	69	change_acsframe
207	Can delete acs frame	69	delete_acsframe
208	Can add avatar	70	add_avatar
209	Can change avatar	70	change_avatar
210	Can delete avatar	70	delete_avatar
211	Can add email validation	71	add_emailvalidation
212	Can change email validation	71	change_emailvalidation
213	Can delete email validation	71	delete_emailvalidation
\.


--
-- PostgreSQL database dump complete
--

