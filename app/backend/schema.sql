CREATE DATABASE IF NOT EXISTS talentflow;

USE talentflow;

CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    position VARCHAR(150) NOT NULL,
    experience VARCHAR(100),
    score INT DEFAULT 0,
    stage VARCHAR(50) DEFAULT 'Applied',
    applied_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    department VARCHAR(100),
    location VARCHAR(150),
    type VARCHAR(50) DEFAULT 'Full-time',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    interview_date DATE NOT NULL,
    interview_time TIME NOT NULL,
    interviewer VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_interview_candidate
        FOREIGN KEY (candidate_id)
        REFERENCES candidates(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_candidates_stage
    ON candidates(stage);

CREATE INDEX idx_candidates_position
    ON candidates(position);

CREATE INDEX idx_interviews_candidate
    ON interviews(candidate_id);