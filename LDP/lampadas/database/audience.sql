DROP TABLE audience;

CREATE TABLE audience (
	audience		CHAR(12)	NOT NULL,
	audience_level		INT4		NOT NULL,
	audience_description	TEXT,

	PRIMARY KEY (audience)	
);

INSERT INTO audience ( audience, audience_level, audience_description ) VALUES ('NOVICE', 1, 'Novice');
INSERT INTO audience ( audience, audience_level, audience_description ) VALUES ('BEGINNER', 2, 'Beginners');
INSERT INTO audience ( audience, audience_level, audience_description ) VALUES ('INTERMEDIATe', 3, 'Intermediate Users');
INSERT INTO audience ( audience, audience_level, audience_description ) VALUES ('ADVANCED', 4, 'Advanced Users');

GRANT SELECT ON audience TO "www-data";
