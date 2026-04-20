--
-- PostgreSQL database dump
--


-- Dumped from database version 17.6
-- Dumped by pg_dump version 17.6

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts (
    user_id bigint NOT NULL,
    name character varying(50) NOT NULL,
    current_balance numeric(10,2) DEFAULT 0 NOT NULL,
    success_count integer DEFAULT 0 NOT NULL,
    ref_link character varying(50) NOT NULL,
    referrer_id bigint,
    is_banned boolean DEFAULT false NOT NULL,
    avatar_filename character varying(100),
    good_marks integer DEFAULT 0 NOT NULL,
    bad_marks integer DEFAULT 0 NOT NULL,
    reg_date date NOT NULL,
    vip_status integer DEFAULT 1 NOT NULL,
    deals_summ numeric(10,2) DEFAULT 0 NOT NULL,
    frozen_balance numeric(10,2) DEFAULT 0 NOT NULL,
    was_online character varying(50) DEFAULT 0 NOT NULL
);


--
-- Name: ad_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ad_requests (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    announ_id integer NOT NULL,
    format character varying(20) NOT NULL,
    text character varying(4000) NOT NULL,
    created_at timestamp with time zone
);


--
-- Name: ad_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ad_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ad_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ad_requests_id_seq OWNED BY public.ad_requests.id;


--
-- Name: ads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ads (
    ad_announ_id integer NOT NULL,
    cover integer NOT NULL,
    cpm integer NOT NULL,
    er integer NOT NULL,
    channel_link character varying(100) NOT NULL,
    subs_count integer NOT NULL,
    topic integer NOT NULL,
    country integer NOT NULL,
    red_label boolean DEFAULT false NOT NULL,
    black_label boolean DEFAULT false NOT NULL
);


--
-- Name: announ_price_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.announ_price_history (
    announ_id integer NOT NULL,
    price numeric(10,2) NOT NULL,
    price_date date NOT NULL
);


--
-- Name: announs_announ_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.announs_announ_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: announs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.announs (
    announ_id integer DEFAULT nextval('public.announs_announ_id_seq'::regclass) NOT NULL,
    seller_id bigint NOT NULL,
    type character varying(16) NOT NULL,
    title character varying(50) NOT NULL,
    short_text character varying(128) NOT NULL,
    long_text character varying(1024) NOT NULL,
    status character varying(16) NOT NULL,
    article bigint NOT NULL
);


--
-- Name: announs_article_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.announs_article_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: announs_article_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.announs_article_seq OWNED BY public.announs.article;


--
-- Name: audience_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.audience_types (
    id integer NOT NULL,
    type_name character varying(100) NOT NULL
);


--
-- Name: audience_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.audience_types_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: audience_types_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.audience_types_id_seq OWNED BY public.audience_types.id;


--
-- Name: channel_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.channel_requests (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    username character varying(33) NOT NULL,
    announ_id integer,
    status character varying(16),
    created_at timestamp with time zone
);


--
-- Name: channel_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.channel_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: channel_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.channel_requests_id_seq OWNED BY public.channel_requests.id;


--
-- Name: channels; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.channels (
    chn_announ_id integer NOT NULL,
    chn_type character varying(32) NOT NULL,
    subs_count integer NOT NULL,
    cover_count numeric(10,2) NOT NULL,
    profit numeric(10,2) NOT NULL,
    on_requests boolean NOT NULL,
    channel_link character varying(100) NOT NULL,
    price numeric(10,2) NOT NULL,
    author boolean NOT NULL,
    topic integer NOT NULL,
    country integer NOT NULL,
    red_label boolean DEFAULT false NOT NULL,
    black_label boolean DEFAULT false NOT NULL
);


--
-- Name: countries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.countries (
    id integer NOT NULL,
    country_name character varying(100) NOT NULL
);


--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.countries_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.countries_id_seq OWNED BY public.countries.id;


--
-- Name: deals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.deals (
    deal_id integer NOT NULL,
    seller_id bigint NOT NULL,
    buyer_id bigint NOT NULL,
    deal_name character varying(50) NOT NULL,
    price numeric(10,2) NOT NULL,
    deal_info character varying(50) NOT NULL,
    type character varying(20) NOT NULL,
    complete_request boolean
);


--
-- Name: deals_deal_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.deals_deal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: deals_deal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.deals_deal_id_seq OWNED BY public.deals.deal_id;


--
-- Name: imgs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.imgs (
    img_id integer NOT NULL,
    img_announ_id integer NOT NULL,
    img_filename character varying(50) NOT NULL
);


--
-- Name: imgs_img_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.imgs_img_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: imgs_img_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.imgs_img_id_seq OWNED BY public.imgs.img_id;


--
-- Name: platforms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.platforms (
    id integer NOT NULL,
    platform_name character varying(100) NOT NULL
);


--
-- Name: platforms_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.platforms_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: platforms_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.platforms_id_seq OWNED BY public.platforms.id;


--
-- Name: topics; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.topics (
    id integer NOT NULL,
    topic_name character varying(100) NOT NULL
);


--
-- Name: topics_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.topics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: topics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.topics_id_seq OWNED BY public.topics.id;


--
-- Name: traffic; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traffic (
    trf_announ_id integer NOT NULL,
    price numeric(10,2) NOT NULL,
    min_leads integer NOT NULL,
    max_leads integer NOT NULL,
    topic integer,
    country integer,
    platform integer,
    audience_type integer,
    traffic_type integer
);


--
-- Name: traffic_requests; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traffic_requests (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    announ_id integer NOT NULL,
    leads_count integer NOT NULL,
    price numeric(10,2) NOT NULL,
    created_at timestamp with time zone
);


--
-- Name: traffic_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.traffic_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: traffic_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.traffic_requests_id_seq OWNED BY public.traffic_requests.id;


--
-- Name: traffic_types; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.traffic_types (
    id integer NOT NULL,
    traffic_type_name character varying(100) NOT NULL
);


--
-- Name: traffic_types_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE public.traffic_types ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.traffic_types_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: transactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transactions (
    transaction_id integer NOT NULL,
    user_id bigint NOT NULL,
    status character varying(16) NOT NULL,
    summ numeric(10,2) NOT NULL,
    tr_type character varying(3) NOT NULL,
    transaction_time timestamp with time zone NOT NULL,
    sys_msg character varying(64)
);


--
-- Name: ad_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ad_requests ALTER COLUMN id SET DEFAULT nextval('public.ad_requests_id_seq'::regclass);


--
-- Name: announs article; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announs ALTER COLUMN article SET DEFAULT nextval('public.announs_article_seq'::regclass);


--
-- Name: audience_types id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audience_types ALTER COLUMN id SET DEFAULT nextval('public.audience_types_id_seq'::regclass);


--
-- Name: channel_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel_requests ALTER COLUMN id SET DEFAULT nextval('public.channel_requests_id_seq'::regclass);


--
-- Name: countries id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries ALTER COLUMN id SET DEFAULT nextval('public.countries_id_seq'::regclass);


--
-- Name: deals deal_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals ALTER COLUMN deal_id SET DEFAULT nextval('public.deals_deal_id_seq'::regclass);


--
-- Name: imgs img_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.imgs ALTER COLUMN img_id SET DEFAULT nextval('public.imgs_img_id_seq'::regclass);


--
-- Name: platforms id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platforms ALTER COLUMN id SET DEFAULT nextval('public.platforms_id_seq'::regclass);


--
-- Name: topics id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.topics ALTER COLUMN id SET DEFAULT nextval('public.topics_id_seq'::regclass);


--
-- Name: traffic_requests id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_requests ALTER COLUMN id SET DEFAULT nextval('public.traffic_requests_id_seq'::regclass);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (user_id);


--
-- Name: ad_requests ad_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ad_requests
    ADD CONSTRAINT ad_requests_pkey PRIMARY KEY (id);


--
-- Name: ads ads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT ads_pkey PRIMARY KEY (ad_announ_id);


--
-- Name: announ_price_history announ_price_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announ_price_history
    ADD CONSTRAINT announ_price_history_pkey PRIMARY KEY (announ_id, price_date);


--
-- Name: announs announs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announs
    ADD CONSTRAINT announs_pkey PRIMARY KEY (announ_id);


--
-- Name: audience_types audience_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.audience_types
    ADD CONSTRAINT audience_types_pkey PRIMARY KEY (id);


--
-- Name: channel_requests channel_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel_requests
    ADD CONSTRAINT channel_requests_pkey PRIMARY KEY (id);


--
-- Name: channels channels_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_pkey PRIMARY KEY (chn_announ_id);


--
-- Name: countries countries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: deals deals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT deals_pkey PRIMARY KEY (deal_id);


--
-- Name: imgs imgs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.imgs
    ADD CONSTRAINT imgs_pkey PRIMARY KEY (img_id);


--
-- Name: platforms platforms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.platforms
    ADD CONSTRAINT platforms_pkey PRIMARY KEY (id);


--
-- Name: topics topics_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.topics
    ADD CONSTRAINT topics_pkey PRIMARY KEY (id);


--
-- Name: traffic traffic_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT traffic_pkey PRIMARY KEY (trf_announ_id);


--
-- Name: traffic_requests traffic_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_requests
    ADD CONSTRAINT traffic_requests_pkey PRIMARY KEY (id);


--
-- Name: traffic_types traffic_types_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_types
    ADD CONSTRAINT traffic_types_pkey PRIMARY KEY (id);


--
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (transaction_id);


--
-- Name: ad_requests ad_requests_announ_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ad_requests
    ADD CONSTRAINT ad_requests_announ_id_fkey FOREIGN KEY (announ_id) REFERENCES public.announs(announ_id);


--
-- Name: ad_requests ad_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ad_requests
    ADD CONSTRAINT ad_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.accounts(user_id);


--
-- Name: ads ads_country_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT ads_country_fkey FOREIGN KEY (country) REFERENCES public.countries(id);


--
-- Name: ads ads_topic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT ads_topic_fkey FOREIGN KEY (topic) REFERENCES public.topics(id);


--
-- Name: announ_price_history announ_price_history_announ_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announ_price_history
    ADD CONSTRAINT announ_price_history_announ_id_fkey FOREIGN KEY (announ_id) REFERENCES public.announs(announ_id) ON DELETE CASCADE;


--
-- Name: channel_requests channel_requests_announ_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel_requests
    ADD CONSTRAINT channel_requests_announ_id_fkey FOREIGN KEY (announ_id) REFERENCES public.announs(announ_id);


--
-- Name: channel_requests channel_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channel_requests
    ADD CONSTRAINT channel_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.accounts(user_id);


--
-- Name: channels channels_country_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_country_fkey FOREIGN KEY (country) REFERENCES public.countries(id);


--
-- Name: channels channels_topic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT channels_topic_fkey FOREIGN KEY (topic) REFERENCES public.topics(id);


--
-- Name: channels fk_announ_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.channels
    ADD CONSTRAINT fk_announ_id FOREIGN KEY (chn_announ_id) REFERENCES public.announs(announ_id) ON DELETE CASCADE;


--
-- Name: ads fk_announ_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ads
    ADD CONSTRAINT fk_announ_id FOREIGN KEY (ad_announ_id) REFERENCES public.announs(announ_id) ON DELETE CASCADE;


--
-- Name: traffic fk_announ_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT fk_announ_id FOREIGN KEY (trf_announ_id) REFERENCES public.announs(announ_id) ON DELETE CASCADE;


--
-- Name: imgs fk_announ_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.imgs
    ADD CONSTRAINT fk_announ_id FOREIGN KEY (img_announ_id) REFERENCES public.announs(announ_id) ON DELETE CASCADE;


--
-- Name: deals fk_buyer_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT fk_buyer_id FOREIGN KEY (buyer_id) REFERENCES public.accounts(user_id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT fk_buyer_id ON deals; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_buyer_id ON public.deals IS 'Foreign key for deal buyer';


--
-- Name: accounts fk_referrer; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT fk_referrer FOREIGN KEY (referrer_id) REFERENCES public.accounts(user_id) ON DELETE SET NULL NOT VALID;


--
-- Name: CONSTRAINT fk_referrer ON accounts; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_referrer ON public.accounts IS 'Foreign key for referrer';


--
-- Name: announs fk_seller; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.announs
    ADD CONSTRAINT fk_seller FOREIGN KEY (seller_id) REFERENCES public.accounts(user_id) ON DELETE CASCADE;


--
-- Name: deals fk_seller_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.deals
    ADD CONSTRAINT fk_seller_id FOREIGN KEY (seller_id) REFERENCES public.accounts(user_id) ON DELETE CASCADE;


--
-- Name: CONSTRAINT fk_seller_id ON deals; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_seller_id ON public.deals IS 'Foreign key for seller of deal';


--
-- Name: transactions fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.accounts(user_id) ON DELETE CASCADE NOT VALID;


--
-- Name: CONSTRAINT fk_user_id ON transactions; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON CONSTRAINT fk_user_id ON public.transactions IS 'Foreign key for transaction owner';


--
-- Name: traffic traffic_audience_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT traffic_audience_type_fkey FOREIGN KEY (audience_type) REFERENCES public.audience_types(id);


--
-- Name: traffic traffic_country_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT traffic_country_fkey FOREIGN KEY (country) REFERENCES public.countries(id);


--
-- Name: traffic traffic_platform_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT traffic_platform_fkey FOREIGN KEY (platform) REFERENCES public.platforms(id);


--
-- Name: traffic_requests traffic_requests_announ_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_requests
    ADD CONSTRAINT traffic_requests_announ_id_fkey FOREIGN KEY (announ_id) REFERENCES public.announs(announ_id);


--
-- Name: traffic_requests traffic_requests_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic_requests
    ADD CONSTRAINT traffic_requests_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.accounts(user_id);


--
-- Name: traffic traffic_topic_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT traffic_topic_fkey FOREIGN KEY (topic) REFERENCES public.topics(id);


--
-- Name: traffic traffic_traffic_type_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.traffic
    ADD CONSTRAINT traffic_traffic_type_fkey FOREIGN KEY (traffic_type) REFERENCES public.traffic_types(id);


--
-- PostgreSQL database dump complete
--


