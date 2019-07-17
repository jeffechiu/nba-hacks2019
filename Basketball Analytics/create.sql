CREATE TABLE Event_Codes (
	event_msg_type int,
	action_type int,
	event_msg_type_description varchar(40),
	action_type_description varchar(40)
);

CREATE TABLE Game_Lineup (
	game_id varchar(40),
	period int,
	person_id varchar(40),
	team_id varchar(40),
	status varchar(40)
);

CREATE TABLE Play_by_Play (
	game_id varchar(40),
	event_num int,
	event_msg_type int,
	period int,
	wc_time int,
	pc_time int,
	option1 int,
	option2 int,
	option3 int,
	team_id varchar(40),
	person1 varchar(40),
	person2 varchar(40),
	person3 varchar(40),
	team_id_type int,
	person1_type int,
	person2_type int,
	person3_type int
);

CREATE TABLE Given_Lineup (
	game_id varchar(40),
	period int,
	start_time int,
	end_time int,
	team_id1 varchar(40),
	person1_1 varchar(40),
	person1_2 varchar(40),
	person1_3 varchar(40),
	person1_4 varchar(40),
	person1_5 varchar(40),
	team_id2 varchar(40),
	person2_1 varchar(40),
	person2_2 varchar(40),
	person2_3 varchar(40),
	person2_4 varchar(40),
	person2_5 varchar(40)
);