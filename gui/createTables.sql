-- create database if not exists automation_suite_database ;
use automation_suite ;

-- drop table if exists WeeklyEvents ;
-- drop table if exists UniqueEvents ;
-- drop table if exists Event ;
-- drop table if exists EventType ;

-- data types -> varchar(n),Int,DECIMAL(M,N),BLOB,DATE,TIMESTAMP
-- constrains -> not null,unique,auto_increment
-- on delete -> on delete set null, on delete cascade
-- snippets -> foreign,

-- data types -> varchar(n),Int,DECIMAL(M,N),BLOB,DATE,TIMESTAMP
-- constrains -> not null,unique,auto_increment
-- on delete -> on delete set null, on delete cascade
-- snippets -> foreign,

-- EXAMPLE
-- student_id INT,
-- name VARCHAR(20) not null,
-- major VARCHAR(20) unique,
-- primary key(student_id)
-- foreign key(student_id) references branch(branch_id) on delete cascade

create table if not exists EventType(
	id int not null unique auto_increment,
	name varchar(100),
	actionDescription varchar(300),
	primary key(id)
);

create table if not exists Event(
	id int not null unique auto_increment,
	actionTime int not null,
	EventTypeId int not null,
	primary key(id),
	foreign key (EventTypeId) references EventType(id)
);
create table if not exists WeeklyEvents(
	id int not null unique auto_increment,
	EventId int not null,
	yearStart int not null,
	monthStart int not null,
	dayStart int not null,
	daysActive int not null,

	primary key(id),
	foreign key (EventId) references Event(id)
);
create table if not exists UniqueEvents(
	id int not null unique auto_increment,
	EventId int not null,

	year int not null,
	month int not null,
	day int not null,
	hour int not null,
	minute int not null,

	primary key(id),
	foreign key (EventId) references Event(id)
);




show tables ;
describe UniqueEvents ;
describe WeeklyEvents ;
describe Event ;
describe EventType ;


-- insert into EventType(name,actionDescription) values("alert","gives a personalized voice alert for the system") ;
-- insert into EventType(name,actionDescription) values("zoom","initiates a zoom meeting") ;
-- insert into EventType(name,actionDescription) values("alarm","reproduces an alarm") ;
-- insert a weekly event

-- insert into Event(actionTime,EventTypeId) values(1800,(select id from EventType where name = 'alarm')) ;
-- insert into WeeklyEvents(EventId,yearStart,monthStart,dayStart,daysActive) values((select count(id) from Event),2021,8,23,100) ;
-- insert a unique event
insert into Event(actionTime,EventTypeId) values(1800,(select id from EventType where name = 'alert')) ;
insert into UniqueEvents(EventId,year,month,day,hour,minute) values((select count(id) from Event),2022,4,12,14,30) ;


-- describe WeeklyEvents ;


-- visualize data

-- select * from WeeklyEvents ;
-- 
-- 
-- select * from Event ;
-- 
-- select * from EventType ;
-- 
-- select * from UniqueEvents ;





