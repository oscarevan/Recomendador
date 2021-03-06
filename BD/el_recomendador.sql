PGDMP     (    5            
    y            el_recomendador    13.2    13.2     ?           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            ?           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            ?           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            ?           1262    57648    el_recomendador    DATABASE     l   CREATE DATABASE el_recomendador WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE = 'Spanish_Mexico.1252';
    DROP DATABASE el_recomendador;
                postgres    false            ?           0    0    DATABASE el_recomendador    ACL     ;   GRANT ALL ON DATABASE el_recomendador TO recomendadoruser;
                   postgres    false    3019            ?            1259    57742    califica    TABLE     ?   CREATE TABLE public.califica (
    puntualidad smallint,
    dificultad smallint,
    dominio smallint,
    usuario_username character varying(30),
    profesor_id integer
);
    DROP TABLE public.califica;
       public         heap    postgres    false            ?            1259    65892 
   peticiones    TABLE     I   CREATE TABLE public.peticiones (
    nombre_maestro character varying
);
    DROP TABLE public.peticiones;
       public         heap    postgres    false            ?            1259    57710    profesor    TABLE     w   CREATE TABLE public.profesor (
    id integer NOT NULL,
    nombre character varying(100),
    calificacion numeric
);
    DROP TABLE public.profesor;
       public         heap    postgres    false            ?            1259    57708    profesor_id_seq    SEQUENCE     ?   CREATE SEQUENCE public.profesor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.profesor_id_seq;
       public          postgres    false    202            ?           0    0    profesor_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.profesor_id_seq OWNED BY public.profesor.id;
          public          postgres    false    201            ?            1259    57718    resena    TABLE     ?   CREATE TABLE public.resena (
    materia character varying(50),
    comentario character varying(1024),
    usuariousername character varying(30),
    profesorid integer
);
    DROP TABLE public.resena;
       public         heap    postgres    false            ?            1259    57650    usuario    TABLE     ?   CREATE TABLE public.usuario (
    username character varying(30) NOT NULL,
    correo character varying(255) NOT NULL,
    contrasena character varying(255) NOT NULL
);
    DROP TABLE public.usuario;
       public         heap    postgres    false            6           2604    57713    profesor id    DEFAULT     j   ALTER TABLE ONLY public.profesor ALTER COLUMN id SET DEFAULT nextval('public.profesor_id_seq'::regclass);
 :   ALTER TABLE public.profesor ALTER COLUMN id DROP DEFAULT;
       public          postgres    false    202    201    202            ?          0    57742    califica 
   TABLE DATA           c   COPY public.califica (puntualidad, dificultad, dominio, usuario_username, profesor_id) FROM stdin;
    public          postgres    false    204   ?       ?          0    65892 
   peticiones 
   TABLE DATA           4   COPY public.peticiones (nombre_maestro) FROM stdin;
    public          postgres    false    205   V       ?          0    57710    profesor 
   TABLE DATA           <   COPY public.profesor (id, nombre, calificacion) FROM stdin;
    public          postgres    false    202   ?       ?          0    57718    resena 
   TABLE DATA           R   COPY public.resena (materia, comentario, usuariousername, profesorid) FROM stdin;
    public          postgres    false    203   s       ?          0    57650    usuario 
   TABLE DATA           ?   COPY public.usuario (username, correo, contrasena) FROM stdin;
    public          postgres    false    200   ?       ?           0    0    profesor_id_seq    SEQUENCE SET     =   SELECT pg_catalog.setval('public.profesor_id_seq', 6, true);
          public          postgres    false    201            :           2606    57715    profesor profesor_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.profesor
    ADD CONSTRAINT profesor_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.profesor DROP CONSTRAINT profesor_pkey;
       public            postgres    false    202            8           2606    57657    usuario usuario_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (username);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public            postgres    false    200            ;           2606    57727    resena id_profesor    FK CONSTRAINT     w   ALTER TABLE ONLY public.resena
    ADD CONSTRAINT id_profesor FOREIGN KEY (profesorid) REFERENCES public.profesor(id);
 <   ALTER TABLE ONLY public.resena DROP CONSTRAINT id_profesor;
       public          postgres    false    2874    203    202            =           2606    57745    califica profesor_id    FK CONSTRAINT     z   ALTER TABLE ONLY public.califica
    ADD CONSTRAINT profesor_id FOREIGN KEY (profesor_id) REFERENCES public.profesor(id);
 >   ALTER TABLE ONLY public.califica DROP CONSTRAINT profesor_id;
       public          postgres    false    204    202    2874            <           2606    57732    resena username_usuario    FK CONSTRAINT     ?   ALTER TABLE ONLY public.resena
    ADD CONSTRAINT username_usuario FOREIGN KEY (usuariousername) REFERENCES public.usuario(username);
 A   ALTER TABLE ONLY public.resena DROP CONSTRAINT username_usuario;
       public          postgres    false    2872    203    200            ?   a   x?340?4?b???TNc.Ct!C.SNBR?Yp??d???@?p??(?f?Ō???F`U?e?y?9??y??`??QC.K????H?&\1z\\\ ɇ#?      ?   B   x??/NN,Rp-K???)??Sp/-?L-*J?RH?\??@?ԢĢ?|??????̒?b?d? *??      ?   ?   x?%?9?0D??S?D1aI?&)@I3??;IA?Q8 ???0Ѝ?Fo?CC{V??ڣ????????c???4-]P??a?P?4ܴu?O?4??F?{???i]????ix???J????????7x??m_?q?&?"?ЇK?2A????T?\&R?.m#+???},?è?k????1ȓ,?D?mD?      ?      x?????? ? ?      ?   ?   x?U??
?@???)|?R:?֥???
?as\????M[?$????\-?>b%?G+Ij?&X?w?շ??.9*???~E6?Q
??h?/gRI??7um????l?i?!??5+?ϼ??i?h?zE?     