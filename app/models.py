from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "Students"

    StudentID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(150), nullable=False)
    Course = Column(String(150), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)

    TotalFee = Column(Numeric(12, 2), nullable=False)
    PaidAmount = Column(Numeric(12, 2), nullable=False)

    DueDate = Column(Date, nullable=False)

    CreatedAt = Column(DateTime, server_default=func.sysutcdatetime())
    UpdatedAt = Column(
        DateTime,
        server_default=func.sysutcdatetime(),
        onupdate=func.sysutcdatetime(),
    )


class Administrator(Base):
    __tablename__ = "Administrators"

    AdminID = Column(Integer, primary_key=True, index=True)
    Name = Column(String(150), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Role = Column(String(50), nullable=False)

    CreatedAt = Column(DateTime, server_default=func.sysutcdatetime())