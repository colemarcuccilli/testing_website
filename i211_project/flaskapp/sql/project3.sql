-- Disable foreign key checks
SET FOREIGN_KEY_CHECKS = 0;

-- Drop all tables
DROP TABLE IF EXISTS venues, people, events, event_attendees;
-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS event_attendees;


CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    contact_phone VARCHAR(20),
    rental_fee DECIMAL(10, 2),
    max_attendees INT
);

CREATE TABLE people (
    person_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    home_address TEXT NOT NULL,
    email VARCHAR(255),
    date_of_birth DATE,
    mobile_phone VARCHAR(20),
    role ENUM('staff', 'customer') NOT NULL
);

CREATE TABLE events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    event_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    invitation_text TEXT,
    image_path VARCHAR(255),
    max_attendees INT, 
    rental_items TEXT, 
    notes TEXT,
    venue_id INT, 
    planner_id INT, 
    host_id INT,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (planner_id) REFERENCES people(person_id),
    FOREIGN KEY (host_id) REFERENCES people(person_id)
);

CREATE TABLE event_attendees (
    event_id INT,
    person_id INT,
    PRIMARY KEY (event_id, person_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id),
    FOREIGN KEY (person_id) REFERENCES people(person_id)
);

INSERT INTO venues (name, address, contact_phone, rental_fee, max_attendees) VALUES
('Moose Lodge Hall', '123 Elm St', '(123) 456-7890', 500, 200),
('Fountain Square Mall Ballroom', '456 Maple Ave', '(234) 567-8901', 1000, 350),
('Bryan Park Pool', '789 Birch Blvd', '(345) 678-9012', 300, 100),
('Rose Garden Hall', '101 Rose St', '(456) 789-0123', 750, 250),
('City Auditorium', '202 Willow Way', '(567) 890-1234', 1200, 400),
('Sunset Beach Venue', '303 Beachfront Rd', '(678) 901-2345', 200, 75),
('Piere''s Entertainment Center', '5629 St Joe Rd', '(260) 492-6064', 2000, 2000),
('Emerald Palace', '111 Green Ln', '(987) 654-3210', 1100, 300),
('Starlight Theatre', '88 Star St', '(876) 543-2109', 1800, 450),
('Downtown Convention Center', '25 Urban Rd', '(765) 432-1098', 2500, 700),
('Riverfront Pavilion', '333 Riverside Dr', '(654) 321-0987', 850, 275),
('Woodland Retreat', '444 Forest Rd', '(543) 210-9876', 400, 120),
('Skyline Banquet Hall', '555 Skyway St', '(432) 109-8765', 1500, 400),
('Lakeside Manor', '222 Lake Ln', '(321) 098-7654', 950, 280);

INSERT INTO people (name, home_address, email, date_of_birth, mobile_phone, role) VALUES
('John Doe', '789 Pine St', 'johndoe@email.com', '1985-05-10', '(345) 678-9012', 'staff'),
('Jane Smith', '101 Oak Rd', 'janesmith@email.com', '1990-03-15', '(456) 789-0123', 'customer'),
('Liam Turner', '202 Spruce Dr', 'liamturner@email.com', '1987-08-25', '(567) 890-1234', 'staff'),
('Alice Cooper', '303 Maple Lane', 'alicecooper@email.com', '1995-11-20', '(678) 901-2345', 'customer'),
('David Johnson', '404 Birch Blvd', 'davidj@email.com', '1982-01-10', '(789) 012-3456', 'staff'),
('Emily Rose', '505 Cedar Ct', 'emilyrose@email.com', '1988-12-05', '(890) 123-4567', 'customer'),
('Bradyn Kole', '11117 Creekwood Ct', 'countyourblessings@gmail.com', '2004-11-11', '(260) 615-7467', 'staff'),
('Nathan Green', '606 Elm Dr', 'nathangreen@email.com', '1992-09-20', '(123) 456-7890', 'customer'),
('Samantha Paul', '707 Pine Circle', 'samanthap@email.com', '1994-04-15', '(234) 567-8901', 'staff'),
('Michael Scott', '808 Oak Lane', 'mscott@email.com', '1970-03-15', '(345) 678-9012', 'customer'),
('Aria Stark', '909 Maple Dr', 'ariastark@email.com', '1996-12-20', '(456) 789-0123', 'staff'),
('Robert Brown', '10 Elm Rd', 'robertb@email.com', '1984-10-11', '(567) 890-1234', 'customer'),
('Grace Williams', '202 Cedar Ln', 'gracew@email.com', '1986-02-19', '(678) 901-2345', 'staff'),
('Lucas Gray', '111 Fir St', 'lucasgray@email.com', '1998-06-05', '(789) 012-3456', 'customer'),
('Rebecca Long', '222 Pine Ct', 'rebeccal@email.com', '1981-07-30', '(890) 123-4567', 'staff'),
('Peter Wilson', '313 Spruce Ave', 'peterw@email.com', '1978-05-15', '(123) 456-7890', 'customer'),
('Olivia Taylor', '414 Elm Ln', 'oliviat@email.com', '1993-04-10', '(234) 567-8901', 'staff'),
('Daniel Carter', '515 Oak Ct', 'danielc@email.com', '1989-11-15', '(345) 678-9012', 'customer'),
('Sophia Davis', '616 Maple Circle', 'sophiad@email.com', '1991-08-25', '(456) 789-0123', 'staff'),
('Leo Adams', '717 Cedar Dr', 'leoadams@email.com', '1975-10-09', '(567) 890-1234', 'customer'),
('Cole Maruccilli', '11117 Creekwood Ct', 'cole@marcuccilli.com', '2001-11-11', '12606157467', 'staff'),
('Jay', '1233 Dads Ave', 'cybmedia@gmail.com', '1999-12-29', '2604599222', 'customer');


INSERT INTO events (name, event_date, start_time, end_time, invitation_text, image_path, max_attendees, rental_items, notes, venue_id, planner_id) VALUES
('Equinox Gala', '2023-11-05', '18:00', '22:00', 'Join us for a magical evening at the Equinox Gala', 'images/equinox_gala.jpg', 100, 'tent, chairs, tables, PA system', 'Set up starts at 16:00', 1, 001),
('Pat''s Graduation Party', '2023-06-10', '14:00', '19:00', 'Celebrate Pat''s academic achievement with us!', 'images/pats_graduation.jpg', 150, 'chairs, tables, stage', 'Need extra chairs', 2, 002),
('Benny Got a Job', '2023-08-15', '12:00', '16:00', 'Benny''s got a new job! Let''s celebrate!', 'images/benny_job.jpg', 50, 'chairs, tables', 'Pool party, bring swimwear!', 3, 003),
('Granny''s 100th Birthday', '2023-10-10', '10:00', '14:00', 'Celebrate Granny''s century milestone with us!', 'images/granny_birthday.jpg', 200, 'chairs, tables, stage', 'Need a ramp for wheelchair access', 4, 004),
('Summer Fest', '2023-07-20', '19:00', '23:30', 'Join us to welcome summer!', 'images/summer_fest.jpg', 300, 'tent, chairs, PA system', 'Special lighting required!', 5, 005),
('Halloween Bash', '2023-10-31', '20:00', '01:00', 'Spooky night at the pool!', 'images/halloween_bash.jpg', 60, 'chairs, tables, tent', 'Bring your costumes!', 6, 006),
('Dawn of December', '2023-12-01', '7:00', '1:00', 'Indiana''s Biggest Party with Lil Skies', 'images/dawn_of_december.jpg', 2500, 'drinks', 'The best night of your life in Fort Wayne, IN!', 7, 007),
('Nightmare on State St.', '2023-10-31', '8:00', '1:00', 'Chicago''s Biggest Halloween Party', 'images/state_street.jpg', 500, 'drinks', 'The best Halloween ever in chicago', 8, 008);

INSERT INTO event_attendees (event_id, person_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10);
