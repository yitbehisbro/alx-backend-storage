-- Creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE average_score DECIMAL(10,2);
    SELECT AVG(score) INTO average_score FROM corrections WHERE user_id = user_id;
    UPDATE users SET average_score = average_score WHERE id = user_id;
END//
DELIMITER ;
