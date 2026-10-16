-- 1. Switch to master database first to perform database creation operations safely
USE master;
GO

-- 2. Drop the database if it already exists to get a clean slate
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'ExpenseDB')
BEGIN
    ALTER DATABASE ExpenseDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE ExpenseDB;
END
GO

-- 3. Create the fresh database container with your chosen name
CREATE DATABASE ExpenseDB;
GO

-- 4. Switch to our new ExpenseDB database container
USE ExpenseDB;
GO

-- 5. Create Users table to store profile name and strict monthly limits
CREATE TABLE ProjectUsers (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    UserName VARCHAR(100) NOT NULL,
    MonthlyBudget DECIMAL(10,2) NOT NULL
);

-- 6. Create Expenses table to track individual transactions mapped via foreign key
CREATE TABLE GroupExpenses (
    ExpenseID INT IDENTITY(1,1) PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES ProjectUsers(UserID),
    Category VARCHAR(50) NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    ExpenseDate DATE NOT NULL
);

-- 7. Insert standard test data profiles
INSERT INTO ProjectUsers (UserName, MonthlyBudget) VALUES 
('Ketan (Personal)', 8000.00), 
('Rahul (Roommate)', 4000.00), 
('Amit (Roommate)', 4000.00);

-- 8. Insert 6-month transaction records to populate our visual analytics interface
INSERT INTO GroupExpenses (UserID, Category, Amount, ExpenseDate) VALUES 
(1, 'Books', 3000.00, '2026-02-15'),      -- Feb record
(1, 'Food', 4500.00, '2026-03-10'),       -- Mar record
(1, 'Rent', 4000.00, '2026-04-05'),       -- Apr record
(1, 'Travel', 9500.00, '2026-05-20'),     -- May record (Simulating budget violation case)
(1, 'Food', 3500.00, '2026-06-12'),       -- June record
(1, 'Groceries', 5000.00, '2026-07-02'),  -- July record

(2, 'Room Rent', 2000.00, '2026-07-01'),  -- Roommate record
(3, 'Mess Food', 2500.00, '2026-07-02'),  -- Roommate record
(2, 'Internet', 600.00, '2026-07-05');    -- Roommate record
GO
