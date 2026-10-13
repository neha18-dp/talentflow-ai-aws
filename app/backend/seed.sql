USE talentflow;

INSERT INTO candidates
    (id, name, email, position, experience, score, stage, applied_date)
VALUES
    (1, 'Aarav Mehta', 'aarav@example.com', 'Frontend Developer', '3 years', 94, 'Interview', '2026-09-25'),
    (2, 'Priya Shah', 'priya@example.com', 'Python Developer', '2 years', 91, 'Screening', '2026-09-24'),
    (3, 'Rohan Patil', 'rohan@example.com', 'DevOps Engineer', '4 years', 88, 'Shortlisted', '2026-09-23'),
    (4, 'Sneha Kulkarni', 'sneha@example.com', 'Data Analyst', '2 years', 86, 'Applied', '2026-09-22'),
    (5, 'Vikram Joshi', 'vikram@example.com', 'Backend Developer', '5 years', 82, 'Offer', '2026-09-20'),
    (6, 'Neha Test', 'neha.test@example.com', 'Cloud Engineer', '2 years', 85, 'Screening', '2026-10-12');

INSERT INTO jobs
    (id, title, department, location, type)
VALUES
    (1, 'Frontend Developer', 'Engineering', 'Mumbai / Hybrid', 'Full-time'),
    (2, 'Python Developer', 'Engineering', 'Remote', 'Full-time'),
    (3, 'Data Analyst', 'Analytics', 'Pune / Hybrid', 'Full-time'),
    (4, 'Cloud Engineer', 'Engineering', 'Mumbai, Maharashtra', 'Full-time');

INSERT INTO interviews
    (id, candidate_id, interview_date, interview_time, interviewer)
VALUES
    (1, 1, '2026-09-28', '10:30:00', 'Neha Sharma'),
    (2, 3, '2026-09-29', '14:00:00', 'Rahul Verma'),
    (3, 2, '2026-09-30', '11:00:00', 'Anita Rao'),
    (4, 6, '2026-10-15', '11:00:00', 'Ananya Deshmukh');