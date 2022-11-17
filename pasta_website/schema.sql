DROP TABLE IF EXISTS Request;

CREATE TABLE Request (
  id_request INTEGER PRIMARY KEY AUTOINCREMENT,
  program TEXT NOT NULL,
  query TEXT NOT NULL,
  evidence TEXT NOT NULL,
  option_1 TEXT NOT NULL,
  option_2 TEXT NOT NULL,
  nSamples TEXT NOT NULL,
  blocks TEXT NOT NULL,
  upper TEXT NOT NULL,
  errors TEXT NOT NULL
);