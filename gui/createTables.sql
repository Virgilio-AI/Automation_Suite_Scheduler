-- create database if not exists automation_suite_database ;
use automation_suite ;


create table if not exists recurrent_actions_table(
	id int not null auto_increment,
	info varchar(300),
	action varchar(50),
	name varchar(100),
	weeks int,
	action_time int,
	hour int,
	minute int,
	primary key(id)
);

-- show tables ;

insert into recurrent_actions_table(info,action,name,weeks,action_time,hour,minute) values("test info","test action","test name",1,10,12,30) ;


select * from recurrent_actions_table ;
