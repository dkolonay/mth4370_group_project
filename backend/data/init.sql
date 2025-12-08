CREATE TABLE api_movie (
    id INTEGER,
    title VARCHAR(1000),
    vote_average REAL,
    vote_count INTEGER,
    -- _status VARCHAR(255),
    release_date VARCHAR(1000),
    revenue BIGINT,
    runtime INTEGER,
    -- adult BOOLEAN,
    backdrop_path VARCHAR(1000),
    budget BIGINT,
    -- homepage VARCHAR(2000),
    -- imdb_id VARCHAR(1000),
    -- original_language VARCHAR(1000),
    -- original_title VARCHAR(1000),
    overview VARCHAR(2000),
    popularity REAL,
    poster_path VARCHAR(1000),
    tagline VARCHAR(1000),
    genres VARCHAR(1000),
    -- production_companies VARCHAR(2000),
    -- production_countries VARCHAR(5000),
    -- spoken_languages VARCHAR(2000),
    keywords VARCHAR(2000),
    PRIMARY KEY (id)
);

COPY api_movie FROM '/docker-entrypoint-initdb.d/movie_dataset_cleaned.csv' DELIMITER ',' CSV HEADER;