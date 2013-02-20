BEGIN;
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
-- Data for Name: dictionaries_processinglevel; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_processinglevel (id, abbreviation, name, description) FROM stdin;
13	L4	Level 4 Value Added	Value added products
1	L1	Level 1 Systematic Corrections	Radiometric corrections of the differences in sensitivy of the detectors based on in-flight calibrations (Level 1A).  Geometric corrections take into account both internal and external orientations of the satellite in relation to the earth to account for scan line misallignment and non-uniform pixel sizes (Level 1B).  Level 1 imagery is often referred to by customers as "raw" imagery as there is still a great deal of processing required before spatial or spectral analysis can be performed.
2	L1A	Level 1A Radiometric 	Radiometric corrections of the differences in sensitivy of the detectors based on in-flight calibrations.
3	L1B	Level 1B Geometric	Geometric corrections take into account both internal and external orientations of the satellite in relation to the earth to account for scan line misallignment and non-uniform pixel sizes.
4	L2	Level 2 Georeferenced	Georeferenced into a standard map projection.  Level 2A is geolocated to the satellite predicted position at the time of the acquisition and still has location errors (not recommended for spatial analysis).  Level 2B is geolocated against a georeferenced reference image and rectified using ground control points (GCPs) in both images with a positional accuracy of the spatial resolution of the original image excluding mountainous areas.
5	L2A	Level 2A Projected	Geolocated to the satellite predicted position at the time of the acquisition and still has location errors (not recommended for spatial analysis).
6	L2B	Level 2B GCP Geolocated	Geolocated to a georeferenced reference image and rectified using ground control points (GCPs) in both images with a positional accuracy of the spatial resolution of the original image excluding mountainous areas.
7	L3	Level 3 Orthorectified	Orthorectification using GCP points, reference imagery and a digital elevation model (DEM) to accurately locate areas of high relief.  The positional accuracy is expected to be the same as the spatial resolution of the original image including mountainous areas.
8	L3Aa	Level 3Aa Orthorectified	Orthorectification using GCP points, reference imagery and 20m DEM.  Suitable for spatial analysis including digitising.
9	L3Ab	Level L3Ab Reflectance at Sensor	Reflectance values at top of atmosphere (at scanner reflectance).  Suitable for visual interpretaton, spectral signature analysis, classification and derivation of indices (NDVI, EVI).
10	L3B	Level 3B Mosaic	Mosaic
11	L3PS	Level 3 Pansharpened	Pansharpened
12	L3TC	Level 3 True Colour	Blue band creation for SPOT for natural colour visualisation
\.


--
-- Data for Name: dictionaries_referencesystem; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_referencesystem (id, name, description, abbreviation) FROM stdin;
\.


--
-- Data for Name: dictionaries_scannertype; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_scannertype (id, name, description, abbreviation) FROM stdin;
1	Active Beam	Active Beam Scanner\r\n	ACT
2	Push Broom	Push Broom Optical Scanner\r\n	PB
3	Whisk Broom	Whisk Broom or Cross-track Optical Scanner\r\n	WB
4	Forward Motion Compensation	Forward Motion Compensation factor of 4:1\r\n	FMC
\.


--
-- Data for Name: dictionaries_instrumenttype; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_instrumenttype (id, name, description, abbreviation, operator_abbreviation, is_radar, is_taskable, scanner_type_id, base_processing_level_id, reference_system_id, swath_optical_km, band_number_total, band_type, spectral_range_list_nm, pixel_size_list_m, spatial_resolution_range, quantization_bits, image_size_km, processing_software, keywords) FROM stdin;
1	AMI	Active Microwave Instrument\r\n	AMI	AMI	t	f	1	1	\N	\N	\N			\N		\N			
2	MSI	Multi-Spectral Imager\r\n	MSI	MSI	f	f	4	1	\N	\N	\N			\N		\N			
3	MSS	Multi-Spectral Scanner\r\n	MSS	MSS	f	f	3	1	\N	\N	\N			\N		\N			
4	TM	Thematic Mapper\r\n	TM	TM	f	f	3	1	\N	\N	\N			\N		\N			
6	HRV	High Resolution Visible\r\n	HRV	HRV	f	f	2	1	\N	\N	\N			\N		\N			
8	HRG	High Resolution Geometric\r\n	HRG	HRG	f	t	2	1	\N	\N	\N			\N		\N			
9	HRCCD	High Resolution Couple Charged Device\r\n	HRC	HRCCD	f	f	2	1	\N	\N	\N			\N		\N			
10	MMRS	Multi-Spectral Medium Resolution Scanner\r\n	MMR	MMRS	f	f	2	1	\N	\N	\N			\N		\N			
7	HRVIR	High Resolution Visible and Infra-Red\r\n	HIR	HRVIR	f	f	2	1	\N	\N	\N			\N		\N			
5	ETM+	Enhanced Thematic Mapper Plus\r\n	ETM+	ETM+	f	f	3	1	\N	\N	\N			\N		\N			
\.


--
-- Data for Name: dictionaries_band; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_band (id, instrument_type_id, band_name, band_abbr, band_number, min_wavelength_nm, max_wavelength_nm, pixelsize_resampled_m, pixelsize_acquired_m) FROM stdin;
1	3	Green	G	1	500	600	60	60
2	3	Red	R	2	600	700	60	60
3	3	Near Infrared	NIR	3	700	800	60	60
4	3	Near Infrared 2	NIR2	4	800	1100	60	60
5	4	Blue	B	1	450	520	30	30
6	4	Green	G	2	520	600	30	30
7	4	Red	R	3	630	690	30	30
8	4	Near Infrared	NIR	4	760	900	30	30
9	4	Shortwave Infrared 1	SWIR1	5	1550	1750	30	30
11	4	Shortwave Infrared 2	SWIR2	7	2080	2350	30	30
12	5	Blue	B	1	450	520	30	30
13	5	Green	G	2	520	600	30	30
14	5	Red	R	3	630	690	30	30
15	5	Near Infrared	NIR	4	770	900	30	30
16	5	Shortwave Infrared 1	SWIR1	5	1550	1750	30	30
10	4	Thermal	THM	6	10400	12500	30	120
17	5	Thermal - High gain	THM1	61	10400	12500	30	60
18	5	Thermal - Low gain	THM2	62	10400	12500	30	60
19	5	Shortwave Infrared 2	SWIR2	7	2090	2350	30	30
20	5	Panchromatic	PAN	8	520	900	15	15
21	6	Green	G	1	500	590	20	20
22	6	Red	R	2	610	680	20	20
23	6	Near Infrared	NIR	3	780	890	20	20
24	6	Panchromatic	P	1	510	730	10	10
25	7	Monospectral	M	1	610	680	10	10
26	7	Green	G	1	500	590	20	20
27	7	Red	R	2	610	680	20	20
28	7	Near Infrared	NIR	3	780	890	20	20
29	8	Panchromatic A	A	1	480	710	5	5
30	8	Panchromatic B	B	1	480	710	5	5
32	8	Green	G	1	500	590	10	10
33	8	Red	R	2	610	680	10	10
34	8	Near Infrared	NIR	3	780	890	10	10
39	10	Blue	B	1	480	500	175	175
40	10	Green	G	2	540	560	175	175
41	10	Red	R	3	630	690	175	175
42	10	Near Infrared	NIR	4	795	835	175	175
43	10	Shortwave Infrared	SWIR	5	1550	1700	175	175
44	9	Panchromatic	PAN	1	510	730	20	20
45	9	Blue	B	2	450	520	20	20
46	9	Green	G	3	520	590	20	20
47	9	Red	R	4	630	690	20	20
48	9	Near Infrared	NIR	5	770	890	20	20
38	2	Near Infrared	NIR	3	840	890	6.25	6.25
37	2	Red-edge	RE	2	690	730	6.25	6.25
36	2	Red	R	1	620	680	6.25	6.25
31	8	Panchromatic Resampled	T	1	480	710	2.5	5
49	7	Shortwave Infrared	SWIR	4	1580	1750	20	20
35	8	Shortwave Infrared	SWIR	4	1580	1750	10	20
\.


--
-- Name: dictionaries_band_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_band_id_seq', 49, true);


--
-- Data for Name: dictionaries_spectralgroup; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_spectralgroup (id, name, description, abbreviation) FROM stdin;
1	Multi-spectral	Multi-spectral imagery	MSS
2	Panchromatic	Panchromatic	PAN
3	Thermal	Thermal band collection\r\n	THM
4	Visible RGB	Visible spectrum	RGB
5	Hyperspectral	Hyperspectral	HYP
6	Stereo	Stereo pairs	STE
\.


--
-- Data for Name: dictionaries_spectralmode; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_spectralmode (id, name, description, abbreviation, instrument_type_id, spectralgroup_id) FROM stdin;
14	HRG Panchromatic A	SPOT 5 HRG Panchromatic A spectral bands denoted as A on products	A	8	2
16	HRG Multi-spectral	SPOT 5 HRG Multi-spectral bands denoted as J on products	J	8	1
18	HRVIR Multi-spectral	SPOT 4 HRVIR Multi-spectral bands denoted as I on products	I	7	1
17	HRVIR Monospectral	SPOT 4 HRVIR Panchromatic spectral bands denoted as Monospectral (M) on products	M	7	2
19	HRV Multi-spectral	SPOT 1, 2 or 3 HRV Multi-spectral denoted as X on products	X	6	1
20	HRV Panchromatic	SPOT 1, 2 or 3 HRV Multi-spectral denoted as X on products	P	6	2
25	MSI Multi-spectral	ZA-2 SumbandilaSat MSI Multi-spectral denoted as MSS on products	R3B	2	1
28	MMRS Multi-spectral	SAC-C MMRS Multi-spectral denoted as VNS for Visible, NIR and SWIR on products	VNS	10	1
29	TM RGB	Landsat 4 or 5 Visible RGB bands	RGB	4	4
30	ETM+ RGB	Landsat 7 Visible RGB bands	RGB	5	4
31	MMRS RGB	SAC-C Visible RGB bands	RGB	10	4
32	HRCCD RGB	CBERS-2B Visible RGB bands	RGB	9	4
26	HRCCD Multi-spectral 5 bands	CBERS-2B HRCCD Multi-spectral denoted as 5BF for Visible, NIR and Panchromatic on products	5BF	9	1
33	HRCCD Multi-spectral 3 band	HRCCD Multispectral 3 band combination of Green, Red and Near-infrared denoted as 3BG on the products	3BG	9	1
34	HRCCD Multi-spectral 2 band + Pan	CBERS-2B HRCCD Panchromatic and Multi-spectral denoted as 3BP for Blue, Red and Panchromatic on products	3BP	9	1
35	HRCCD Panchromatic 3 band	CBERS-2B HRCCD Panchromatic and Multi-spectral denoted as 3BP for Blue, Red and Panchromatic on products	3BP	9	2
27	HRCCD Panchromatic 5 band	CBERS-2B HRCCD Panchromatic and Multi-spectral denoted as VNP for Visible, NIR and Panchromatic on products	5BF	9	2
1	ETM+ HRF	Landsat 7 ETM+ Multi-spectral bands denoted as HRF on products	HRF	5	1
2	ETM+ HTM	Landsat 7 ETM+ Thermal bands denoted as HTM on products	HTM	5	3
3	ETM+ HPN	Landsat 7 ETM+ Panchromatic bands denoted as HPN on products	HPN	5	2
4	TM HRF	Landsat 4 or 5 TM Multi-spectral bands denoted as HRF on products	HRF	4	1
5	TM THM	Landsat 4 or 5 TM Thermal bands denoted as HTM on products	THM	4	3
6	MSS	Landsat 1, 2, 3, 4 or 5 MSS Multi-spectral bands denoted as MSS on products	MSS 	3	1
13	HRG Panchromatic	SPOT 5 HRG Panchromatic resampled spectral bands denoted as T on products	T	8	2
15	HRG Panchromatic B	SPOT 5 HRG Panchromatic B spectral bands denoted as B on products	B	8	2
\.


--
-- Data for Name: dictionaries_bandspectralmode; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_bandspectralmode (id, band_id, spectral_mode_id) FROM stdin;
1	29	14
3	31	13
4	32	16
5	33	16
6	34	16
7	35	16
8	26	18
9	27	18
10	28	18
11	49	18
12	25	17
13	21	19
14	22	19
15	23	19
16	24	20
17	36	25
18	37	25
19	38	25
20	45	26
21	46	26
22	47	26
23	48	26
24	44	27
25	39	28
26	40	28
27	41	31
28	42	28
29	43	28
30	1	6
31	2	6
32	3	6
33	4	6
34	5	4
35	6	4
36	7	4
37	8	4
38	9	4
39	11	4
40	10	5
41	12	1
42	13	1
43	14	1
44	15	1
45	16	1
46	19	1
47	17	2
48	18	2
49	20	3
50	5	29
51	6	29
52	7	29
53	12	30
54	13	30
55	14	30
56	39	31
57	40	31
58	45	32
59	46	32
60	47	32
61	41	28
2	30	15
\.


--
-- Name: dictionaries_bandspectralmode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_bandspectralmode_id_seq', 61, true);


--
-- Data for Name: dictionaries_collection; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_collection (id, name, description, institution_id) FROM stdin;
1	SPOT	Système Pour l'Observation de la Terre\r\n	4
2	Landsat	The Landsat program, originally known as the Earth Resources Technology Satellite (ERTS), was proposed in 1965 by the US Geological Survey(USGS) as a civilian satellite program.  NASA started building the first satellite in 1970 and have launched 6 spacecraft successfully (Landsat 6 was lost at launch).  In December 2009 all Landsat archive products were made available free to the public on the USGS website.\r\n	7
3	ZA	South African (ZA) Satellite Program\r\n	1
4	CBERS	China-Brazil Earth Resources Satellite Program\r\n	5
5	SAC	Satélite de Aplicaciones Científicas\r\n	8
6	ERS	European Remote-Sensing Satellite Program\r\n	6
\.


--
-- Name: dictionaries_collection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_collection_id_seq', 6, true);


--
-- Data for Name: dictionaries_foreigncurrency; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_foreigncurrency (id, abbreviation, name, conversion_rate) FROM stdin;
\.


--
-- Name: dictionaries_foreigncurrency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_foreigncurrency_id_seq', 1, false);


--
-- Data for Name: dictionaries_radarbeam; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_radarbeam (id, instrument_type_id, band_name, wavelength_cm, looking_distance, azimuth_direction) FROM stdin;
1	1	C-Band	5660	250	23
\.


--
-- Data for Name: dictionaries_imagingmode; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_imagingmode (id, radarbeam_id, name, incidence_angle_min, incidence_angle_max, approximate_resolution_m, swath_width_km, number_of_looks, polarization) FROM stdin;
1	1	ERS-1 AMI SAR Image Mode	23	23	30	100	3	VV
\.


--
-- Name: dictionaries_imagingmode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_imagingmode_id_seq', 1, true);


--
-- Name: dictionaries_instrumenttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_instrumenttype_id_seq', 10, true);


--
-- Data for Name: dictionaries_instrumenttypeprocessinglevel; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_instrumenttypeprocessinglevel (id, instrument_type_id, processinglevel_id, operator_processing_level_name, operator_processing_level_abbreviation) FROM stdin;
1	2	2	Level 1A	L1A
2	2	3	Level 1B	L1B
4	3	3	Level 1G	L1G
5	4	3	Level 1G	L1G
7	5	3	Level 1G	L1G
8	5	8	Level 1T	L1T
6	4	8	Level 1T	L1T
10	6	8	Level 3	L3
12	7	8	Level 3	L3
13	7	11	Level 3	L3
15	8	8	Level 3	L3
16	8	11	Level 3	L3
17	8	12	Level 3	L3
18	7	12	Level 3	L3
19	10	5	Level 2	L2
20	9	5	Level 2	L2
14	8	2	Level 1A	L1A
11	7	2	Level 1A	L1A
9	6	2	Level 1A	L1A
21	7	11	Level 3	L3
22	6	11	Level 3 	L3
23	6	12	Level 3	L3
\.


--
-- Name: dictionaries_instrumenttypeprocessinglevel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_instrumenttypeprocessinglevel_id_seq', 23, true);


--
-- Data for Name: dictionaries_satellite; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_satellite (id, name, description, abbreviation, operator_abbreviation, collection_id, launch_date, status, altitude_km, orbit, revist_time_days, reference_url, license_type_id) FROM stdin;
1	ZA-2 SumbandilaSat	The second South African Satellite ZA-2 renamed as SumbandilaSat\r\n	ZA2	ZASat-002	3	\N		\N		\N		2
2	Landsat 1	Landsat 1\r\n	L1	LS-1	2	\N		\N		\N		1
3	Landsat 2	Landsat 2\r\n	LS2	LS-2	2	\N		\N		\N		1
4	Landsat 3	Landsat 3\r\n	L3-MSS	LS-3	2	\N		\N		\N		1
5	Landsat 4	Landsat 4\r\n	L4	LS-4	2	\N		\N		\N		1
6	Landsat 5	Landsat 5\r\n	L5	LS-5	2	\N		\N		\N		1
7	Landsat 7	Landsat 7\r\n	L7	LS-7	2	\N		\N		\N		1
8	SPOT 1	SPOT 1\r\n	S1	SPOT-1	1	\N		\N		\N		1
9	SPOT 2	SPOT 2	S2	SPOT-2	1	\N		\N		\N		1
10	SPOT 3	SPOT 3\r\n	S3	SPOT-3	1	\N		\N		\N		1
11	SPOT 4	SPOT 4\r\n	S4	SPOT-4	1	\N		\N		\N		1
12	SPOT 5	SPOT 5\r\n	S5	SPOT-5	1	\N		\N		\N		1
13	CBERS-2B	CBERS-2B\r\n	C2B	CBERS-2-B	4	\N		\N		\N		2
14	SAC-C	SAC-C\r\n	SCC	SCC	5	\N		\N		\N		2
16	ERS-2	European Remote-Sensing Satellite-2\r\n	E2	ERS-2	6	\N		\N		\N		1
15	ERS-1	European Remote-Sensing Satellite 1\r\n	E1	ERS-1	6	\N		\N		\N		1
\.


--
-- Data for Name: dictionaries_satelliteinstrument; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_satelliteinstrument (id, name, description, abbreviation, operator_abbreviation, satellite_id, instrument_type_id) FROM stdin;
1	SPOT 5 HRG 1	HRG Camera 1 on the SPOT 5 Satellite\r\n	S5-HRG1	S5-HRG1	12	8
2	SPOT 5 HRG 2	HRG Camera 2 on the SPOT 5 Satellite\r\n	S5-HRG2	S5-HRG2	12	8
3	SPOT 4 HRVIR 1	HRVIR Camera 1 on the SPOT 4 Satellite\r\n	S4-HIR1	S4-HIR1	11	7
4	SPOT 4 HRVIR 2	HRVIR Camera 2 on the SPOT 4 Satellite\r\n	S4-HIR2	S4-HIR2	11	7
5	SPOT 3 HRV 1	HRV Camera 1 on the SPOT 3 Satellite\r\n	S3-HRV1	S3-HRV1	10	6
6	SPOT 3 HRV 2	HRV Camera 2 on the SPOT 3 Satellite\r\n	S3-HRV2	S3-HRV2	10	6
7	SPOT 2 HRV 1	HRV Camera 1 on the SPOT 2 Satellite\r\n	S2-HRV1	S2-HRV1	9	6
8	SPOT 2 HRV 2	HRV Camera 2 on the SPOT 2 Satellite\r\n	S2-HRV2	S2-HRV2	9	6
9	SPOT 1 HRV 1	HRV Camera 1 on the SPOT 1 Satellite\r\n	S1-HRV1	S1-HRV1	9	6
10	SPOT 1 HRV 2	HRV Camera 2 on the SPOT 1 Satellite\r\n	S1-HRV2	S1-HRV2	8	6
11	Landsat 1 MSS	Landsat 1 MSS\r\n	L1-MSS	L1-MSS	2	3
12	Landsat 2 MSS	Landsat 2 MSS\r\n	L2-MSS	L2-MSS	9	3
13	Landsat 3 MSS	Landsat 3 MSS	L3-MSS	L3-MSS	10	3
14	Landsat 4 MSS	Landsat 4 MSS\r\n	L4-MSS	L4-MSS	5	3
15	Landsat 4 TM	Landsat 4 TM\r\n	L4-TM	L4-TM	5	4
16	Landsat 5 MSS	Landsat 5 MSS\r\n	L5-MSS	L5-MSS	6	3
17	Landsat 5 TM	Landsat 5 TM\r\n	L5-TM	L5-TM	6	4
18	Landsat 7 ETM+	Landsat 7 ETM Plus\r\n	L7-ETM+	L7-ETM+	7	5
19	ZA-2 SumbandilaSat MSI	ZA-2 SumbandilaSat MSI\r\n	ZA2-MSI	ZA2-MSI	1	2
20	CBERS-2B HRCCD	CBERS-2B HRCCD\r\n	C2B-CCD	C2B-CCD	13	9
21	ERS-1 AMI	ERS-1 AMI\r\n	E1-AMI	E1-AMI	15	1
22	ERS-2 SMI	ERS-2 SMI\r\n	E2-AMI	E2-AMI	16	1
23	SAC-C MMRS	SAC-C MMRS	SCC-MMRS	SCC-MMRS	14	10
\.


--
-- Data for Name: dictionaries_opticalproductprofile; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_opticalproductprofile (id, satellite_instrument_id, spectral_mode_id) FROM stdin;
2	19	25
3	20	33
4	20	26
5	20	34
6	23	28
7	7	20
8	8	20
9	3	17
10	4	17
11	9	20
12	10	20
13	1	14
14	2	14
15	1	15
16	2	15
17	1	16
18	2	16
19	1	13
20	2	13
21	5	20
22	6	20
23	12	6
24	13	6
25	14	6
26	16	6
27	17	4
28	18	1
29	9	19
30	10	19
31	5	19
32	6	19
33	3	18
34	4	18
35	7	19
36	8	19
\.


--
-- Name: dictionaries_opticalproductprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_opticalproductprofile_id_seq', 36, true);


--
-- Name: dictionaries_processinglevel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_processinglevel_id_seq', 13, true);


--
-- Name: dictionaries_radarbeam_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_radarbeam_id_seq', 1, true);


--
-- Data for Name: dictionaries_radarproductprofile; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_radarproductprofile (id, satellite_instrument_id, imaging_mode_id) FROM stdin;
1	21	1
\.


--
-- Name: dictionaries_radarproductprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_radarproductprofile_id_seq', 1, true);


--
-- Name: dictionaries_referencesystem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_referencesystem_id_seq', 1, false);


--
-- Name: dictionaries_satellite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_satellite_id_seq', 16, true);


--
-- Name: dictionaries_satelliteinstrument_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_satelliteinstrument_id_seq', 23, true);


--
-- Name: dictionaries_scannertype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_scannertype_id_seq', 4, true);


--
-- Name: dictionaries_spectralgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_spectralgroup_id_seq', 6, true);


--
-- Name: dictionaries_spectralmode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_spectralmode_id_seq', 35, true);


--
-- Data for Name: dictionaries_spectralmodeprocessingcosts; Type: TABLE DATA; Schema: public; Owner: dodobas
--

COPY dictionaries_spectralmodeprocessingcosts (id, spectral_mode_id, instrumenttypeprocessinglevel_id, cost_per_scene_in_rands, foreign_currency_id, cost_per_scene_in_foreign) FROM stdin;
1	14	14	400	\N	\N
2	16	14	400	\N	\N
9	1	7	2000	\N	\N
11	4	5	2000	\N	\N
12	15	14	400	\N	\N
13	13	14	800	\N	\N
4	17	11	200	\N	\N
3	18	11	200	\N	\N
5	19	9	200	\N	\N
6	20	9	200	\N	\N
14	6	4	2000	\N	\N
15	4	6	1000	\N	\N
16	1	8	1000	\N	\N
17	13	15	1000	\N	\N
18	16	15	1000	\N	\N
19	16	16	2500	\N	\N
20	16	17	500	\N	\N
21	18	12	1000	\N	\N
22	18	12	1000	\N	\N
23	18	13	2500	\N	\N
24	18	18	500	\N	\N
25	20	10	1000	\N	\N
26	19	10	1000	\N	\N
27	19	22	2500	\N	\N
28	19	23	500	\N	\N
\.


--
-- Name: dictionaries_spectralmodeprocessingcosts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: dodobas
--

SELECT pg_catalog.setval('dictionaries_spectralmodeprocessingcosts_id_seq', 28, true);


--
-- PostgreSQL database dump complete
--

COMMIT;