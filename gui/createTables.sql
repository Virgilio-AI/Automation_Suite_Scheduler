-- create a the main database if it doesn't exists 
create database if not exists automation_suite ;
-- use the data base where the tables will be created

use automation_suite ;

-- day of the week will be related to WeeklyEvents in many to many
create table if not exists DayOfTheWeek(
	id int not null unique auto_increment,

	day varchar(50),

	primary key(id)
);
-- EventType will be related to table Event in one to many
create table if not exists EventType(
	id int not null unique auto_increment,
	name varchar(100),
	actionDescription varchar(300),
	primary key(id)
);
-- Event will be related to Weekly Events and UniqueEvents in one to many
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
-- Weekly Events wil be related to Event in a relationship of one to one
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
-- this is the helper table to relate WeeklyEvents and DayOfTheWeek in a many to many way
create table if not exists WeeklyEvents_DayOfTheWeek(
	id int not null unique auto_increment,

	WeeklyEventsId int not null,
	DayOfTheWeekId int not null,

	primary key(id),
	foreign key (WeeklyEventsId) references WeeklyEvents(id) on delete cascade,
	foreign key (DayOfTheWeekId) references DayOfTheWeek(id) on delete cascade
);
-- Unique events will be related in a one to many relationship with the event table
create table if not exists UniqueEvents(
	id int not null unique auto_increment,
	EventId int not null,

	year int not null,
	month int not null,
	day int not null,

	primary key(id),
	foreign key (EventId) references Event(id) on delete cascade
);

-- create the default presets for Types of events
-- this are the three default but will be adding more in the future

delete from EventType where id > 0 ;
alter table EventType auto_increment = 0 ;
insert into EventType(name,actionDescription) values("alert","gives a personalized voice alert for the system") ;
insert into EventType(name,actionDescription) values("zoom","initiates a zoom meeting") ;
insert into EventType(name,actionDescription) values("alarm","reproduces an alarm") ;

-- create the default presets for the days of the week
-- this are just the days of the week
delete from DayOfTheWeek where id > 0;
alter table DayOfTheWeek  auto_increment = 0;
insert into DayOfTheWeek(day) values("monday") ;
insert into DayOfTheWeek(day) values("tuesday") ;
insert into DayOfTheWeek(day) values("wednesday") ;
insert into DayOfTheWeek(day) values("thursday") ;
insert into DayOfTheWeek(day) values("friday") ;
insert into DayOfTheWeek(day) values("saturday") ;
insert into DayOfTheWeek(day) values("sunday") ;

