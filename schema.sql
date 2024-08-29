-- drop tables when running app.py
DROP TABLE IF EXISTS administrators;
DROP TABLE IF EXISTS applicants;
DROP TABLE IF EXISTS schemes;
DROP TABLE IF EXISTS applications;

CREATE TABLE IF NOT EXISTS administrators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    date_of_birth DATE,
    sex TEXT CHECK (sex IN ('Male', 'Female')),
    marital_status TEXT CHECK (
        marital_status IN ('Single', 'Married', 'Widowed', 'Divorced')
    ),
    employment_status TEXT CHECK (
        employment_status IN ('Employed', 'Unemployed')
    ),
    household_json TEXT
);

-- demo applicant 1
INSERT INTO applicants (
    id,
    name,
    email,
    date_of_birth,
    sex,
    marital_status,
    employment_status,
    household_json
) VALUES (
    1,
    'Alice Smith',
    'alice.smith@example.com',
    '1990-05-15',
    'Female',
    'Single',
    'Unemployed',
    '[
        {
            "name": "Alice Smith",
            "email": "alice.smith@example.com",
            "relationship": "Self",
            "employment_status": "Unemployed",
            "marital_status": "Single"
        }
    ]'
);


-- demo applicant 2
INSERT INTO applicants (
    id,
    name,
    email,
    date_of_birth,
    sex,
    marital_status,
    employment_status,
    household_json
) VALUES (
    2,
    'Bob Johnson',
    'bob.johnson@example.com',
    '1985-08-22',
    'Male',
    'Married',
    'Employed',
    '[
        {"name": "Bob Johnson", "email": "bob.johnson@example.com", "relationship": "Self", "marital_status": "Married", "employment_status": "Employed"},
        {"name": "Carol Johnson", "email": "carol.johnson@example.com", "relationship": "Spouse", "marital_status": "Married", "employment_status": "Employed"},
        {"name": "Child 1", "email": "child1@example.com", "relationship": "Child", "marital_status": "Single", "employment_status": "Unemployed"},
        {"name": "Child 2", "email": "child2@example.com", "relationship": "Child", "marital_status": "Single", "employment_status": "Unemployed"}
    ]'
);


CREATE TABLE IF NOT EXISTS schemes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    criteria_jq TEXT,
    benefits TEXT
);

-- demo scheme 1
INSERT INTO schemes (name, description, criteria_jq, benefits)
VALUES (
    'Unemployed and Single Scheme',
    'A scheme for applicants who are unemployed and single, with self in the household.',
    '[ .[] | select(.relationship == "Self" and .employment_status == "Unemployed" and .marital_status == "Single") ] | length > 0',
    'Benefits include financial assistance and job placement services.'
);

-- demo scheme 2
INSERT INTO schemes (name, description, criteria_jq, benefits)
VALUES (
    'Employed with More Than 1 Child Scheme',
    'A scheme for employed applicants with more than one child in the household.',
    '(.[] | select(.relationship == "Self").employment_status == "Employed") and ((.[] | select(.relationship == "Child")) | length > 1)',
    'Benefits include educational support and childcare subsidies.'
);


CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    applicant_id INTEGER NOT NULL,
    scheme_id INTEGER NOT NULL,
    outcome TEXT CHECK(outcome IN ('Pending', 'Approved', 'Denied')) DEFAULT 'Pending',
    FOREIGN KEY (applicant_id) REFERENCES applicants (id),
    FOREIGN KEY (scheme_id) REFERENCES schemes (id)
);
