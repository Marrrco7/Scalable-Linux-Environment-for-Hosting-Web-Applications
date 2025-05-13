CREATE SCHEMA audit;
CREATE SCHEMA analytics;

CREATE ROLE app_reader  NOINHERIT;
CREATE ROLE app_writer  NOINHERIT;
CREATE ROLE auditor     NOINHERIT;
CREATE ROLE report_user NOINHERIT;
CREATE ROLE backup_role NOINHERIT;

ALTER ROLE backup_user CREATEDB;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;
GRANT SELECT,INSERT,UPDATE,DELETE ON ALL TABLES IN SCHEMA public TO app_writer;
GRANT SELECT ON ALL TABLES IN SCHEMA audit TO auditor;
GRANT SELECT ON ALL TABLES IN SCHEMA analytics TO report_user;

GRANT CONNECT ON DATABASE videogames_db TO backup_role;
GRANT USAGE ON SCHEMA public,audit,analytics TO backup_role;
GRANT SELECT ON ALL TABLES IN SCHEMA public,audit,analytics TO backup_role;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public,audit,analytics TO backup_role;

ALTER DEFAULT PRIVILEGES IN SCHEMA public,audit,analytics
  GRANT SELECT ON TABLES    TO backup_role;
ALTER DEFAULT PRIVILEGES IN SCHEMA public,audit,analytics
  GRANT SELECT ON SEQUENCES TO backup_role;

GRANT USAGE ON SCHEMA audit      TO app_writer;
GRANT INSERT ON audit.audit_log TO app_writer;
GRANT USAGE,SELECT ON SEQUENCE   audit.audit_log_id_seq TO app_writer;

CREATE USER game_reader     WITH PASSWORD 'readerpass';
CREATE USER game_writer     WITH PASSWORD 'writerpass';
CREATE USER audit_user      WITH PASSWORD 'auditpass';
CREATE USER report_user_app WITH PASSWORD 'reportpass';
CREATE USER backup_user     WITH PASSWORD 'backuppass';

GRANT app_reader  TO game_reader;
GRANT app_writer  TO game_writer;
GRANT auditor     TO audit_user;
GRANT report_user TO report_user_app;
GRANT backup_role TO backup_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT,INSERT,UPDATE,DELETE ON TABLES TO app_writer;

GRANT USAGE ON SCHEMA public                   TO report_user;
GRANT SELECT ON TABLE public.django_session    TO report_user;
GRANT SELECT ON TABLE public.auth_user         TO report_user;
GRANT SELECT ON TABLE public.django_content_type TO report_user;
GRANT SELECT ON TABLE public.auth_permission   TO report_user;

-------------------------------------------------------------------------------

CREATE TABLE audit.audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    action TEXT,
    changed_data JSONB,
    changed_at TIMESTAMPTZ DEFAULT now(),
    changed_by TEXT
);



CREATE OR REPLACE FUNCTION audit_if_modified()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit.audit_log (table_name, action, changed_data, changed_by)
    VALUES (
        TG_TABLE_NAME,
        TG_OP,
        CASE
            WHEN TG_OP = 'DELETE' THEN row_to_json(OLD)
            ELSE row_to_json(NEW)
        END,
        current_user
    );
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;



CREATE TRIGGER trg_audit_videogame
AFTER INSERT OR UPDATE OR DELETE ON public.videogames_register_videogame
FOR EACH ROW
EXECUTE FUNCTION audit_if_modified();

CREATE TRIGGER trg_audit_genre
AFTER INSERT OR UPDATE OR DELETE ON public.videogames_register_genre
FOR EACH ROW
EXECUTE FUNCTION public.audit_if_modified();

CREATE TRIGGER trg_audit_user
AFTER INSERT OR UPDATE OR DELETE ON public.auth_user
FOR EACH ROW
EXECUTE FUNCTION public.audit_if_modified();


CREATE TRIGGER trg_audit_review
AFTER INSERT OR UPDATE OR DELETE
  ON public.videogames_register_review
FOR EACH ROW
  EXECUTE FUNCTION audit_if_modified();

CREATE TRIGGER trg_audit_developer
AFTER INSERT OR UPDATE OR DELETE
  ON public.videogames_register_developer
FOR EACH ROW
  EXECUTE FUNCTION audit_if_modified();


CREATE TRIGGER trg_audit_copy
AFTER INSERT OR UPDATE OR DELETE
  ON public.videogames_register_copy
FOR EACH ROW
  EXECUTE FUNCTION audit_if_modified();


CREATE TRIGGER trg_audit_userprofile
AFTER INSERT OR UPDATE OR DELETE
  ON public.videogames_register_userprofile
FOR EACH ROW
  EXECUTE FUNCTION audit_if_modified();




SELECT * FROM audit.audit_log ORDER BY changed_at DESC;

----------------------------------------------------------------------------------------------

CREATE MATERIALIZED VIEW analytics.cumulative_releases AS
WITH yearly_counts AS (
    SELECT
        EXTRACT(YEAR FROM release_date)::INT AS year,
        COUNT(*) AS games_this_year
    FROM public.videogames_register_videogame
    GROUP BY EXTRACT(YEAR FROM release_date)
)
SELECT
    year,
    games_this_year,
    SUM(games_this_year) OVER (ORDER BY year) AS cumulative_total
FROM yearly_counts
ORDER BY year;



GRANT SELECT ON analytics.cumulative_releases TO report_user;


SELECT * FROM analytics.cumulative_releases;


CREATE MATERIALIZED VIEW analytics.top_reviewed_games_per_genre AS
WITH ranked AS (
  SELECT
    vg.id         AS game_id,
    vg.title      AS game_title,
    g.title       AS genre,
    COUNT(r.id)   AS review_count,
    RANK() OVER (
      PARTITION BY g.id
      ORDER BY COUNT(r.id) DESC
    ) AS rank_in_genre
  FROM public.videogames_register_videogame vg
  JOIN public.videogames_register_genre g
    ON vg.genre_id = g.id
  LEFT JOIN public.videogames_register_review r
    ON vg.id = r.game_id
  GROUP BY vg.id, vg.title, g.id, g.title
)
SELECT *
FROM ranked
WHERE rank_in_genre <= 5;

GRANT SELECT ON analytics.top_reviewed_games_per_genre TO report_user;



CREATE MATERIALIZED VIEW analytics.avg_rating_per_game AS
SELECT
  vg.id           AS game_id,
  vg.title        AS game_title,
  COUNT(r.id)     AS review_count,
  ROUND(AVG(r.rating)::numeric, 2) AS avg_rating
FROM public.videogames_register_videogame vg
LEFT JOIN public.videogames_register_review r
  ON vg.id = r.game_id
GROUP BY vg.id, vg.title
ORDER BY avg_rating DESC;

GRANT SELECT ON analytics.avg_rating_per_game TO report_user;


CREATE MATERIALIZED VIEW analytics.copy_availability_summary AS
SELECT
  vg.id            AS game_id,
  vg.title         AS game_title,
  COUNT(c.id)      AS total_copies,
  SUM(CASE WHEN c.condition = 'available' THEN 1 ELSE 0 END) AS available_copies
FROM public.videogames_register_videogame vg
LEFT JOIN public.videogames_register_copy c
  ON vg.id = c.game_id
GROUP BY vg.id, vg.title
ORDER BY total_copies DESC;

GRANT SELECT ON analytics.copy_availability_summary TO report_user;



------------------------------------------------------------------------------------

EXPLAIN ANALYZE
SELECT genre_id, COUNT(*) FROM public.videogames_register_videogame
GROUP BY genre_id;


EXPLAIN ANALYZE
SELECT * FROM public.videogames_register_videogame
WHERE release_date >= '2022-01-01';


EXPLAIN ANALYZE
SELECT * FROM public.videogames_register_videogame
WHERE LOWER(title) LIKE '%fifa%';


EXPLAIN ANALYZE
SELECT *
FROM public.videogames_register_videogame
ORDER BY release_date DESC
LIMIT 10;


EXPLAIN ANALYZE
SELECT *
FROM public.videogames_register_videogame
WHERE to_tsvector('english', description) @@ plainto_tsquery('football');


CREATE INDEX idx_release_date ON public.videogames_register_videogame(release_date);

CREATE INDEX idx_genre_id ON public.videogames_register_videogame(genre_id);

CREATE INDEX idx_title_lower ON public.videogames_register_videogame(LOWER(title));

CREATE INDEX idx_developer_name ON public.videogames_register_developer(LOWER(name));

CREATE INDEX idx_review_rating ON public.videogames_register_review(rating);

CREATE INDEX idx_review_user_id ON public.videogames_register_review(user_id);

CREATE INDEX idx_copy_condition ON public.videogames_register_copy(condition);

CREATE INDEX idx_userprofile_user_id ON public.videogames_register_userprofile(user_id);

CREATE INDEX idx_userprofile_country ON public.videogames_register_userprofile(country);

CREATE INDEX idx_description_tsvector
ON public.videogames_register_videogame
USING GIN(to_tsvector('english', description));




SELECT * FROM videogames_register_developer WHERE videogames_register_developer.id IS NULL;

--------------------------------------------------------
--additional queries


SELECT
    u.username,
    COUNT(DISTINCT r.game_id) AS reviewed_games
FROM public.auth_user u
JOIN public.videogames_register_review r ON u.id = r.user_id
GROUP BY u.username
HAVING COUNT(DISTINCT r.game_id) > 3;



SELECT
    vg.title,
    ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
    COUNT(r.id) AS total_reviews
FROM public.videogames_register_videogame vg
JOIN public.videogames_register_review r ON vg.id = r.game_id
GROUP BY vg.title
HAVING COUNT(r.id) >= 2
ORDER BY avg_rating DESC;


SELECT *
FROM (
    SELECT
        vg.id AS game_id,
        vg.title AS game_title,
        g.title AS genre,
        COUNT(r.id) AS review_count,
        RANK() OVER (PARTITION BY g.id ORDER BY COUNT(r.id) DESC) AS rank_in_genre
    FROM public.videogames_register_videogame vg
    JOIN public.videogames_register_genre g ON vg.genre_id = g.id
    LEFT JOIN public.videogames_register_review r ON vg.id = r.game_id
    GROUP BY vg.id, vg.title, g.id, g.title
) ranked
WHERE rank_in_genre <= 3;

