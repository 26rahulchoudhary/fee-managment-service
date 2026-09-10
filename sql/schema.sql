IF OBJECT_ID('dbo.Students', 'U') IS NOT NULL
    DROP TABLE dbo.Students;

IF OBJECT_ID('dbo.Administrators', 'U') IS NOT NULL
    DROP TABLE dbo.Administrators;


CREATE TABLE dbo.Students
(
    StudentID INT IDENTITY(1,1) NOT NULL,
    Name NVARCHAR(150) NOT NULL,
    Course NVARCHAR(150) NOT NULL,
    Email NVARCHAR(255) NOT NULL,
    TotalFee DECIMAL(12,2) NOT NULL,
    PaidAmount DECIMAL(12,2) NOT NULL DEFAULT 0,
    DueDate DATE NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    UpdatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_Students
        PRIMARY KEY (StudentID),

    CONSTRAINT UQ_Students_Email
        UNIQUE (Email),

    CONSTRAINT CK_Students_TotalFee
        CHECK (TotalFee >= 0),

    CONSTRAINT CK_Students_PaidAmount
        CHECK (PaidAmount >= 0),

    CONSTRAINT CK_Students_PaidAmount_TotalFee
        CHECK (PaidAmount <= TotalFee)
);


CREATE TABLE dbo.Administrators
(
    AdminID INT IDENTITY(1,1) NOT NULL,
    Name NVARCHAR(150) NOT NULL,
    Email NVARCHAR(255) NOT NULL,
    Role NVARCHAR(50) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT PK_Administrators
        PRIMARY KEY (AdminID),

    CONSTRAINT UQ_Administrators_Email
        UNIQUE (Email),

    CONSTRAINT CK_Administrators_Role
        CHECK (Role IN ('Admin', 'FinanceAdmin', 'SuperAdmin'))
);



CREATE INDEX IX_Students_DueDate
ON dbo.Students (DueDate);

CREATE INDEX IX_Students_PaymentLookup
ON dbo.Students (PaidAmount, TotalFee);

CREATE INDEX IX_Administrators_Role
ON dbo.Administrators (Role);