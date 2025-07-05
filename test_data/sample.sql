-- Sample SQL data with phone numbers
INSERT INTO users (username, phone_number, notes) VALUES ('john_doe', '+1-555-555-5555', 'Main number');
INSERT INTO users (username, phone_number, notes) VALUES ('jane_smith', '(555) 123-4567', 'Work phone');
INSERT INTO users (username, phone_number, notes) VALUES ('test_user', '1234567', 'Short number, should be valid');
INSERT INTO users (username, phone_number, notes) VALUES ('no_phone_user', NULL, 'No phone on file');
INSERT INTO users (username, phone_number, notes) VALUES ('invalid_phone', '555-1234', 'Too short');
INSERT INTO users (username, phone_number, notes) VALUES ('uk_user', '+442079460999', 'UK contact');
-- Some comments with numbers
-- Meeting at 10:00 AM, call +15555555555 if late.
-- Old record: 5551234567 (deactivated)
INSERT INTO users (username, phone_number, notes) VALUES ('de_user', '+4912345678903', 'German contact');
