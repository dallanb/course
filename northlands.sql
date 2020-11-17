--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.19
-- Dumped by pg_dump version 9.6.19

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

ALTER TABLE ONLY public.hole DROP CONSTRAINT hole_course_uuid_fkey;
ALTER TABLE ONLY public.hole DROP CONSTRAINT hole_pkey;
ALTER TABLE ONLY public.course DROP CONSTRAINT course_pkey;
DROP TABLE public.hole;
DROP TABLE public.course;
DROP TYPE public.statusenum;
DROP EXTENSION plpgsql;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: course
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO course;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: course
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: statusenum; Type: TYPE; Schema: public; Owner: course
--

CREATE TYPE public.statusenum AS ENUM (
    'pending',
    'active',
    'inactive'
);


ALTER TYPE public.statusenum OWNER TO course;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: course; Type: TABLE; Schema: public; Owner: course
--

CREATE TABLE public.course (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    name character varying NOT NULL,
    status public.statusenum NOT NULL,
    line_1 character varying,
    line_2 character varying,
    city character varying,
    province character varying,
    country character varying(2)
);


ALTER TABLE public.course OWNER TO course;

--
-- Name: hole; Type: TABLE; Schema: public; Owner: course
--

CREATE TABLE public.hole (
    uuid uuid NOT NULL,
    ctime bigint,
    mtime bigint,
    name character varying,
    number integer NOT NULL,
    par integer NOT NULL,
    distance integer NOT NULL,
    course_uuid uuid
);


ALTER TABLE public.hole OWNER TO course;

--
-- Data for Name: course; Type: TABLE DATA; Schema: public; Owner: course
--

COPY public.course (uuid, ctime, mtime, name, status, line_1, line_2, city, province, country) FROM stdin;
09443c98-6559-4247-9308-7099ff09ecc4	1605570256032	\N	Northlands Golf Course	pending	3400 Anne Macdonald Way	\N	North Vancouver	British Columbia	CA
\.


--
-- Data for Name: hole; Type: TABLE DATA; Schema: public; Owner: course
--

COPY public.hole (uuid, ctime, mtime, name, number, par, distance, course_uuid) FROM stdin;
5690cf0b-bc11-4cc3-b8ec-e65306a84c51	1605570313809	\N	Uno	1	4	424	09443c98-6559-4247-9308-7099ff09ecc4
a809026e-faf6-49cd-971b-9237f3d6c9e9	1605570742678	\N	\N	2	4	353	09443c98-6559-4247-9308-7099ff09ecc4
5b13186e-be20-47d2-8198-6cf639d0f020	1605570757526	\N	\N	3	3	177	09443c98-6559-4247-9308-7099ff09ecc4
727d316a-e76c-4cae-9686-090a048ba6c1	1605570804114	\N	\N	4	5	558	09443c98-6559-4247-9308-7099ff09ecc4
5cede585-8ffe-4eac-9f39-b5dbfbceda0b	1605570815872	\N	\N	5	4	434	09443c98-6559-4247-9308-7099ff09ecc4
43f4dbd3-bfb1-4371-90b0-a473f7d0975f	1605570845977	\N	\N	6	4	368	09443c98-6559-4247-9308-7099ff09ecc4
469994a4-fc56-4cb6-9e21-8f06890c0770	1605570855052	\N	\N	7	4	401	09443c98-6559-4247-9308-7099ff09ecc4
fcc7d3db-1bd3-4429-931b-20dce4628f08	1605570867139	\N	\N	8	3	220	09443c98-6559-4247-9308-7099ff09ecc4
530ab34c-5e2e-4f90-8942-3b1d62d17969	1605570994636	\N	\N	9	4	419	09443c98-6559-4247-9308-7099ff09ecc4
bfef68c9-4ad0-4da4-82e7-e1edae88f6d4	1605571005634	\N	\N	10	4	337	09443c98-6559-4247-9308-7099ff09ecc4
826a5045-6ca9-4647-9554-78cf695257b6	1605571014547	\N	\N	11	4	412	09443c98-6559-4247-9308-7099ff09ecc4
bf445551-795e-46d3-955a-18cdde6901a1	1605571026025	\N	\N	12	3	190	09443c98-6559-4247-9308-7099ff09ecc4
2611af22-186d-495b-aad2-307c0e6e4252	1605571193641	\N	\N	13	4	322	09443c98-6559-4247-9308-7099ff09ecc4
f86f25ad-6535-468a-9322-38015fa307d1	1605571209016	\N	\N	14	3	194	09443c98-6559-4247-9308-7099ff09ecc4
6af93772-9885-4342-93b3-056e865848c9	1605571219336	\N	\N	15	5	547	09443c98-6559-4247-9308-7099ff09ecc4
91765bd6-be8a-4831-a865-93de8e62c264	1605571229709	\N	\N	16	3	168	09443c98-6559-4247-9308-7099ff09ecc4
a586e7c0-4f4b-43c2-9631-6f4867c094f0	1605571241468	\N	\N	17	5	491	09443c98-6559-4247-9308-7099ff09ecc4
4d948d57-3026-437a-801f-cd1a4e59deef	1605571251981	1605571315703	Fin	18	5	508	09443c98-6559-4247-9308-7099ff09ecc4
\.


--
-- Name: course course_pkey; Type: CONSTRAINT; Schema: public; Owner: course
--

ALTER TABLE ONLY public.course
    ADD CONSTRAINT course_pkey PRIMARY KEY (uuid);


--
-- Name: hole hole_pkey; Type: CONSTRAINT; Schema: public; Owner: course
--

ALTER TABLE ONLY public.hole
    ADD CONSTRAINT hole_pkey PRIMARY KEY (uuid);


--
-- Name: hole hole_course_uuid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: course
--

ALTER TABLE ONLY public.hole
    ADD CONSTRAINT hole_course_uuid_fkey FOREIGN KEY (course_uuid) REFERENCES public.course(uuid);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: course
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

