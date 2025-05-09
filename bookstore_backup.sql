--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_stat_statements IS 'track planning and execution statistics of all SQL statements executed';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: books; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.books (
    book_id integer NOT NULL,
    title character varying(255) NOT NULL,
    author character varying(255),
    price numeric(10,2) DEFAULT 19.99,
    stock_quantity integer DEFAULT 1,
    genre character varying(255) DEFAULT 'Unknown'::character varying,
    description text DEFAULT 'This is a placeholder book description.'::text
);


--
-- Name: books_book_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.books_book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: books_book_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.books_book_id_seq OWNED BY public.books.book_id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    name character varying(255),
    email character varying(255) NOT NULL,
    phone_number character varying(20),
    password text,
    is_guest boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    first_name text,
    last_name text,
    address_line1 text,
    address_line2 text,
    city text,
    state text,
    zip_code text
);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: customers_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;


--
-- Name: order_items; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.order_items (
    order_item_id integer NOT NULL,
    order_id integer NOT NULL,
    book_id integer NOT NULL,
    quantity integer NOT NULL
);


--
-- Name: order_items_order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.order_items_order_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: order_items_order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.order_items_order_item_id_seq OWNED BY public.order_items.order_item_id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.orders (
    order_id integer NOT NULL,
    customer_id integer NOT NULL,
    order_date date NOT NULL,
    total_amount numeric(10,2) NOT NULL
);


--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.orders_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: orders_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.orders_order_id_seq OWNED BY public.orders.order_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    role text DEFAULT 'user'::text NOT NULL
);


--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: books book_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.books ALTER COLUMN book_id SET DEFAULT nextval('public.books_book_id_seq'::regclass);


--
-- Name: customers customer_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);


--
-- Name: order_items order_item_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items ALTER COLUMN order_item_id SET DEFAULT nextval('public.order_items_order_item_id_seq'::regclass);


--
-- Name: orders order_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders ALTER COLUMN order_id SET DEFAULT nextval('public.orders_order_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.books (book_id, title, author, price, stock_quantity, genre, description) FROM stdin;
20	Ancient Ruins	Benjamin King	16.49	70	Adventure	This is a placeholder book description.
4	Whispers in the Dark	Jane Smith	9.99	80	Horror	This is a placeholder book description.
9	Echoes of the Past	Amanda Brown	14.25	133	Historical Fiction	This is a placeholder book description.
14	Battle for the Skies	Ava Adams	19.20	93	Action	This is a placeholder book description.
30	The Warlord’s Daughter	Fiona Turner	16.00	99	Fantasy	This is a placeholder book description.
29	Waves of Change	Benjamin Black	21.75	89	Non-Fiction	This is a placeholder book description.
8	The Final Key	Michael Black	11.45	88	Thriller	This is a placeholder book description.
17	The Hacker’s Code	Jack Reynolds	14.99	101	Technology	This is a placeholder book description.
32	Guardians of the Realm	Matthew White	18.00	95	Fantasy	This is a placeholder book description.
19	City of Fire	Olivia Baker	20.99	98	Crime	This is a placeholder book description.
27	Beyond the Stars	Charlotte Brown	23.99	93	Science Fiction	This is a placeholder book description.
33	The Vanishing Point	Grace Lee	19.99	75	Mystery	This is a placeholder book description.
6	Gardens of Tomorrow	Lucas Green	22.00	109	Non-Fiction	This is a placeholder book description.
12	The Last Goodbye	Oscar King	10.75	81	Drama	This is a placeholder book description.
31	Into the Abyss	Hannah Moore	14.25	97	Adventure	This is a placeholder book description.
7	Journey Through Time	Sarah White	18.75	95	Fantasy	This is a placeholder book description.
2	To Kill a Mockingbird	Harper Lee	19.99	100	Classics	This is a placeholder book description.
18	The Phantom of the Opera	Charles Doyle	10.30	128	Classics	This is a placeholder book description.
21	The Forgotten Island	Sophia Clarke	12.85	95	Adventure	This is a placeholder book description.
5	The Mystery of the Lost City	Emily Turner	15.50	197	Adventure	This is a placeholder book description.
11	Code Breaker	Nina Patel	16.99	107	Technology	This is a placeholder book description.
10	The Ocean’s Heart	David Blue	13.00	100	Romance	This is a placeholder book description.
1	The Great Gatsby	F. Scott Fitzgerald	12.99	100	Classic	This is a placeholder book description.
26	Life After Death	Christopher Miller	19.50	100	Drama	This is a placeholder book description.
23	Whispers of the Forest	Isabella King	15.40	100	Horror	This is a placeholder book description.
16	The Secret Library	Grace Harris	17.50	100	Fantasy	This is a placeholder book description.
25	The Golden Compass	Lily Collins	14.75	100	Fantasy	This is a placeholder book description.
28	The Red Knight	Samuel Green	17.30	100	Historical Fiction	This is a placeholder book description.
24	Tales of the Deep	William Johnson	13.55	100	Mystery	This is a placeholder book description.
3	The Silent Sea	John Doe	12.99	100	Science Fiction	This is a placeholder book description.
22	Rising Phoenix	Daniel Lee	18.90	100	Action	This is a placeholder book description.
13	Mysteries of the Mind	Ethan Gray	21.60	100	Psychology	This is a placeholder book description.
15	Shadows of the Moon	Liam Carter	13.80	100	Fantasy	This is a placeholder book description.
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.customers (customer_id, name, email, phone_number, password, is_guest, created_at, first_name, last_name, address_line1, address_line2, city, state, zip_code) FROM stdin;
24	\N	test1@example.com	240-555-9999	scrypt:32768:8:1$Zg4GGz5zHwjyRuvz$0a43fa36867405d0068ec277fc12ac5e7e6920ffd36424a3df318f4080c7f68016413c0874c509c72c4cb58d3e2b5d609c9177bc1da60b2c85e66cae2ff504d6	f	2025-04-16 03:33:49.227586	Reggie	Cosens	123 Test St	123 Test St	Test	Md	99999
25	\N	REggiecosens3@example.com	240-515-0111	scrypt:32768:8:1$y2ipyj87Z60qOV3D$172beba86ede6fa2555e3e3bf9df39f68fc95acb98de146ba7828072ec57ad7053386bd412d02bf92cacdad8454c7916a6ebd9ebdc457003c029e1e0f38e7c4a	f	2025-04-16 21:49:19.098789	Reggie	Cosens	123 Test St	Apt 1	Test	Ca	21740
26	\N	VirginiaSlim@example.com	2405131368	scrypt:32768:8:1$imiFyYU6ZfCBewvv$47f9f89476e31f95fa3dc34b2d2da91f50cb13b850a208b189f4c2b6af748a3f47597123031811d69ab1a6246e6cfd8338b289b2ae6f2a9b7c3dbcf060dcdfaf	f	2025-04-16 21:53:40.868244	Virginia	Slim	123 Test St	Apt 1	Test	Ca	21740
27	\N	ReginaldCosensIII@exa.com	2405131368	scrypt:32768:8:1$CgZVuzNvkLa9JeFK$dde4844f4662d89bef25bba0036d172d04395b0a809230aaf62a726161c3cb625743451531d18d7ac6f82f5511a62bed4dbf3fa6f81aafe51035213c44a1a0fb	f	2025-04-16 22:49:50.887469	Reggie	Cosens	123 Test St	Apt 1	Test	Ca	21740
28	\N	camelmenthol@example.com	2405131368	scrypt:32768:8:1$z0Gt3Kv7PpcS4Fb5$6014aee3df71f5771dc9faaae09e7a1d6e6d11ff3cc9a62f442f037280043a5dd09fbf3a064979461c7e76200a350c17ec44f9f67518293407c061fd2b31a8ab	f	2025-04-16 23:26:38.956402	camel	menthol	123 test st	apt 1	test	ca	21740
29	\N	newport@example.com	2405131368	scrypt:32768:8:1$NYsHriIYx13XoTjJ$3ca8330e7c71221f8899deea5ce00d10e12273c2bd8c62ef7b31aac0882d4538a5022538bef7fdd02de61341bbfc10e7176576d5147a4424442532e645eca092	f	2025-04-16 23:39:04.246236	new	port	123 test st	apt 1	test	ca	21740
30	\N	regular@example.com	2405131368	scrypt:32768:8:1$lcwaFd8pCbdGWK67$316e7283f72a25d54ea2061732ad136315f0d17804e2dd810d9b00881434ea2d8099584f6bd92ee2fda03909e1c35ed5e50cf5ed28cdbc241260c77ec6f6ffdf	f	2025-04-16 23:48:30.48743	new	port	123 test st	apt 1	test	ca	21740
31	\N	test123@example.com	1234454444	scrypt:32768:8:1$FcS0sNxoRQCgFvqk$75a75166350caff38eeb30d0dbd8db38e4dfb1b294144f98ba4b30bc98d75666a602c9a0a54c9d21b81274ad6b29ce38e330a31d167ca1a74d69fddca7918c9c	f	2025-04-17 00:50:32.637005	test	test	123 test st	apt 1	test	ca	21740
32	\N	register@example.com	1234454444	scrypt:32768:8:1$kbRwQPV0RnJIrb2f$9e6b8bdc677471b8a65fe5f7d098f46d992ea54897d7f7e350c677939fe4515c434f2e1354ea6fae3dd1b8c26e7892db4e925198a8110c1d4a04d6f9097dc046	f	2025-04-17 00:54:20.482117	test	test	123 test st	apt 1	test	ca	21740
33	\N	user@example.com	2404131255	scrypt:32768:8:1$RQJwibgTYwgttjhR$ed8b2ed3873509847f7504cacf907d5a0f10c9c086f19301d6de093da6981d61c74b3a07798770af061a66860cd458ff3eeca8920971ebca69c29c5a19ac5307	f	2025-04-17 21:47:15.888523	user	user	123 test st	apt 1	test	ca	21740
34	\N	user1@example.com	2404131255	scrypt:32768:8:1$UlcLsNQ2vt6T1prD$15c99da158089b9c6708252f28cb5590b01827a3d172cef8fd002c135a547e75dc765f06a5c5a4c7f6a925ed97c2dcd682a5788e2c64788202735894e45fc0dc	f	2025-04-17 21:49:19.327766	user	user	123 test st	apt 1	test	ca	21740
1	John Doe	johndoe@example.com	123-456-7890	\N	t	2025-04-11 06:08:02.3093	John	Doe	\N	\N	\N	\N	\N
2	Alice Johnson	alice.johnson@example.com	555-123-4567	\N	t	2025-04-11 06:08:02.3093	Alice	Johnson	\N	\N	\N	\N	\N
3	Bob Smith	bob.smith@example.com	555-987-6543	\N	t	2025-04-11 06:08:02.3093	Bob	Smith	\N	\N	\N	\N	\N
4	Charlie Brown	charlie.brown@example.com	555-555-5555	\N	t	2025-04-11 06:08:02.3093	Charlie	Brown	\N	\N	\N	\N	\N
5	David Smith	david.smith@example.com	555-123-9876	\N	t	2025-04-11 06:08:02.3093	David	Smith	\N	\N	\N	\N	\N
6	Test User	testuser@example.com	555-123-4567	testpassword123	f	2025-04-11 06:27:31.274079	Test	User	\N	\N	\N	\N	\N
8	Test User	test@example.com	555-123-4567	scrypt:32768:8:1$N0dLvPBLKHtOKzEd$1231cb6a7baea98cf1ed935bb306e5ce298e9ba2d80f18c7a0b3f66af3968b37d7d430e7771866beaa8c177d051ef82fbca1af01a94d3a17b8471734d5f4930d	f	2025-04-12 01:02:38.715483	Test	User	\N	\N	\N	\N	\N
10	Reggie Cosens	reggiecosens@example.com	240-513-1368	scrypt:32768:8:1$MrcjgSAgpaKG0Fpe$86227303ab748b91c9878ce4d766280c807ee29052030f9b13dddaefe61f9ab764dfce6910072cf8c63361a82af822b0f9c2e98c968c29fc95274e1757737185	f	2025-04-12 01:48:17.923414	Reggie	Cosens	\N	\N	\N	\N	\N
13	\N	heather@example.com	240-999-9999	scrypt:32768:8:1$LlgqmU7hrr2rinZd$92517863f5c76996d2b829c53e8acff44636070c2ca037470e68fe4163f4a24b280f232ddb098a81d4f7fc1acf613ea1e8a5518b35c7515196d19feb39fdc762	f	2025-04-13 14:51:18.2158	Heather	Jordan	36 elizabeth st	apt 2	hagerstown	maryland	21740
14	\N	testexample@example.com	240-999-9999	scrypt:32768:8:1$c9ukAoIbmWOtyY0y$e1286db38016b08ea8b4fa4a51c312f74d6a92d0bfd5a9c04e95f738f1d6a83dc43315bacc83fb424dd46abe7b39cf7c2e3ba986d85e9cc2a9e457f67a5f3653	f	2025-04-13 20:27:16.89031	Test	Example	123 Test St		Test	Test	99999
15	\N	kristaspranke@example.com	240-999-9999	scrypt:32768:8:1$xViABU1GzHtNdVFG$9cb161771729288459bc8175364b0e75824f15bbd3a12040e9789049333f2232fed1015933ee2cc6e7c60d13f16ac1a296fd2cc57d2b63a2bbdcf23e775b6b56	f	2025-04-13 21:42:31.030506	Krista	Sprankle	123 Test St		Test	Test	99999
16	\N	test@gmail.com	240-999-9999	scrypt:32768:8:1$yWVwezt6mPEtIdvB$cef8b53ec419ce060a48b6a70fd6df06a595f7c49bf393c149dc3eca1ca6db9d1cbaeb40dea663212c5f56909952f51cc533ef61fcb814cedc271da6d9e4c279	f	2025-04-13 22:14:15.606202	Test	Test	123 Test St		Test	Test	99999
17	\N	heathertest@gmail.com	240-999-9999	scrypt:32768:8:1$8UIEUXkWyW56dQO0$44fcf9a2882bb783ee1058a5ae85f8dd033802f2de377ac9b338ecfa50e24d601b6d82b7b88cf1053fdadb1372512b58f64e2b9c300d407039b9a943b5f0d71b	f	2025-04-13 22:25:28.199946	Test	Test	123 Test St		Test	Test	99999
18	\N	georgetest@gmail.com	240-999-9999	scrypt:32768:8:1$os6XfKwOUlAi0IUR$227b501f534cd5163c5e257be6074e314373e4a5774910765f411dc99165706023995dac89e5590a3504c2782170c87a967de3e0d0e650ce3b0b5c4eb041b5bf	f	2025-04-15 01:37:15.357758	George	Test	123 Test St		Test	Test	99999
19	\N	bobtest@example.com	240-999-9999	scrypt:32768:8:1$Ve4N5985ERngwkH9$82a2ea056152cd4aaedf2059b8285d30c3a513b96a4d4de30b9c5c785817b3d8ce15df72664e4e940514a8c751f6ae51ff1a6fbfa6a1005ba090a685c435ddb6	f	2025-04-15 02:17:24.070673	Bob	Test	123 Test St		Test	Test	99999
20	\N	JasonBruchey@example.com	2409999999	scrypt:32768:8:1$lQV5x9f8MSzmNNQ9$3610dc3bf857754bddcf580f0b281b628743ae317b2adc740cd87dc65c682ddbd05514ac7a872d3f8ff5b622e9abb0f0c87f8b73282655d29a0a671aa3a4c1a8	f	2025-04-15 04:43:19.769442	Jason	bruchey	123 Test St	123 Test St	Test	Md	99999
21	\N	bad@email.com	123abc	scrypt:32768:8:1$2nIDLQk0916oBaPF$444e3b69c0d41c6faf18602fd928c50e440743124444801a31701171ce7e2e7064aac97c394f381cd1e218fb21776c8a0a3a0f37ed88cefab505b4fba96f4bea	f	2025-04-15 06:45:40.887778	Jason	bruchey	123 Test St	123 Test St	Test	Californiaaaaa	21740
22	\N	Tester@a.com	2409999999	scrypt:32768:8:1$0po0HgyV2PiEZK5h$8712514373a95fe4c5933d7be37a3a0448317a36602d21d6032405ec76d878dd63305455ca914f496f01502f330544b957b0d3b9e3a6ebb7c1fe05f5984eadca	f	2025-04-15 07:21:10.198542	Test	test	123 Test St	Apt 1	Test	Ca	21740
35	\N	user2@example.com	2404131255	scrypt:32768:8:1$dQxOz1lRzNXeCveI$8f6c58c5ce9056741eb9ba1b95c9920becf6beb9db196320fe0ee9dd3809739fdfd9cebcb16a8bdcdd6abb49659a0721babaaea11fe5d9dc8b273014c2a91a8c	f	2025-04-17 21:50:30.637285	user	user	123 test st	apt 1	test	ca	21740
36	\N	test10@example.com	2405559999	scrypt:32768:8:1$0Vr1CWbH7KpJoAcK$37e65dd750931447d281d8717ea800681407113187fb6bf253ca9181d32ff6db5b30617501ba5d32c63e4a03cffb181fe176e1e243b9176cf43e0d0d67b3cb4f	f	2025-04-18 01:06:07.613821	reggie	cosens	123 test st	123 test st	test	md	99999
37	\N	test101@example.com	2405559999	scrypt:32768:8:1$9gZFZt0zkn6szLui$e50265fea91dcca9cba8a481468a6d61f18dc8f776064ff2bdda0effb954244f6eb051ce52314ec2c49f89d466d409b002a1a906995c73bb82d65a202395b66a	f	2025-04-18 21:57:25.060393	reggie	cosens	123 test st	123 test st	test	md	99999
38	\N	realreal@eaxmple.com	2405559999	scrypt:32768:8:1$5fJFGB5z7Qeqgc3g$027eda57fb10d45de2ca7709cf625cd18335f09dbe57f507e10fbe05afbe829fcbffc0766e22603adc46010e9d760761a6cddf81c854c56ade1eb17679521c5e	f	2025-04-19 02:51:02.919238	reggie	cosens	123 test st	123 test st	test	md	99999
39	\N	KillaTShirtDesigns@gmail.com	2405131368	scrypt:32768:8:1$CkFpQ8EK1ivbHC8C$042491e9017969a7a28e61a71b3ff61ae03e3ff413d7f1590098ec05f47865ea79fa55fc57ef0116543b42d36c4048d92003a136e9811c6aa19d4c66841e3d74	f	2025-04-19 23:50:04.401869	Reginald	Cosens	36 Elizabeth St	Apt 2	Hagerstown	Md	21740
40	\N	reggiecosens3rd@example.com	2405559999	scrypt:32768:8:1$SttxmAWIDZLXOqH0$fa60d825ba5b2ae257f11a5ac3fffa38f6f644d8fa92b2fea374edd73b1543e556537bb7f2438d14fe6445ee18cd7c2009606ff0d7a00652611f3a79fe6bb071	f	2025-04-24 02:55:53.249067	reggie	cosens	123 test st	123 test st	test	md	99999
41	\N	reginaldcosens@example.com	240-513-1368	scrypt:32768:8:1$XaeYrAS75v8h7RtX$077f88520d4aa14599143cdc3c6416b8578aee6cd760a177368645849974c5c887d616e9b6d892c9e08cbaa91b0602bf2c05214d0ddc8c4e7bcb4d0102649101	f	2025-04-25 04:30:13.499195	reggie	cosens	123 test st		test	md	21740
42	\N	reginaldcosens3rd@example.com	2405559999	scrypt:32768:8:1$0chq5vvH7cr4HbKf$d2531f960514d0ef9c2fcaaf2cc1239c96cf148f70882a125bf204320ba8aa4d56ce880397dbb5197bac609e5730c6032a3e1f9fb619b6dc300565de4df36183	f	2025-04-25 05:41:06.631962	reggie	cosens	123 test st	123 test st	test	md	99999
43	\N	reginaldcosensiiinew@gmail.com	240-513-1368	scrypt:32768:8:1$uHz06LxxsEj0ZY4W$617b70344318a13623dbd0fdc9f2001a923c4f35d18f2f7581033d5217b48b9055f4b89d21de6998c2058866f415873f316303a873c2020a4abf136035691e20	f	2025-04-25 19:31:52.61174	reginald	cosens	36 elizabeth st	apt 2	hagerstown	md	21740
44	\N	reginaldcosensiiinewnew@gmail.com	240-513-1368	scrypt:32768:8:1$KhHOy2rWx9vmtbWx$f4184b661c24dffe5a9f16fa962e7a170b2aa65bd2d9f6d549c7bbaec18a44340f94115b3cdf8995a5319533052fc4aef57607f13520635c049703a112326010	f	2025-04-25 21:24:45.427464	reginald	cosens	36 elizabeth st	apt 2	hagerstown	md	21740
45	\N	kevinsmith@gmail.com	240-412-1253	scrypt:32768:8:1$91cPFLSqggJ2mHo1$25e0fd04e4d2db421462790e2eee1f9c12bf2df4d9a5664cbc1f0be214c581fceea6c4baf6e751b38a3a10b9ef8ec5e5b54e773ae6de7f42a65cfa83ba70a5d2	f	2025-04-26 00:36:41.209881	kevin	smith	123 south st		hagerstown	md	21740
46	\N	hjordan@gmail.com	240-123-1245	scrypt:32768:8:1$0TwzcSv9PHME2Jd9$2c34d537816b9a804969461ccaf3ea154c03120b44f55c19d0e8ba91321a2ed29c58c1ef8cebb8f8f2367ad20497d1a5aa5fd249578c43c880e9a5c8c53f3b28	f	2025-04-26 02:40:04.465861	heather	jordan	36 elizabeth st	apt 2	hagerstown	md	21740
47	\N	rcosens@example.com	2405559999	scrypt:32768:8:1$AnL4eZE8H5SaG87b$df6759a26b82d6460d0900a4a5faa456fbc61a3126a51c030831556360c052bd2b697586c0dd83ab3a53f3fa49de399233744b6b1307700c59fdc24eb1dbe291	f	2025-05-05 06:24:41.53142	reggie	cosens	123 test st		test	md	99999
48	heather jordan	hljordan@example.com	2401231234	scrypt:32768:8:1$h7rmQZFaoPQg2uZK$24340182490918fe1ad2562b92d4b6362b36e1e3f303f0cdb32d65bf02835e84be29dcb9282711331621a6ee7b6779ad96b7983da0b57058ac0822971bb15cc9	f	2025-05-05 06:42:12.061217	heather	jordan	123 Test St	Apt 1	test	ca	21740
49	juniper olivia	juni@example.com	2405131368	scrypt:32768:8:1$mkpEziwrzn2aNUqI$58e573bb800295e57c4019c8436d656be69398d98cea32fa48c064f05deb52efafdac5bf87957928a42f7a085e02d2b0f2959e3062b860d7eddcd5c3c30ff898	f	2025-05-05 23:15:55.053083	juniper	olivia	123 Test St	Apt 1	test	ca	21740
50	reginald cosens	regreg@example.com	240-513-1368	scrypt:32768:8:1$z2AfgKOl2AksQZ0l$c85e9b3a16eb38f1cdb7052db22021ac6840d1ae0ac654e668267ff0c463834a046554dbf856def57636447264f9c38865e8d3b8e8999d332f56f3a5d1e31449	f	2025-05-05 23:35:18.638256	reginald	cosens	36 Elizabeth St	Apt 2	hagerstown	md	21740
51	test test	customer1@example.com	2409999999	scrypt:32768:8:1$DYq1So9VydBDCBQP$6386bb902153c3564b5d131b0dc4e441f5ab3c81d72e64e65eeddbfa79a0c1eaf037d5ce44559849ad64aab3a9691423199a34717afe5698ab9e6cae9c7517f2	f	2025-05-06 00:43:41.081009	test	test	123 Test St	Apt 1	test	ca	21740
52	reggie reggie	regr@example.com	2405131368	scrypt:32768:8:1$qj9Z15wNnCPjzs3G$052b6e92740b60c9ce6457966817182955c35a9b95fa5f5f35e5d3c67d3d43e07d5373bd5a29209cfc7bd1a5eddfc48e026de4486b2bc34d0d602fafad5fd672	f	2025-05-06 01:01:54.532389	reggie	reggie	123 Test St	Apt 1	hagerstown	ca	21740
53	reggie reggie	customer2@example.com	2405131368	scrypt:32768:8:1$gdl097fq9j8DRjyq$a6121ee433d4ba1b1e66a5c4a9eda7ed3b51fc5c5666ace02afc51be537babc476e86eeffe739af01481973dc182b956d39d9f4c71aa6fbe7bbbea271a12cc91	f	2025-05-06 04:40:32.099411	reggie	reggie	123 Test St	Apt 1	hagerstown	ca	21740
54	reggie cosens	customer3@example.com	2405559999	scrypt:32768:8:1$BER1jBn394Kbj2nm$0257c815c28e7a779c8a6e975ca7974c24c1d6e1fecc855f14c4ac7b5040d231f02180955a28a292b53f500c314056d7d08b2103d7b17e54319bf4b934a7d2d4	f	2025-05-07 04:24:27.799491	reggie	cosens	123 Test St	123 Test St	test	md	99999
55	reggie cosens	customer4@example.com	2405559999	scrypt:32768:8:1$4Rxr7aiJ6LnkvCQc$5c21bc217eb9c28ec27c87aec5689ba83f674f36b659021ada0c6c73aad6ea3e28ee3179fddd4b814425436c4c8dd0296e3aafcf7d97273d6b39812d177c34ce	f	2025-05-07 04:28:56.428552	reggie	cosens	123 Test St	123 Test St	test	md	99999
56	reggie cosens	customer5@example.com	2405559999	scrypt:32768:8:1$dcDudA5fsmhpTEl0$e61d066d51bfbdf9d5a8795e80920395f244ccf793382ef679a7b1da3934536911f8ad00a686c620c41630d9bb23003f7583a39304ff3ecb535228089b32b516	f	2025-05-07 04:58:45.744072	reggie	cosens	123 Test St		test	md	99999
57	\N	customer6@example.com	2405131368	scrypt:32768:8:1$pomoPbOazpkSPltt$c29eadad6b513c04e4d95abbeedaf80d035bfdb25cd15fd1fbedfb71f17fa709a77ba7fdd84da6ec93861c44f9ad1c0638bb6b73c12e9c6a538bb266f5a19c28	f	2025-05-07 05:40:07.131164	reginald	cosens	36 elizabeth st	apt 2	hagerstown	md	21740
\.


--
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.order_items (order_item_id, order_id, book_id, quantity) FROM stdin;
1	1	1	2
2	1	1	2
3	1	3	1
4	2	2	3
5	2	4	1
6	3	5	1
7	1	1	3
8	1	2	2
9	1	3	1
10	6	20	1
11	6	19	2
12	6	18	3
13	6	17	1
14	7	3	1
15	7	10	1
16	7	22	1
17	7	27	1
18	7	28	1
19	8	3	4
20	8	5	1
21	8	6	1
22	9	6	1
23	9	7	1
24	10	5	1
25	11	3	3
26	12	3	3
27	12	5	1
28	13	5	1
29	14	2	1
30	15	3	1
31	15	6	2
32	16	3	1
33	16	5	2
34	16	14	1
35	17	9	2
36	17	13	1
37	18	8	1
38	19	3	1
39	19	8	1
40	19	11	1
41	20	3	1
42	20	7	5
43	20	24	3
44	21	1	1
45	22	3	1
46	23	5	1
47	24	6	5
48	25	33	1
49	26	3	1
50	27	12	1
51	28	9	1
52	29	11	1
53	30	8	3
54	31	1	3
55	32	33	2
56	33	3	5
57	33	1	3
58	34	18	1
59	35	17	1
60	36	33	1
61	37	24	1
62	38	16	1
63	38	30	3
64	38	20	1
65	39	9	5
66	39	27	3
67	39	31	1
68	39	4	1
69	39	19	1
70	40	23	2
71	40	32	5
72	40	3	1
73	40	16	1
74	40	30	1
75	41	20	1
76	41	31	2
77	42	7	1
78	42	27	1
79	42	32	1
80	43	1	1
81	44	12	1
82	45	14	2
83	46	22	1
84	47	24	1
85	48	16	1
86	48	20	1
87	48	27	5
88	48	1	2
89	49	25	1000
90	50	6	1
91	50	20	2
92	51	9	1
93	52	10	1
94	52	18	1
95	52	33	1
96	53	9	1
97	55	5	1
98	56	11	1
99	56	3	1
100	56	1	1
101	56	33	1
102	57	29	1
103	58	25	1
104	59	13	1
105	60	8	1
106	61	21	1
107	62	28	1
108	76	15	1
109	76	19	2
110	76	30	6
111	76	24	1
112	76	16	4
113	76	27	1
114	76	18	1
115	77	2	1
116	78	26	1
117	79	8	1
118	80	8	1
119	81	30	1
120	81	8	1
121	81	32	2
122	81	20	5
123	82	17	1
124	83	28	5
125	83	27	1
126	83	4	2
127	84	15	1
128	85	19	1000
129	86	21	1
130	87	13	1
131	88	2	4
132	88	23	1
133	88	27	1
134	89	16	1
135	90	18	1
136	91	26	1
137	92	24	1
138	93	8	1
139	94	30	1
140	95	32	1
141	96	31	1
142	97	7	1
143	98	20	1
144	99	17	1
145	100	12	1
146	101	14	2
147	102	22	1
148	103	28	1
149	104	4	1
150	105	6	5
151	105	11	1
152	106	27	6
153	106	22	1
154	106	28	1
155	107	28	1
156	108	10	1
157	109	3	1
158	110	3	1
159	111	3	1
160	112	3	1
161	113	10	1
162	114	15	1
163	115	10	1
164	116	5	1
165	120	33	1
166	121	10	1
167	122	9	1
168	123	5	1
169	124	9	1
170	125	15	1
171	126	3	1
172	126	9	1
173	126	15	2
174	126	32	3
175	127	25	1
176	128	5	1
177	128	7	1
178	128	17	2
179	129	5	1
180	129	7	1
181	129	17	2
182	130	10	1
183	131	3	1
184	131	13	1
185	131	11	2
186	132	3	1
187	132	13	1
188	132	11	2
189	133	10	1
190	133	13	2
191	134	24	1
192	134	31	2
193	135	33	2
194	135	19	1
195	135	15	1
196	136	7	1
197	137	32	2
198	138	25	1
199	139	5	1
200	140	28	1
201	140	10	2
202	140	24	4
203	141	1	1
204	142	16	1
205	143	31	1
206	144	33	1
207	145	13	1
208	146	29	1
209	147	2	1
210	148	2	1
211	149	26	1
212	150	8	1
213	150	30	1
214	150	14	3
215	150	4	2
216	151	3	1
217	152	9	1
218	153	32	1
219	154	20	1
220	155	22	1
221	156	23	1
222	157	19	1
223	158	15	1
224	159	7	1
225	160	7	1
226	161	7	1
227	162	7	1
228	163	7	1
229	164	7	1
230	165	7	1
231	166	7	1
232	167	7	1
233	168	7	1
234	169	7	1
235	170	25	2
236	170	17	1
237	170	10	2
238	171	25	1
239	172	7	2
240	172	17	2
241	173	25	1
242	174	10	1
243	175	7	1
244	176	17	1
245	177	17	1
246	178	10	1
247	179	25	1
248	180	7	1
249	181	27	1
250	182	5	1
251	183	10	1
252	184	17	1
253	184	28	2
254	184	24	1
255	185	25	1
256	185	7	3
257	185	11	2
258	186	16	1
259	187	1	1
260	188	31	1
261	189	27	1
262	190	5	1
263	191	33	1
264	192	10	1
265	193	13	1
266	194	29	1
267	195	17	1
268	196	28	1
269	197	2	1
270	198	24	1
271	199	26	2
272	199	8	1
273	199	30	2
274	200	30	1
275	200	25	2
276	200	7	2
277	201	30	2
278	201	7	1
279	201	14	1
280	201	11	3
281	202	25	1
282	202	14	2
283	202	21	3
284	202	16	1
285	203	30	2
286	203	11	1
287	203	25	3
288	204	7	1
289	204	21	2
290	204	11	3
291	205	14	1
292	205	30	2
293	205	7	3
294	206	25	1
295	206	14	1
296	206	33	4
297	206	10	2
298	206	6	2
299	207	16	2
300	207	11	1
301	207	30	3
302	207	7	2
303	208	25	1
304	209	21	1
305	210	14	1
306	211	10	1
307	211	16	2
308	211	11	2
309	212	33	1
310	213	6	1
311	214	30	1
312	215	7	1
313	216	25	1
314	217	21	1
315	218	10	3
316	218	11	1
317	218	6	1
318	219	16	1
319	219	4	2
320	220	14	1
321	220	33	1
322	220	30	2
323	220	25	3
324	221	33	1
325	222	24	1
326	222	26	5
327	222	8	2
328	222	14	3
329	223	30	1
330	224	25	1
331	225	4	1
332	226	33	1
333	227	24	1
334	228	2	1
335	229	26	1
336	229	8	2
337	229	14	7
338	229	21	1
339	229	10	2
340	229	1	1
341	230	28	1
342	231	30	1
343	231	25	2
344	231	8	4
345	232	33	1
346	233	4	1
347	233	24	2
348	233	26	3
349	233	11	5
350	234	12	3
351	235	12	3
352	236	14	1
353	237	2	1
354	237	10	1
355	238	21	1
356	239	23	2
357	239	17	1
358	240	23	3
359	240	16	1
360	241	25	1
361	242	1	1
362	242	28	2
363	242	24	3
364	243	30	1
365	243	14	3
366	244	19	1
367	245	11	4
368	245	12	3
369	245	7	4
370	246	8	1
371	246	26	3
372	246	12	1
373	247	7	1
374	248	8	1
375	248	12	1
376	248	7	2
377	249	29	1
378	250	26	1
379	251	26	1
380	252	12	1
381	261	26	1
382	262	12	2
383	262	8	1
384	262	7	2
385	263	29	1
386	264	26	1
387	265	12	1
388	266	8	1
389	267	29	1
390	268	7	1
391	268	1	2
392	268	26	1
393	269	21	1
394	270	21	1
395	271	21	1
396	272	33	1
397	273	21	2
398	274	21	1
399	275	33	1
400	276	21	1
401	277	33	3
402	278	21	1
403	279	33	1
404	280	21	1
405	281	33	1
406	282	21	1
407	283	33	1
408	284	21	1
409	285	33	1
410	286	21	1
411	287	33	1
412	288	33	1
413	288	4	2
414	288	12	2
415	288	7	1
416	289	21	1
417	289	4	2
418	290	33	1
419	291	12	1
420	292	7	1
421	293	21	2
422	293	4	1
423	293	33	4
424	293	12	1
425	294	7	1
426	295	21	3
427	295	4	2
428	295	33	1
429	295	12	1
430	296	7	1
431	297	21	1
432	298	4	1
433	299	33	1
434	300	33	1
435	301	12	1
436	302	7	1
437	303	8	1
438	304	29	1
439	305	6	1
440	306	17	1
441	307	17	1
442	308	21	1
443	308	4	2
444	308	12	4
445	308	8	1
446	309	21	1
447	310	4	1
448	311	4	1
449	312	12	1
450	312	8	1
451	312	21	3
452	313	4	1
453	314	12	1
454	314	8	2
455	315	21	1
456	316	29	1
457	316	6	1
458	317	4	1
459	318	12	1
460	319	8	1
461	320	8	1
462	321	21	1
463	322	29	1
464	323	6	1
465	324	4	1
466	325	12	1
467	326	8	1
468	327	21	1
469	327	29	2
470	327	4	1
471	327	33	4
472	328	6	1
473	328	12	2
474	329	8	1
475	330	21	1
476	331	4	1
477	332	29	1
478	333	33	1
479	334	6	1
480	335	12	1
481	336	29	1
482	337	8	1
483	338	21	1
484	339	4	1
485	340	33	1
486	341	6	1
487	342	12	1
488	343	4	1
489	344	12	1
490	345	21	1
491	346	29	1
492	347	29	1
493	348	29	1
494	349	8	1
495	350	20	1
496	351	20	1
497	352	20	2
498	352	14	1
499	353	20	1
500	353	14	1
501	353	27	2
502	354	20	1
503	354	14	2
504	354	19	1
505	354	32	4
506	355	20	2
507	356	20	1
508	357	20	1
509	358	20	1
510	359	20	1
511	360	20	1
512	361	20	1
513	362	20	1
514	363	14	1
515	364	20	1
516	365	20	1
517	366	20	1
518	366	14	1
519	366	27	4
520	367	20	1
521	368	30	1
522	369	29	1
523	370	8	1
524	370	17	1
525	371	32	1
526	372	19	1
527	373	20	1
528	374	31	1
529	375	31	1
530	376	27	1
531	377	20	1
532	378	20	1
533	379	20	1
534	380	20	1
535	381	20	1
536	382	31	1
537	383	20	1
538	384	20	1
539	385	20	1
540	386	20	1
541	387	20	1
542	388	4	1
543	389	9	1
544	390	14	1
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.orders (order_id, customer_id, order_date, total_amount) FROM stdin;
2	1	2025-04-04	39.98
3	2	2025-04-04	59.97
4	3	2025-04-04	19.99
5	1	2025-04-04	0.00
1	1	2025-04-03	156.89
6	1	2025-04-07	104.36
7	1	2025-04-07	0.00
8	1	2025-04-07	578.72
9	1	2025-04-07	539.75
10	1	2025-04-07	539.75
11	1	2025-04-07	38.97
12	1	2025-04-07	54.47
13	1	2025-04-07	15.50
14	1	2025-04-07	19.99
15	1	2025-04-07	56.99
16	1	2025-04-07	63.19
17	1	2025-04-07	50.10
18	1	2025-04-07	11.45
19	1	2025-04-08	41.43
20	1	2025-04-08	147.39
21	1	2025-04-08	12.99
22	1	2025-04-09	12.99
23	1	2025-04-09	15.50
24	5	2025-04-09	110.00
25	5	2025-04-09	19.99
26	1	2025-04-10	12.99
27	1	2025-04-10	10.75
28	1	2025-04-10	14.25
29	3	2025-04-10	16.99
30	4	2025-04-10	34.35
31	5	2025-04-10	38.97
32	1	2025-04-10	39.98
33	2	2025-04-10	103.92
34	1	2025-04-12	10.30
35	1	2025-04-12	14.99
36	1	2025-04-12	19.99
37	1	2025-04-12	13.55
38	1	2025-04-12	81.99
39	1	2025-04-12	188.45
40	13	2025-04-13	167.29
41	14	2025-04-13	44.99
42	14	2025-04-13	60.74
43	14	2025-04-13	12.99
44	14	2025-04-13	10.75
45	14	2025-04-13	38.40
46	16	2025-04-13	18.90
47	16	2025-04-13	13.55
48	17	2025-04-13	179.92
49	17	2025-04-14	14750.00
50	17	2025-04-15	54.98
51	17	2025-04-15	14.25
52	17	2025-04-15	43.29
53	19	2025-04-15	14.25
54	19	2025-04-15	0.00
55	19	2025-04-15	15.50
56	19	2025-04-15	62.96
57	1	2025-04-15	21.75
58	24	2025-04-16	14.75
59	19	2025-04-16	21.60
60	19	2025-04-16	11.45
61	19	2025-04-16	12.85
62	19	2025-04-17	17.30
69	36	2025-04-17	0.00
70	36	2025-04-17	0.00
71	36	2025-04-17	0.00
72	36	2025-04-17	0.00
73	36	2025-04-17	0.00
74	36	2025-04-18	0.00
75	36	2025-04-18	0.00
76	36	2025-04-18	269.62
77	36	2025-04-18	19.99
78	36	2025-04-18	19.50
79	36	2025-04-18	11.45
80	36	2025-04-18	11.45
81	37	2025-04-18	145.90
82	36	2025-04-18	14.99
83	36	2025-04-18	130.47
84	36	2025-04-19	13.80
85	36	2025-04-19	20990.00
86	36	2025-04-19	12.85
87	36	2025-04-19	21.60
88	36	2025-04-19	119.35
89	36	2025-04-19	17.50
90	36	2025-04-19	10.30
91	36	2025-04-19	19.50
92	36	2025-04-19	13.55
93	36	2025-04-19	11.45
94	36	2025-04-19	16.00
95	36	2025-04-19	18.00
96	36	2025-04-19	14.25
97	36	2025-04-19	18.75
98	36	2025-04-19	16.49
99	36	2025-04-19	14.99
100	36	2025-04-19	10.75
101	38	2025-04-19	38.40
102	38	2025-04-19	18.90
103	38	2025-04-19	17.30
104	38	2025-04-19	9.99
105	10	2025-04-19	126.99
106	38	2025-04-24	180.14
107	40	2025-04-24	17.30
108	40	2025-04-24	13.00
109	40	2025-04-24	12.99
110	40	2025-04-24	12.99
111	40	2025-04-24	12.99
112	40	2025-04-24	12.99
113	40	2025-04-24	13.00
114	40	2025-04-24	13.80
115	40	2025-04-24	13.00
116	40	2025-04-24	15.50
120	40	2025-04-24	19.99
121	40	2025-04-24	13.00
122	40	2025-04-24	14.25
123	40	2025-04-24	15.50
124	40	2025-04-24	14.25
125	40	2025-04-24	13.80
126	40	2025-04-24	108.84
127	40	2025-04-24	14.75
128	40	2025-04-24	64.23
129	40	2025-04-24	64.23
130	40	2025-04-24	13.00
131	40	2025-04-24	68.57
132	40	2025-04-24	68.57
133	40	2025-04-24	56.20
134	40	2025-04-24	42.05
135	40	2025-04-24	74.77
136	40	2025-04-24	18.75
137	40	2025-04-24	36.00
138	40	2025-04-25	14.75
139	40	2025-04-25	15.50
140	40	2025-04-25	97.50
141	40	2025-04-25	12.99
142	40	2025-04-25	17.50
143	40	2025-04-25	14.25
144	40	2025-04-25	19.99
145	40	2025-04-25	21.60
146	40	2025-04-25	21.75
147	40	2025-04-25	19.99
148	40	2025-04-25	19.99
149	40	2025-04-25	19.50
150	41	2025-04-25	105.03
151	41	2025-04-25	12.99
152	41	2025-04-25	14.25
153	41	2025-04-25	18.00
154	42	2025-04-25	16.49
155	42	2025-04-25	18.90
156	42	2025-04-25	15.40
157	42	2025-04-25	20.99
158	42	2025-04-25	13.80
159	42	2025-04-25	18.75
160	42	2025-04-25	18.75
161	42	2025-04-25	18.75
162	42	2025-04-25	18.75
163	42	2025-04-25	18.75
164	42	2025-04-25	18.75
165	42	2025-04-25	18.75
166	42	2025-04-25	18.75
167	42	2025-04-25	18.75
168	42	2025-04-25	18.75
169	42	2025-04-25	18.75
170	42	2025-04-25	70.49
171	42	2025-04-25	14.75
172	42	2025-04-25	67.48
173	42	2025-04-25	14.75
174	42	2025-04-25	13.00
175	42	2025-04-25	18.75
176	42	2025-04-25	14.99
177	42	2025-04-25	14.99
178	42	2025-04-25	13.00
179	42	2025-04-25	14.75
180	42	2025-04-25	18.75
181	42	2025-04-25	23.99
182	42	2025-04-25	15.50
183	42	2025-04-25	13.00
184	42	2025-04-25	63.14
185	42	2025-04-25	104.98
186	42	2025-04-25	17.50
187	42	2025-04-25	12.99
188	42	2025-04-25	14.25
189	42	2025-04-25	23.99
190	42	2025-04-25	15.50
191	42	2025-04-25	19.99
192	42	2025-04-25	13.00
193	42	2025-04-25	21.60
194	42	2025-04-25	21.75
195	42	2025-04-25	14.99
196	42	2025-04-25	17.30
197	42	2025-04-25	19.99
198	42	2025-04-25	13.55
199	42	2025-04-25	82.45
200	42	2025-04-25	83.00
201	42	2025-04-25	120.92
202	42	2025-04-25	109.20
203	42	2025-04-25	93.24
204	42	2025-04-25	95.42
205	42	2025-04-25	107.45
206	43	2025-04-25	183.91
207	43	2025-04-25	137.49
208	43	2025-04-25	14.75
209	43	2025-04-25	12.85
210	43	2025-04-25	19.20
211	43	2025-04-25	81.98
212	43	2025-04-25	19.99
213	43	2025-04-25	22.00
214	43	2025-04-25	16.00
215	43	2025-04-25	18.75
216	43	2025-04-25	14.75
217	43	2025-04-25	12.85
218	43	2025-04-25	77.99
219	43	2025-04-25	37.48
220	43	2025-04-25	115.44
221	44	2025-04-25	19.99
222	44	2025-04-25	191.55
223	44	2025-04-25	16.00
224	44	2025-04-25	14.75
225	44	2025-04-25	9.99
226	44	2025-04-25	19.99
227	44	2025-04-25	13.55
228	44	2025-04-25	19.99
229	44	2025-04-25	228.64
230	44	2025-04-25	17.30
231	44	2025-04-25	91.30
232	10	2025-04-26	19.99
233	45	2025-04-26	180.54
234	44	2025-04-26	32.25
235	44	2025-04-26	32.25
236	45	2025-04-26	19.20
237	45	2025-04-26	32.99
238	45	2025-04-26	12.85
239	45	2025-04-26	45.79
240	45	2025-04-26	63.70
241	44	2025-04-26	14.75
242	46	2025-04-26	88.24
243	45	2025-04-26	73.60
244	45	2025-04-26	20.99
245	45	2025-04-26	175.21
246	45	2025-04-26	80.70
247	45	2025-04-27	18.75
248	45	2025-04-27	59.70
249	44	2025-04-27	21.75
250	44	2025-05-02	19.50
251	44	2025-05-02	19.50
252	44	2025-05-02	10.75
256	44	2025-05-02	11.45
257	44	2025-05-02	18.75
258	44	2025-05-02	21.75
259	44	2025-05-02	21.75
261	44	2025-05-02	19.50
262	44	2025-05-02	70.45
263	45	2025-05-03	21.75
264	44	2025-05-03	19.50
265	44	2025-05-03	10.75
266	44	2025-05-03	11.45
267	44	2025-05-03	21.75
268	44	2025-05-03	64.23
269	44	2025-05-03	12.85
270	44	2025-05-03	12.85
271	44	2025-05-03	12.85
272	44	2025-05-03	19.99
273	44	2025-05-03	25.70
274	44	2025-05-03	12.85
275	44	2025-05-04	19.99
276	44	2025-05-04	12.85
277	44	2025-05-04	59.97
278	44	2025-05-04	12.85
279	44	2025-05-04	19.99
280	44	2025-05-04	12.85
281	44	2025-05-04	19.99
282	44	2025-05-04	12.85
283	44	2025-05-04	19.99
284	44	2025-05-04	12.85
285	44	2025-05-04	19.99
286	44	2025-05-04	12.85
287	44	2025-05-04	19.99
288	44	2025-05-04	80.22
289	44	2025-05-04	32.83
290	44	2025-05-04	19.99
291	44	2025-05-04	10.75
292	44	2025-05-04	18.75
293	44	2025-05-04	126.40
294	44	2025-05-04	18.75
295	44	2025-05-04	89.27
296	44	2025-05-04	18.75
297	44	2025-05-04	12.85
298	44	2025-05-04	9.99
299	44	2025-05-04	19.99
300	44	2025-05-04	19.99
301	44	2025-05-04	10.75
302	44	2025-05-04	18.75
303	44	2025-05-04	11.45
304	44	2025-05-04	21.75
305	44	2025-05-04	22.00
306	44	2025-05-04	14.99
307	44	2025-05-04	14.99
308	44	2025-05-04	87.28
309	44	2025-05-04	12.85
310	44	2025-05-04	9.99
311	44	2025-05-04	9.99
312	44	2025-05-04	60.75
313	44	2025-05-04	9.99
314	44	2025-05-04	33.65
315	44	2025-05-04	12.85
316	44	2025-05-05	43.75
317	44	2025-05-05	9.99
318	44	2025-05-05	10.75
319	44	2025-05-05	11.45
320	44	2025-05-05	11.45
321	44	2025-05-05	12.85
322	47	2025-05-05	21.75
323	48	2025-05-05	22.00
324	48	2025-05-05	9.99
325	48	2025-05-05	10.75
326	48	2025-05-05	11.45
327	50	2025-05-05	146.30
328	51	2025-05-06	43.50
329	48	2025-05-06	11.45
330	48	2025-05-06	12.85
331	52	2025-05-06	9.99
332	48	2025-05-06	21.75
333	48	2025-05-06	19.99
334	48	2025-05-06	22.00
335	48	2025-05-06	10.75
336	48	2025-05-06	21.75
337	53	2025-05-06	11.45
338	53	2025-05-06	12.85
339	53	2025-05-06	9.99
340	53	2025-05-06	19.99
341	53	2025-05-06	22.00
342	53	2025-05-06	10.75
343	53	2025-05-07	9.99
344	53	2025-05-07	10.75
345	53	2025-05-07	12.85
346	53	2025-05-07	21.75
347	53	2025-05-07	21.75
348	53	2025-05-07	21.75
349	53	2025-05-07	11.45
350	53	2025-05-07	16.49
351	53	2025-05-07	16.49
352	53	2025-05-07	52.18
353	53	2025-05-07	83.67
354	53	2025-05-07	147.88
355	53	2025-05-07	32.98
356	53	2025-05-07	16.49
357	54	2025-05-07	16.49
358	53	2025-05-07	16.49
359	55	2025-05-07	16.49
360	55	2025-05-07	16.49
361	55	2025-05-07	16.49
362	53	2025-05-07	16.49
363	53	2025-05-07	19.20
364	56	2025-05-07	16.49
365	53	2025-05-07	16.49
366	53	2025-05-07	131.65
367	53	2025-05-07	16.49
368	10	2025-05-07	16.00
369	10	2025-05-07	21.75
370	10	2025-05-07	26.44
371	57	2025-05-07	18.00
372	10	2025-05-07	20.99
373	10	2025-05-07	16.49
374	53	2025-05-07	14.25
375	53	2025-05-07	14.25
376	53	2025-05-07	23.99
377	53	2025-05-07	16.49
378	10	2025-05-07	16.49
379	45	2025-05-07	16.49
380	57	2025-05-07	16.49
381	10	2025-05-07	16.49
382	53	2025-05-08	14.25
383	53	2025-05-08	16.49
384	53	2025-05-08	16.49
385	53	2025-05-08	16.49
386	53	2025-05-08	16.49
387	53	2025-05-08	16.49
388	53	2025-05-08	9.99
389	53	2025-05-08	14.25
390	53	2025-05-08	19.20
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, username, password, role) FROM stdin;
1	admin	$2b$12$r80ISjmnucdFyP4RV7K5xeq01eaMTGSJ.Ih9HUnXRBYwyLb8HhzDO	admin
6	Jason	$2b$12$uoiub1vHD6TeSuQDz4.9Ce9GBWBKNtbDuZ/CUjDjA7S97rrOcvmf.	user
7	juniper	$2b$12$15WhETftAfWHuKNHjnH8CuDpmTYKuDWVl//Hh/R/ARd89RbaWs7Me	user
4	Heather	$2b$12$fwcYpTuOWggGC550JzQuo.TD/pTz5bp8nqm7zxJabMN4MLijfdZMK	user
\.


--
-- Name: books_book_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.books_book_id_seq', 35, true);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.customers_customer_id_seq', 57, true);


--
-- Name: order_items_order_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.order_items_order_item_id_seq', 544, true);


--
-- Name: orders_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.orders_order_id_seq', 390, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 7, true);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (book_id);


--
-- Name: customers customers_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_email_key UNIQUE (email);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: order_items order_items_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_pkey PRIMARY KEY (order_item_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: unique_lower_email; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_lower_email ON public.customers USING btree (lower((email)::text));


--
-- Name: unique_username_lowercase; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX unique_username_lowercase ON public.users USING btree (lower(username));


--
-- Name: order_items order_items_book_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_book_id_fkey FOREIGN KEY (book_id) REFERENCES public.books(book_id);


--
-- Name: order_items order_items_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.order_items
    ADD CONSTRAINT order_items_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(order_id);


--
-- Name: orders orders_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES public.customers(customer_id);


--
-- PostgreSQL database dump complete
--

