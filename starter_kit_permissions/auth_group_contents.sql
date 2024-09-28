-- Connect to the SQLite database
sqlite3 bd.sqlite3

-- Insert data into the auth_group table
INSERT INTO auth_group (id, name) VALUES
(1, 'Managers'),
(2, 'Unauthorized Users'),
(3, 'Service Companies'),
(4, 'Clients'),
(5, 'Admins');