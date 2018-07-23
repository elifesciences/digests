-- TODO: compare with builder-base-formula scripts
CREATE USER app_user WITH PASSWORD 'app_password';
GRANT ALL PRIVILEGES ON DATABASE digests TO app_user;
