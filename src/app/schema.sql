DROP TABLE IF EXISTS links;

CREATE TABLE links (
  shortname TEXT PRIMARY KEY,
  full_url TEXT NOT NULL
);
