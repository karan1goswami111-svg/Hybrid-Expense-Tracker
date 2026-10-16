-- Switch to our newly created ExpenseDB database container
USE ExpenseDB;
GO

-- Procedure 1: To calculate monthly aggregates and map dynamic budget warnings
CREATE OR ALTER PROCEDURE GetUserMonthlyStatus
    @UID INT,
    @Month INT,
    @Year INT
AS
BEGIN
    SET NOCOUNT ON;
    
    SELECT 
        u.UserName,
        u.MonthlyBudget,
        ISNULL(SUM(e.Amount), 0) AS TotalSpent
    FROM ProjectUsers u
    LEFT JOIN GroupExpenses e ON u.UserID = e.UserID 
        AND MONTH(e.ExpenseDate) = @Month 
        AND YEAR(e.ExpenseDate) = @Year
    WHERE u.UserID = @UID
    GROUP BY u.UserName, u.MonthlyBudget;
END;
GO

-- Procedure 2: To pull clustered timeline metrics for our timeline analytical bar chart
CREATE OR ALTER PROCEDURE GetUserHistory
    @UID INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT 
        MONTH(ExpenseDate) AS ExpenseMonth,
        YEAR(ExpenseDate) AS ExpenseYear,
        SUM(Amount) AS TotalAmount
    FROM GroupExpenses
    WHERE UserID = @UID
    GROUP BY YEAR(ExpenseDate), MONTH(ExpenseDate)
    ORDER BY ExpenseYear ASC, ExpenseMonth ASC;
END;
GO
