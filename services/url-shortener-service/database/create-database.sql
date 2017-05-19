DROP DATABASE UrlShortener;

CREATE DATABASE UrlShortener WITH ENCODING = 'UTF8';

DROP TABLE IF EXISTS url;

CREATE TABLE url (
  id BIGSERIAL PRIMARY KEY,
  value TEXT NOT NULL UNIQUE,
  creation_time TIMESTAMP DEFAULT current_timestamp
);

CREATE OR REPLACE FUNCTION send_url_deletion_notification () RETURNS TRIGGER AS
  $send_url_deletion_notification$
  BEGIN
    IF (tg_op <> 'DELETE') THEN
      RAISE EXCEPTION 'Function send_url_deletion_notification does not support %s', tg_op;
    END IF;
    PERFORM pg_notify('url_deletion_notification', OLD.id::text);
    RETURN NULL;
  END;
  $send_url_deletion_notification$ LANGUAGE plpgsql;

CREATE TRIGGER url_deletion_notification AFTER DELETE ON url
  FOR EACH ROW EXECUTE PROCEDURE send_url_deletion_notification();
