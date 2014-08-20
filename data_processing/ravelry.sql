CREATE TABLE Projects(
	user_id integer,
	username text, 
	pattern_name text,
	pattern_id integer,
	status_name ENUM('Finished', 'In progress', 'Hibernating', 'Frogged'),
	started date,
	completed date,
	tag_names text,
	favorites_count integer,
	photos_count integer,
	comments_count integer,
	craft_id integer,
	created_at datetime,
	made_for text,
	progress integer,
	rating integer);
	
CREATE INDEX index_user ON Projects (user_id);
CREATE INDEX index_pattern ON Projects (pattern_id);

CREATE TABLE Queues(
	user_id integer,
	username text,
	pattern_name text,
	pattern_id integer,
	created_at date,
	position_in_queue integer,
	skeins integer,
	yarn_id text,
	yarn_name text);
	
CREATE INDEX index_user ON Queues (user_id);
CREATE INDEX index_pattern ON Queues (pattern_id);

CREATE TABLE Patterns(
	pattern_id integer PRIMARY KEY,
	pattern_name text,
	comments_count integer,
	craft_id integer,
	difficulty_avg float,
	difficulty_count integer,
	downloadable bool, 
	favorites_count integer,
	is_free bool,
	yardage integer,
	yardage_max integer,
	projects_count integer,
	queued_count integer,
	rating_avg float,
	rating_count integer,
	ravelry_download bool,
	knit_gauge integer,
	weight_name text,
	ply integer,
	wpi integer,
	categories text,
	posted_at date);
	
CREATE TABLE Photos(
	pattern_id integer PRIMARY KEY,
	pattern_name text,
	pattern_photo text);
