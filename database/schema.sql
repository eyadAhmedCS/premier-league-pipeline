CREATE TABLE Seasons(
season_id INT PRIMARY KEY,
year INT,
start_date TEXT CHECK (start_date LIKE '____-__-__'),
end_date TEXT CHECK (end_date LIKE '____-__-__'),
"current" INT DEFAULT 0 CHECK("current" IN (0,1)),
CHECK (start_date<end_date AND start_date <date('now'))
);

CREATE TABLE Teams(
team_id INT,
name VARCHAR(200) NOT NULL,
city VARCHAR(200) NOT NULL,
stadium VARCHAR(200) NOT NULL,
capacity INT,
founded_year INT,
season_id INT,
PRIMARY KEY(team_id,season_id),
FOREIGN KEY (season_id) REFERENCES Seasons(season_id)
);

CREATE TABLE Matches(
match_id INT PRIMARY KEY,
"date" TEXT,
matchweek INT,
referee VARCHAR(200),
status TEXT GENERATED ALWAYS AS (
	CASE
		WHEN "date">=date('now') THEN 'NOT Played'
		WHEN "date"<date('now') THEN 'Finished'
		ELSE NULL
	END	
) STORED,
home_score_ht INT,
away_score_ht INT,
home_score_ft INT,
away_score_ft INT,
home_team_id INT,
away_team_id INT,
season_id INT,
winner TEXT,
FOREIGN KEY (home_team_id,season_id) REFERENCES Teams(team_id,season_id),
FOREIGN KEY (away_team_id,season_id) REFERENCES Teams(team_id,season_id),
FOREIGN KEY (season_id) REFERENCES Seasons(season_id)
);

CREATE TABLE Standings(
matchweek INT,
team_id INT,
season_id INT,
rank INT,
points INT,
wins INT,
draws INT,
losses INT,
goals_for INT,
goals_against INT,
goal_diff INT,
CHECK (points<=114 AND points>=0 AND wins <=38 AND wins >=0 
AND draws <=38 AND draws >=0 AND losses <=38 AND losses >=0 AND goal_diff = goals_for-goals_against),
FOREIGN KEY (team_id,season_id) REFERENCES Teams(team_id,season_id),
PRIMARY KEY(matchweek,team_id,season_id)
);

CREATE TABLE Team_Match_Stats(
match_id INT,
team_id INT,
season_id INT,
possession INT,
shots_total INT,
shots_on_target INT,
corners INT,
fouls INT,
offsides INT,
yellow_cards INT,
red_cards INT,
passes_total INT,
passes_accuracy INT,
goals_scored INT,
goals_conceded INT,
FOREIGN KEY (team_id,season_id) REFERENCES Teams(team_id,season_id),
FOREIGN KEY (match_id) REFERENCES Matches(match_id),
PRIMARY KEY(team_id,season_id,match_id)
);

CREATE TABLE Coach(
coach_id INT,
team_id INT,
season_id INT,
name VARCHAR(200),
FOREIGN KEY (team_id,season_id) REFERENCES Teams(team_id,season_id),
PRIMARY KEY(team_id,season_id,coach_id)
);

