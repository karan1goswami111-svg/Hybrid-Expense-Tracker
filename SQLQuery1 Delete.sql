USE ExpenseDB;
GO

-- Purani foreign key constraint ko drop karenge
ALTER TABLE GroupExpenses DROP CONSTRAINT IF EXISTS FK__GroupExpe__UserI__3B75D760;

-- Nayi foreign key lagayenge ON DELETE CASCADE ke sath (Isse user delete hote hi uske expenses automatic delete ho jayenge)
ALTER TABLE GroupExpenses 
ADD CONSTRAINT FK_GroupExpenses_ProjectUsers 
FOREIGN KEY (UserID) REFERENCES ProjectUsers(UserID) 
ON DELETE CASCADE;
GO
