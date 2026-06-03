--
-- PostgreSQL database dump
--

\restrict Hjmw2XvvWj1haUhw5cb7Hdn4xRwO0ixAAZZZVenMyLVqeTpf34abIVwnbAjrpJO

-- Dumped from database version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.14 (Ubuntu 16.14-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.accounts (
    id integer NOT NULL,
    name text NOT NULL,
    insta_id text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.accounts OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.accounts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.accounts_id_seq OWNER TO postgres;

--
-- Name: accounts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.accounts_id_seq OWNED BY public.accounts.id;


--
-- Name: post_phrase; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.post_phrase (
    id integer NOT NULL,
    text text NOT NULL
);


ALTER TABLE public.post_phrase OWNER TO postgres;

--
-- Name: post_phrase_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.post_phrase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.post_phrase_id_seq OWNER TO postgres;

--
-- Name: post_phrase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.post_phrase_id_seq OWNED BY public.post_phrase.id;


--
-- Name: posts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    account_id integer,
    shortcode text NOT NULL,
    media_type integer,
    caption text,
    hashtags text[],
    status text DEFAULT 'pending'::text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.posts OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_seq OWNER TO postgres;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: accounts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts ALTER COLUMN id SET DEFAULT nextval('public.accounts_id_seq'::regclass);


--
-- Name: post_phrase id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post_phrase ALTER COLUMN id SET DEFAULT nextval('public.post_phrase_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Data for Name: accounts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.accounts (id, name, insta_id, created_at) FROM stdin;
1	_abs_avto_	72291400730	2026-05-21 15:29:19.238833
\.


--
-- Data for Name: post_phrase; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.post_phrase (id, text) FROM stdin;
1	🚗 Приганяємо авто під замовлення з Європи \n💥 Викуп авто після ДТП, з проблемними документами та нерозмитнені (“бляхи”)\n📲 Пишіть: @abs_auto_1
\.


--
-- Data for Name: posts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.posts (id, account_id, shortcode, media_type, caption, hashtags, status, created_at) FROM stdin;
89	1	DYt1YGjANcf	8	✅В НАЯВНОСТІ ✅\n🔥BMW e60 2.5 дизель, автомат 2006.🔥\nВільнюс 🇱🇹 2600€💶\nУкраїна 🇺🇦 3500€💶	{}	completed	2026-05-24 13:04:30.330982
94	1	DY4tZreN6wY	2	#продажавто	{#продажавто}	completed	2026-05-28 17:47:40.070004
90	1	DYzhTZpjbUF	8	✅В НАЯВНОСТІ ✅\n🔥Volvo xc 90, 2,4 дизель, 4х4 автомат,2006 г🔥\nВільнюс🇱🇹 2900€💶\nУкраїна🇺🇦3800€💶	{}	completed	2026-05-26 17:53:50.406258
91	1	DYzhsRrtNMj	2		{}	completed	2026-05-26 17:53:50.417096
86	1	DYkAXpUjYXo	8	✅В НАЯВНОСТІ ✅\n🔥 Toyota Highlander 3,5  ГАЗ/БЕНЗ автомат 2015 рік🔥\nВільнюс🇱🇹7500€💶\nУкраїна 🇺🇦 8500€💶	{}	completed	2026-05-21 15:58:08.386745
87	1	DYkQExDNXTZ	2		{}	completed	2026-05-21 15:58:08.38903
88	1	DYkQNnfNUyZ	2		{}	completed	2026-05-21 15:58:08.392909
92	1	DYzwrdNgESz	8	✅В НАЯВНОСТІ ✅\n🔥Mitsubishi Outlander I| 2.0 DID дизель, механіка,2008🔥\nВільнюс🇱🇹2300€💶\nУкраїна 🇺🇦 3200€💶	{}	completed	2026-05-26 20:23:02.044944
1	1	DFUfxmJg4bV	8	❌ПРОДАНА❌\n🔥Mitsubishi Pajero 2002 рік, 3.2 дізель, механіка, 4*4🔥\nКаунасі🇱🇹3000€💶\nУкраїні🇺🇦4000€💶	{}	completed	2026-05-21 15:58:07.95882
2	1	DFUkwluAMQ8	8	❌ПРОДАНА❌\n🔥Audi A6 2007 рік, 3.0 дізель, автомат🔥\nКаунасі🇱🇹2200€💶\nУкраїні🇺🇦3200€💶	{}	completed	2026-05-21 15:58:07.973909
3	1	DFUk-HygWzZ	8	❌ПРОДАНА❌\n🔥Audi A6 2007 рік, 3.0 дізель, автомат,2006🔥\nКаунасі🇱🇹2200€💶\nУкраїні🇺🇦3200€💶	{}	completed	2026-05-21 15:58:07.978853
4	1	DFlwx_TNNE7	8	❌ПРОДАНА❌\n🔥BMW X5 E53 3.0 дизель,автомат,4*4,2006 рік🔥\nКаунасі🇱🇹3500€💶\nУкраїні🇺🇦4500€💶	{}	completed	2026-05-21 15:58:07.984108
5	1	DFpeKB6ACWP	8	❌ПРОДАНА❌\n🔥BMW X5 3.0 дизель, автомат,4*4,2006 рік🔥\nКаунасі🇱🇹3400€💶\nУкраїні🇺🇦4400€💶	{}	completed	2026-05-21 15:58:07.990926
6	1	DF0i4YaAueV	8	❌ПРОДАНА❌\n🔥Audi A6 2005 рік, 3.0 дізель, автомат, quattro,2007🔥\nКаунасі 🇱🇹2200€💶\nУкраїні🇺🇦 3200€💶	{}	completed	2026-05-21 15:58:07.997336
7	1	DF7him3gvvh	8	❌ПРОДАНА❌\n🔥Audi A62005 рік, 3.0 дізель, автомат, quattro,2007🔥Каунасі🇱🇹2300€💶\nУкраїні🇺🇦3300€💶	{}	completed	2026-05-21 15:58:08.001425
8	1	DHRePehAQ-D	8	❌ПРОДАНА❌\n🔥Audi A6 2006 рік, 3.0 дізель, автомат,2006🔥\nКаунасі🇱🇹2200€💶\nУкраїні🇺🇦3200€💶	{}	completed	2026-05-21 15:58:08.014049
9	1	DHYN7PnNKrX	8	❌ПРОДАНА❌\n🔥BMW e46 2001 рік 2.0 дізель, механіка,2004🔥\nКаунасі🇱🇹1550€💶\nУкраїні🇺🇦2400€💶	{}	completed	2026-05-21 15:58:08.017635
10	1	DHcDNW1tXUz	8	❌ПРОДАНА❌\n🔥Audi A4Б7 2006 рік, 2.5 дізель,механіка,2006🔥\nКаунас🇱🇹2000€💶\nУкраїна🇺🇦3000€💶	{}	completed	2026-05-21 15:58:08.020541
11	1	DPtXG7ojLNd	8	❌ПРОДАНА❌\n🔥BMW X5 e70 , 3.0 дизель, автомат, 4x4, 2007рік🔥\nВільнюс🇱🇹3600€💶\nУкраїна 🇺🇦 4500€💶	{}	completed	2026-05-21 15:58:08.024413
12	1	DPyCxt_DAyH	8	❌ПРОДАНА❌\n🔥BMW e60 , 3.0 дизель ,автомат,2004🔥\nВильнюс🇱🇹 2600€💶\nУкраїна 🇺🇦 3500€💶	{}	completed	2026-05-21 15:58:08.027409
13	1	DRMu7JLDBWM	8	❌ПРОДАНА❌\n🔥ML320 164 , 3.0 дизель, механіка,4x4, 2007рік🔥\nВільнюс🇱🇹3000€💶\nУкраїна 🇺🇦 3900€💶	{}	completed	2026-05-21 15:58:08.030249
14	1	DRSEbgqDFZx	8	❌ПРОДАНА❌\n🔥Audi a4 b7 2,0 дизель, механіка,2007рік🔥\nВільнюс🇱🇹1200€💶\nУкраїна 🇺🇦 2100€💶	{}	completed	2026-05-21 15:58:08.033738
15	1	DRcB_xxDByD	8	❌ПРОДАНА❌\n🔥 Volvo v50 2,0 дизель ,механіка,2007🔥\n🇱🇹Вільнюсі 1000€💶\n🇺🇦Україна  1900 €💶	{}	completed	2026-05-21 15:58:08.038057
16	1	DRcIjRFDMiS	8	❌ПРОДАНА❌\n🔥 Lexus is220 ,2.2дизель, механіка, 2008🔥\n🇱🇹Вільнюсі 2100€💶\n🇺🇦Україна 3000€💶	{}	completed	2026-05-21 15:58:08.042529
17	1	DR1o-XFDdW9	8	❌ПРОДАНА❌\n🔥 Volkswagen Touran ,2.0 дизель, автомат, 2007🔥\n🇱🇹Вільнюсі 900€💶\n🇺🇦Україна 1800€💶	{}	completed	2026-05-21 15:58:08.046574
18	1	DR1pWrkjQ3i	8	❌ПРОДАНА❌\n🔥 Volvo v50 1,6 дизель, механіка, 2012🔥\n🇱🇹Вільнюсі 1500€💶\n🇺🇦Україна  2400€ 💶	{}	completed	2026-05-21 15:58:08.051557
19	1	DR4hs9IDM2_	8	❌ПРОДАНА❌\n🔥Audi Quattro a6c6, 3.0 , 4x4,дизель,механіка,2007рік🔥\nВільнюс🇱🇹2000€💶\nУкраїна 🇺🇦 2900€💶	{}	completed	2026-05-21 15:58:08.057627
20	1	DR4h5ASDGEd	8	❌ПРОДАНА❌\n🔥КіА соренто 2,5, 4x4, дизель, механіка 2007рік🔥\nВільнюс🇱🇹2100€💶\nУкраїна 🇺🇦 3000€💶	{}	completed	2026-05-21 15:58:08.061856
21	1	DSGCGa3gA9L	8	❌ПРОДАНА❌\n🔥BMW 530 е60 3,0,дизель, механіка 2005🔥\nВільнюс🇱🇹2200€💶\nУкраїна 🇺🇦 3100€💶	{}	completed	2026-05-21 15:58:08.070931
22	1	DSKv61cjGwT	8	❌ПОДАНА❌\n🔥Hyundai sanfe , 2,2 , 4x4,дизель, механіка, 2008рік🔥\nВільнюс🇱🇹2200€💶\nУкраїна 🇺🇦 3100€💶	{}	completed	2026-05-21 15:58:08.077847
23	1	DTDFXOPDRXW	8	❌ПРОДАНА❌\n🔥Audi Quattro a6c6, 3.0 , 4x4,дизель, механіка,2006рік🔥 \nВільнюс🇱🇹1900€💶\nУкраїна 🇺🇦 2800€💶	{}	completed	2026-05-21 15:58:08.082583
24	1	DTDPlKpjWli	8	❌ПРОДАНА❌\n🔥КіА соренто 2,5, 4x4, дизель, механіка 2005рік🔥\nВільнюс🇱🇹2000€💶\nУкраїна 🇺🇦 2900€💶	{}	completed	2026-05-21 15:58:08.08868
25	1	DTNNQ73DXoQ	8	❌ПРОДАНА❌\n🔥Audi Quattro a6c6, 3.0 , 4x4,дизель, механіка 2005рік🔥\nВільнюс🇱🇹1900€💶\nУкраїна 🇺🇦 2800€💶	{}	completed	2026-05-21 15:58:08.093048
26	1	DTaoABWjL4A	8	❌ПРОДАНА❌\n🔥Volvo xc 90 , 2,4, 4x4, дизель, механіка, 2009🔥\nВільнюс🇱🇹3000€💶\nУкраїна 🇺🇦 3900€💶	{}	completed	2026-05-21 15:58:08.096619
27	1	DTcnt48DQNE	8	❌ПРОДАНА❌\n🔥Skoda super B 2,0, дизель, механіка 2008🔥\nВільнюс🇱🇹1200€💶\nУкраїна 🇺🇦 2100€💶	{}	completed	2026-05-21 15:58:08.103811
28	1	DTcwaBfjcM1	8	❌ПРОДАНА❌\n🔥TOYOTA RAV4 , 2,2 , 4x4, дизель, механіка 2008рік🔥\nВільнюс🇱🇹2900€💶\nУкраїна 🇺🇦3800€💶	{}	completed	2026-05-21 15:58:08.107349
29	1	DTgWV_7gFjI	8	❌ПРОДАНА❌\n🔥 Volkswagen Touran ,1,9 дизель, механіка,2006🔥\n🇱🇹Вільнюсі 1100€💶\n🇺🇦Україна 2000€💶	{}	completed	2026-05-21 15:58:08.111058
30	1	DUA9EjvDFT_	8	❌ПРОДАНА❌\n🔥Audi Quattro a6c6, 3.0 , 4x4,дизель, механіка,2006рік🔥\nВільнюс🇱🇹2000€💶\nУкраїна 🇺🇦 2900€💶	{}	completed	2026-05-21 15:58:08.114421
31	1	DUA9c6MjOib	8	❌ПРОДАНА❌\n🔥Volvo xc 90 , 2,4, 4x4, дизель, механіка, 2005🔥\nВільнюс🇱🇹2700€💶\nУкраїна 🇺🇦 3600€💶	{}	completed	2026-05-21 15:58:08.117618
32	1	DUA-GlhDP9O	8	❌ПРОДАНА❌\n🔥TOYOTA AVENSIS, 2,2, дизель, механіка 2009 рік🔥\nВільнюс🇱🇹1400💶\nУкраїна 🇺🇦2300€💶	{}	completed	2026-05-21 15:58:08.12104
33	1	DUA_zrBjP10	8	❌ПРОДАНА❌\n🔥ML320 164 , 3,2 газ-бензин ,механіка,4x4,2003🔥\nВільнюс🇱🇹2000€💶\nУкраїна 🇺🇦 2900€💶	{}	completed	2026-05-21 15:58:08.123916
34	1	DUlLll-jZ3r	8	❌ПРОДАНА❌\n🔥BMW X5 e53 m57,3.0 дизель, механіка,4x4, 2006 рік 🔥\nВільнюс🇱🇹3500€💶\nУкраїна 🇺🇦 4400€💶	{}	completed	2026-05-21 15:58:08.127648
35	1	DUz5F-cDTWX	8	❌ПРОДАНА❌\n🔥 Audi A6C6 Рест ,2.7 дизель,автомат, 2010рiк🔥\nВільнюс 🇱🇹2700€💶\nУкраїна 🇺🇦 3600€💶	{}	completed	2026-05-21 15:58:08.132484
36	1	DU07y1cDTYV	8	❌ПРОДАНА❌\n🔥Honda Accord VII 2.2 i-CTDi, дизель, механіка 2004🔥\nВільнюс🇱🇹1000€💶\nУкраїна 🇺🇦1900 €💶	{}	completed	2026-05-21 15:58:08.140249
37	1	DU5kC7MjY5i	8	❌ПРОДАНА❌\n🔥Volkswagen Golf 5 2,0 дизель, механіка ,2008 рік🔥\nВільнюс🇱🇹800€💶\nУкраїна 🇺🇦 1800€💶	{}	completed	2026-05-21 15:58:08.149512
38	1	DU5uhe0jHT3	8	❌ПРОДАНА❌\n🔥Audi Quattro a6c6, 3.0 дизель , механіка,4x4, 2006рік🔥\nВільнюс🇱🇹2000€💶\nУкраїна 🇺🇦 2900€💶	{}	completed	2026-05-21 15:58:08.154566
39	1	DU5xFm7jATR	8	❌ПРОДАНА❌\n🔥BMW 7 Series 4.4 дизель,механіка, 2010 рік 🔥. \nВільнюс🇱🇹2500€💶\nУкраїна 🇺🇦 3400€💶	{}	completed	2026-05-21 15:58:08.159907
40	1	DU50azbDMqI	8	❌У ПРОДАЖУ❌\n🔥BMW 730b m57, дизель, механіка, 2007рік🔥\nВільнюс🇱🇹2600€💶\nУкраїна 🇺🇦 3500€💶	{}	completed	2026-05-21 15:58:08.163781
41	1	DU51HsBDJMK	8	❌ПРОДАНА❌\n🔥Opel Vectra C 1.9 CDTI 1,9  діз ,механіка, 2009рік🔥\nВільнюс🇱🇹800€💶\nУкраїна 🇺🇦 1700€💶	{}	completed	2026-05-21 15:58:08.168478
42	1	DU8YNI_jKTO	8	❌ПРОДАНА❌\n🔥Suzuki Grand Vitara, 2.0 дизель, механіка, 4x4,2009🔥\nВільнюс🇱🇹2400€💶\nУкраїна 🇺🇦 3300€💶	{}	completed	2026-05-21 15:58:08.172645
43	1	DVQoYTZDSlG	8	❌ПРОДАНА❌\n🔥 Volvo v50 2,0  дизель ,механіка,2011🔥\n🇱🇹Вільнюсі 1500€💶\n🇺🇦Україна  2400€💶	{}	completed	2026-05-21 15:58:08.178441
44	1	DVQ0pPGjPn7	8	❌ПРОДАНА❌\n🔥 Volvo v50 2,0  дизель, механіка ,2010 ресталіг🔥\n🇱🇹Вільнюсі 1700€💶\n🇺🇦Україна  2600€💶	{}	completed	2026-05-21 15:58:08.183845
45	1	DVTjKtrDLUO	8	❌ПРОДАНА❌\n🔥Volvo xc 90 , 2,4,дизель, 4x4 автомат ,2005🔥\nВільнюс🇱🇹2700€💶\nУкраїна 🇺🇦 3600€💶	{}	completed	2026-05-21 15:58:08.187405
46	1	DVTjcBojHUf	8	❌ПРОДАНА❌\n🔥Volvo xc 90 , 2,4 дизель, автомат,4x4,2005🔥\nВільнюс🇱🇹2800€💶\nУкраїна 🇺🇦 3700€💶	{}	completed	2026-05-21 15:58:08.190602
47	1	DVTpj66DMNx	8	❌ПРОДАНА❌\n🔥Opel Astra III 1.9 CDT| дизель , механіка,2007🔥\nВільнюс🇱🇹600€💶\nУкраїна 🇺🇦1500 €💶	{}	completed	2026-05-21 15:58:08.193523
48	1	DVV8k-LDN7E	8	❌ПРОДАНА❌\n🔥 ,Honda Accord VIII 2.0 ГАЗ/БЕНЗ ,автомат, 2013рiк🔥\nВільнюс 🇱🇹2000€💶\nУкраїна 🇺🇦 2900€💶	{}	completed	2026-05-21 15:58:08.203793
49	1	DVV83IyjHIE	8	❌ПРОДАНА❌\n🔥Opel Astra III 1.9 CDT| , дизель , механіка, 2008🔥\nВільнюс🇱🇹600€💶\nУкраїна 🇺🇦1500 €💶	{}	completed	2026-05-21 15:58:08.207339
50	1	DVay-8MDedX	8	❌ПРОДАНА❌\n🔥Audi a6c5 1,9 дизель ,механіка, 2003 🔥\nВільнюс🇱🇹800€💶\nУкраїна 🇺🇦 1600€💶	{}	completed	2026-05-21 15:58:08.210865
51	1	DVgc9nEjLIq	8	❌ПРОДАНА❌\n🔥Opel Vectra C 1.9 CDTI Elegance 1,9 диз,механік, 2005🔥\nВільнюс🇱🇹600€💶\nУкраїна 🇺🇦 1500€💶	{}	completed	2026-05-21 15:58:08.216615
52	1	DVoPIMojNrK	8	❌ПРОДАНА❌\n🔥 Lexus is220 ,2.2дизель ,механіка ,2009🔥\n🇱🇹Вільнюсі 2100💶\n🇺🇦Україна 3000 💶	{}	completed	2026-05-21 15:58:08.220768
53	1	DVxvaL8DQJx	8	❌ПРОДАНА❌\n🔥Volkswagen Touareg 2,5 дизель, механіка,4х4,2005🔥\nВільнюс🇱🇹2800€💶\nУкраїна🇺🇦 3700€💶	{}	completed	2026-05-21 15:58:08.224624
54	1	DV8PSqnDZ0E	8	❌ПРОДАНА❌\n🔥Opel Antara 2.0 CDTI,дизель,4x4,механіка ,2010🔥\nВільнюс🇱🇹2300€💶\nУкраїна 🇺🇦 3200€💶	{}	completed	2026-05-21 15:58:08.229624
55	1	DV8P4vZDcN9	8	❌ПРОДАНА❌\n🔥Saab 9-3 (2G)  1.9tid дизель , механіка, 2008🔥\nВільнюс🇱🇹600€💶\nУкраїна 🇺🇦 1500€💶	{}	completed	2026-05-21 15:58:08.234551
56	1	DV8SCUsDRrz	8	🔥Opel Vivaro 2.0 CDTI MT 2010🔥\nВільнюс🇱🇹2000💶\nУкраїна 🇺🇦 3000€💶 \n\nНадійний дизель. Двигун, коробка, ходова в нормі. Кузов без іржі, салон чистий. Сів і поїхав.	{}	completed	2026-05-21 15:58:08.239425
57	1	DWBz6VgjO3O	8	❌ПРОДАНА❌\n🔥 Volkswagen Touran ,1,9 дизель ,механіка, 2006🔥\n🇱🇹Вільнюсі 1000€💶\n🇺🇦Україна 1900€💶	{}	completed	2026-05-21 15:58:08.249523
58	1	DWJkxi_DNg9	8	❌ПРОДАНА❌\n🔥BMW 316i e46 1,6 Benz , механіка, 2000рік🔥\nЛитва 🇱🇹 1000€💶\nУкраїна 🇺🇦 1600€💶	{}	completed	2026-05-21 15:58:08.258086
59	1	DWOoDqojUva	8	❌ПРОДАНА❌\n🔥Audi Quattro a4B73.0 , 4x4, 2007рік🔥\nВільнюс🇱🇹1700💶\nУкраїна 🇺🇦 2600€💶	{}	completed	2026-05-21 15:58:08.262553
60	1	DWOpInpjTiF	8	❌ПРОДАНА❌\n🔥Volkswagen Golf 5 1,9дизель, 4х4, механіка,2007🔥\nВільнюс🇱🇹1100€💶\nУкраїна 🇺🇦 2000€💶	{}	completed	2026-05-21 15:58:08.266561
61	1	DWRPJ1ujZMW	8	❌ПІД ЗАДАТКОМ❌\n🔥 Volkswagen Touran ,1,9 дизель ,автомат,2006🔥\n🇱🇹Вільнюсі 1500€💶\n🇺🇦Україна 2400€💶	{}	completed	2026-05-21 15:58:08.270079
62	1	DWRcr3ujIXy	8	❌ПРОДАНА❌\n🔥Volkswagen Touareg 3,0 дизель,автомат,4х4,2005🔥\nВільнюс🇱🇹3000€💶\nУкраїна🇺🇦 3900€💶	{}	completed	2026-05-21 15:58:08.274021
63	1	DWWg_ltjAT6	8	❌ПРОДАНА❌\n🔥Honda Accord VII 2.2дизель i-CTDi , механіка,2004🔥\nВільнюс🇱🇹1100€💶\nУкраїна 🇺🇦2000 €💶	{}	completed	2026-05-21 15:58:08.27887
64	1	DWbc9hzjY7x	8	❌ПРОДАНА❌\n🔥Volvo xc 90 , 2,4 дизель, 4x4 автомат ,2006🔥\nВільнюс🇱🇹2900€💶\nУкраїна 🇺🇦 3800€💶	{}	completed	2026-05-21 15:58:08.283158
65	1	DWbddJkjXvC	8	❌ПРОДАНА❌\n🔥Audi a4 b7 1,9 дизель, механіка,2008рік🔥\nВільнюс🇱🇹1400€💶\nУкраїна 🇺🇦 2300€💶	{}	completed	2026-05-21 15:58:08.288063
66	1	DWgOaOPAGn1	8	❌ПРОДАНА❌\n🔥Audi Quattro a6c6, 3.0 дизель,автомат,4x4, 2007рік🔥\nВільнюс🇱🇹2500€💶\nУкраїна 🇺🇦 3500€💶	{}	completed	2026-05-21 15:58:08.301235
67	1	DWglaNMjcDQ	8	❌ПІД ЗАДАТКОМ❌\n🔥Honda CR-V 2.2 i-DTEC (150 л.с.) 6-меx,4x4, 2007рік🔥\nВільнюс🇱🇹2600💶\nУкраїна 🇺🇦 3500€💶	{}	completed	2026-05-21 15:58:08.309954
68	1	DWoHiWNDZeb	8	❌У ПРОДАЖІ ❌\n🔥Mitsubishi Grandis 2.0 DI-D (136 л.с.)механіка,2009🔥\nВільнюс🇱🇹1200€💶\nУкраїна 🇺🇦 2100€💶	{}	completed	2026-05-21 15:58:08.316232
69	1	DWoH8s4jeeu	8	❌ПРОДАНА ❌\n🔥 Volkswagen Touran ,2,0 дизель,механіка,2006🔥\n🇱🇹Вільнюсі 1100€💶\n🇺🇦Україна 2000€💶	{}	completed	2026-05-21 15:58:08.320193
70	1	DWrOodUDcV0	8	❌ПРОДАНА ❌\n🔥Mitsubishi Outlander I| 2.0 DID дизель, механіка,2010🔥\nВільнюс🇱🇹2300€💶\nУкраїна 🇺🇦 3100€💶	{}	completed	2026-05-21 15:58:08.32454
71	1	DW1lJU3jY3t	8	❌ПРОДАНА❌\n🔥Audi A4 Quattro (4*4) 2.5 дизель, механіка, 2006 р🔥\nВільнюс 🇱🇹1400€💶\nУкраїна 🇺🇦2400€💶	{}	completed	2026-05-21 15:58:08.327838
72	1	DW81N0yjWeg	8	❌ПРОДАНА❌\n🔥КіА соренто 2,5 дизель, автомат,4x4, 2007 рік🔥\nВільнюс🇱🇹2000€💶\nУкраїна 🇺🇦 3000€💶	{}	completed	2026-05-21 15:58:08.331309
73	1	DXHbWfrjDWk	8	✅В НАЯВНОСТІ ✅\n🔥 Volvo v50 2,0 дизель ,механіка,2007🔥\n🇱🇹Вільнюсі 900€💶\n🇺🇦Україна  1800 €💶	{}	completed	2026-05-21 15:58:08.334689
74	1	DXMJzsLDSqJ	8	❌ПРОДАНА❌\n🔥Audi a6c6, 2,0 діз механіка 2007рік🔥\nВільнюс🇱🇹1800€💶\nУкраїна 🇺🇦 2700€💶	{}	completed	2026-05-21 15:58:08.338811
75	1	DXM0KypjX1f	8	❌ПІД ЗАДАТКОМ❌\n🔥TOYOTA RAV4 , 2,2 , 4x4, дизель, механіка 2008рік🔥\nВільнюс🇱🇹2900€💶\nУкраїна 🇺🇦3800€💶	{}	completed	2026-05-21 15:58:08.344748
76	1	DXM6M-hALbp	8	❌ПРОДАНА❌\n🔥Volkswagen Golf 5 2,0 дизель, механіка,2008🔥\nВільнюс🇱🇹800€💶\nУкраїна 🇺🇦 1700€💶	{}	completed	2026-05-21 15:58:08.349495
77	1	DXOxRiUjTNr	8	✅В НАЯВНОСТІ ✅\n🔥 Volvo v40,1,8 бензин,механіка,2009🔥\n🇱🇹Вільнюсі 900€💶\n🇺🇦Україна  1800 €💶	{}	completed	2026-05-21 15:58:08.353652
78	1	DXPApPnDbuH	8	✅В НАЯВНОСТІ ✅\n🔥 Audi A6C6/4F (FL) 2,0 Бенз TFSI, автомат,2011🔥\nВільнюс🇱🇹 2500€💶\nУкраїна🇺🇦 3500€💶	{}	completed	2026-05-21 15:58:08.357785
79	1	DXeIO9LDYwO	8	✅В НАЯВНОСТІ ✅🔥Volkswagen Golf 5 plus 1,9дизель,механіка,2008🔥\nВільнюс🇱🇹1200€💶\nУкраїна 🇺🇦 2100€💶	{}	completed	2026-05-21 15:58:08.362884
80	1	DXeRM7jjWGN	8	❌ПРОДАНА❌\n🔥TOYOTA RAV4 , 2,2 , 4x4, дизель, механіка 2009рік🔥\nВільнюс🇱🇹2100€💶\nУкраїна 🇺🇦3000€💶	{}	completed	2026-05-21 15:58:08.367506
81	1	DXjzhKzjMC5	8	✅В НАЯВНОСТІ ✅\nMitsubishi Pajero Sport 2.5 TD механік 4х4\n🇱🇹Вільнюсі 2800€💶\n🇺🇦Україна  3700€💶	{}	completed	2026-05-21 15:58:08.370794
82	1	DXj0GYLDJ4g	8	✅В НАЯВНОСТІ ✅\n🔥Volkswagen Tiguan 2.0 TDI механік 2012 рік🔥\nВільнюс🇱🇹3000€💶\nУкраїна 🇺🇦 4000€💶	{}	completed	2026-05-21 15:58:08.374425
83	1	DXj1Cz3jL04	8	❌ПРОДАНА❌\n🔥Skoda Octavia 1Z 1.9 TDI  механік 2012 рік🔥\nВільнюс🇱🇹1000€💶\nУкраїна 🇺🇦 1900€💶	{}	completed	2026-05-21 15:58:08.377285
84	1	DYPLFA4AF-Q	8	✅В НАЯВНОСТІ ✅\n🔥Audi а4b7 sline 2.5 дизель , автомат 2008 рік🔥\nВільнюс 🇱🇹 1500€💶\nУкраїна 🇺🇦 2400€💶	{}	completed	2026-05-21 15:58:08.38046
85	1	DYPXsJPjdbl	8	❌ПРОДАНА❌\n🔥Volvo xc 90 , 2,4 дизель, 4x4 механіка ,2005🔥\nВільнюс🇱🇹2100€💶\nУкраїна 🇺🇦 3000€💶	{}	completed	2026-05-21 15:58:08.383849
93	1	DY2SMMFDWL2	8	✅В НАЯВНОСТІ ✅\n🔥Mitsubishi Outlander I| 2.0 DID дизель, механіка,2008🔥\nВільнюс🇱🇹2300€💶\nУкраїна 🇺🇦 3300€💶	{}	completed	2026-05-27 19:27:15.76153
\.


--
-- Name: accounts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.accounts_id_seq', 1, true);


--
-- Name: post_phrase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.post_phrase_id_seq', 1, true);


--
-- Name: posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.posts_id_seq', 94, true);


--
-- Name: accounts accounts_insta_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_insta_id_key UNIQUE (insta_id);


--
-- Name: accounts accounts_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_name_key UNIQUE (name);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: post_phrase post_phrase_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.post_phrase
    ADD CONSTRAINT post_phrase_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: posts posts_shortcode_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_shortcode_key UNIQUE (shortcode);


--
-- Name: idx_posts_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_posts_status ON public.posts USING btree (status);


--
-- Name: posts posts_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict Hjmw2XvvWj1haUhw5cb7Hdn4xRwO0ixAAZZZVenMyLVqeTpf34abIVwnbAjrpJO

