CREATE SCHEMA stg;

CREATE USER etl_user WITH PASSWORD '12345';

grant usage on schema stg to etl_user;

grant select, insert on all tables in schema stg to etl_user;

create table stg."statsSingleSeason" (
"team_id" integer,
"team_name" varchar(30),
"gameType_id" varchar(2),
"gameType_description" varchar(30),
"gameType_postseason" boolean,
"gamesPlayed" integer,
"wins" integer,
"losses" integer,
"ot" integer,
"pts" integer,
"ptPctg" varchar(5),
"goalsPerGame" float(5),
"goalsAgainstPerGame" float(5),
"evGGARatio" float(5),
"powerPlayPercentage" varchar(5),
"powerPlayGoals" float(5),
"powerPlayGoalsAgainst" float(5),
"powerPlayOpportunities" float(5),
"penaltyKillPercentage" varchar(5),
"shotsPerGame" float(5),
"shotsAllowed" float(5),
"winScoreFirst" float(5),
"winOppScoreFirst" float(5),
"winLeadFirstPer" float(5),
"winLeadSecondPer" float(5),
"winOutshootOpp" float(5),
"winOutshotByOpp" float(5),
"faceOffsTaken" float(5),
"faceOffsLost" float(5),
"faceOffsWon" float(5),
"faceOffWinPercentage" varchar(5),
"shootingPctg" float(5),
"savePctg" float(5),
load_dttm timestamp default current_timestamp
);


create table stg."regularSeasonStatRankings" (
"team_id" integer,
"team_name" varchar(30),
"wins" varchar(5),
"losses" varchar(5),
"ot" varchar(5),
"pts" varchar(5),
"ptPctg" varchar(5),
"goalsPerGame" varchar(5),
"goalsAgainstPerGame" varchar(5),
"evGGARatio" varchar(5),
"powerPlayPercentage" varchar(5),
"powerPlayGoals" varchar(5),
"powerPlayGoalsAgainst" varchar(5),
"powerPlayOpportunities" varchar(5),
"penaltyKillOpportunities" varchar(5),
"penaltyKillPercentage" varchar(5),
"shotsPerGame" varchar(5),
"shotsAllowed" varchar(5),
"winScoreFirst" varchar(5),
"winOppScoreFirst" varchar(5),
"winLeadFirstPer" varchar(5),
"winLeadSecondPer" varchar(5),
"winOutshootOpp" varchar(5),
"winOutshotByOpp" varchar(5),
"faceOffsTaken" varchar(5),
"faceOffsWon" varchar(5),
"faceOffsLost" varchar(5),
"faceOffWinPercentage" varchar(5),
"savePctRank" varchar(5),
"shootingPctRank" varchar(5),
load_dttm timestamp default current_timestamp
);