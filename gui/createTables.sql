-- create database if not exists automation_suite_database ;
use automation_suite ;

drop table if exists WeeklyEvents_DayOfTheWeek ;
drop table if exists WeeklyEvents ;
drop table if exists UniqueEvents ;
drop table if exists Event ;
drop table if exists EventType ;
drop table if exists DayOfTheWeek ;

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

create table if not exists DayOfTheWeek(
	id int not null unique auto_increment,

	day varchar(50),

	primary key(id)
);

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
	hour int not null,
	minute int not null,
	actionInformation varchar(300) not null,

	primary key(id),
	foreign key (EventTypeId) references EventType(id) on delete cascade
);

create table if not exists WeeklyEvents(
	id int not null unique auto_increment,
	EventId int not null,


	yearStart int not null,
	monthStart int not null,
	dayStart int not null,
	daysActive int not null,

	primary key(id),
	foreign key (EventId) references Event(id) on delete cascade
);
create table WeeklyEvents_DayOfTheWeek(
	id int not null unique auto_increment,

	WeeklyEventsId int not null,
	DayOfTheWeekId int not null,

	primary key(id),
	foreign key (WeeklyEventsId) references WeeklyEvents(id) on delete cascade,
	foreign key (DayOfTheWeekId) references DayOfTheWeek(id) on delete cascade
);


create table if not exists UniqueEvents(
	id int not null unique auto_increment,
	EventId int not null,

	year int not null,
	month int not null,
	day int not null,

	primary key(id),
	foreign key (EventId) references Event(id) on delete cascade
);



show tables ;

-- describe UniqueEvents ;

-- describe WeeklyEvents ;

-- describe Event ;

-- describe EventType ;

-- describe DayOfTheWeek ;


-- create the default presets for Types of events

delete from EventType where id > 0 ;
alter table EventType auto_increment = 0 ;
insert into EventType(name,actionDescription) values("alert","gives a personalized voice alert for the system") ;
insert into EventType(name,actionDescription) values("zoom","initiates a zoom meeting") ;
insert into EventType(name,actionDescription) values("alarm","reproduces an alarm") ;

-- create the default presets for the days of the week
delete from DayOfTheWeek where id > 0;
alter table DayOfTheWeek  auto_increment = 0;
insert into DayOfTheWeek(day) values("monday") ;
insert into DayOfTheWeek(day) values("tuesday") ;
insert into DayOfTheWeek(day) values("wednesday") ;
insert into DayOfTheWeek(day) values("thursday") ;
insert into DayOfTheWeek(day) values("friday") ;
insert into DayOfTheWeek(day) values("saturday") ;
insert into DayOfTheWeek(day) values("sunday") ;




-- describe the tables
describe DayOfTheWeek ;
describe EventType ;
describe Event ;
describe WeeklyEvents ;
describe WeeklyEvents_DayOfTheWeek ;
describe UniqueEvents ;






-- visualize data

-- select * from WeeklyEvents ;
-- select * from Event ;
-- select * from EventType ;
-- select * from DayOfTheWeek ;
-- select * from UniqueEvents ;

