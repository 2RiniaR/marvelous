-- Drop tables
DROP TABLE IF EXISTS users;

-- Create tables
CREATE TABLE users(
    discord_id bigint unsigned not null primary key,
    display_name varchar(64) not null,
    marvelous_point int signed,
    super_marvelous_left int signed,
    marvelous_bonus_step int unsigned,
    marvelous_bonus_today_step int unsigned,
    booing_penalty_step int unsigned,
    booing_penalty_today_step int unsigned,
    survival_bonus_given boolean
);
