PRAGMA foreign_keys = ON;
CREATE TABLE Seasons(
season_id INT PRIMARY KEY,
"year" INT,
start_date TEXT CHECK (date(start_date) IS NOT NULL),
end_date TEXT CHECK (date(end_date) IS NOT NULL),
"current" INT DEFAULT 0 CHECK("current" IN (0,1)),
CHECK (start_date<end_date)
);

CREATE TABLE Teams(
team_id INT,
name VARCHAR(200) NOT NULL,
city VARCHAR(200) NOT NULL,
stadium VARCHAR(200) NOT NULL,
capacity INT CHECK(capacity > 0),
founded_year INT CHECK(founded_year >= 1800),
PRIMARY KEY(team_id)
);

CREATE TABLE Matches(
match_id INT PRIMARY KEY,
match_date TEXT CHECK(date(match_date) IS NOT NULL),
matchweek INT,
referee VARCHAR(200),
status VARCHAR(200),
home_score_ht INT,
away_score_ht INT,
home_score_ft INT,
away_score_ft INT,
home_team_id INT,
away_team_id INT,
season_id INT,
winner_team_id INT,
FOREIGN KEY (home_team_id) REFERENCES Teams(team_id),
FOREIGN KEY (away_team_id) REFERENCES Teams(team_id),
FOREIGN KEY (winner_team_id) REFERENCES Teams(team_id),
FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
CHECK(home_team_id <> away_team_id),
CHECK(home_score_ht >= 0),
CHECK(away_score_ht >= 0),
CHECK(home_score_ft >= 0),
CHECK(away_score_ft >= 0)
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
FOREIGN KEY (team_id) REFERENCES Teams(team_id),
FOREIGN KEY (season_id) REFERENCES Seasons(season_id),
PRIMARY KEY(matchweek,team_id,season_id),
CHECK(rank > 0),
CHECK(wins + draws + losses <= 38)
);

CREATE TABLE Team_Match_Stats(
match_id INT,
team_id INT,
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
FOREIGN KEY (team_id) REFERENCES Teams(team_id),
FOREIGN KEY (match_id) REFERENCES Matches(match_id),
PRIMARY KEY(team_id,match_id),
CHECK(shots_on_target <= shots_total),
CHECK(possession BETWEEN 0 AND 100),
CHECK(passes_accuracy BETWEEN 0 AND 100),
CHECK(shots_total >= 0),
CHECK(corners >= 0),
CHECK(fouls >= 0),
CHECK(offsides >= 0),
CHECK(yellow_cards >= 0),
CHECK(red_cards >= 0),
CHECK(passes_total >= 0),
CHECK(goals_scored >= 0),
CHECK(goals_conceded >= 0)
);

CREATE TABLE Coach(
coach_id INT,
age INT,
name VARCHAR(200) NOT NULL,
country VARCHAR(200),
PRIMARY KEY(coach_id)
);

CREATE TABLE Coachs_teams(
coach_id INT,
team_id INT,
start_date TEXT CHECK(date(start_date) IS NOT NULL),
end_date TEXT CHECK(end_date IS NULL OR date(end_date) IS NOT NULL),
CHECK(start_date < end_date),
FOREIGN KEY (team_id) REFERENCES Teams(team_id),
FOREIGN KEY(coach_id) REFERENCES Coach(coach_id),
PRIMARY KEY(team_id,start_date,coach_id)
);

