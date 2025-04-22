CREATE TABLE Rooms (
    RoomID INT PRIMARY KEY,
    RoomType VARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Status VARCHAR(20) NOT NULL,
    Floor INT,
    Orientation VARCHAR(20)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name VARCHAR(30) NOT NULL,
    Phone VARCHAR(50) NOT NULL,
    Email VARCHAR(50),
    Address VARCHAR(200),
    IDNumber VARCHAR(20) UNIQUE
);

CREATE TABLE Services (
    ServiceID INT PRIMARY KEY,
    ServiceType VARCHAR(50) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    ServiceTime DATE
);

CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    RoomID INT NOT NULL,
    ReservationDate DATE NOT NULL,
    CheckInDate DATE NOT NULL,
    CheckOutDate DATE NOT NULL,
    Status VARCHAR(20) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID)
);

CREATE TABLE Members (
    MemberID INT PRIMARY KEY,
    CustomerID INT NOT NULL UNIQUE,
    MembershipLevel VARCHAR(20) NOT NULL,
    Points INT DEFAULT 0,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Transactions (
    TransactionID INT PRIMARY KEY,
    CustomerID INT NOT NULL,
    RoomID INT NULL,
    ServiceID INT NULL,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentMethod VARCHAR(20) NOT NULL,
    TransactionDate DATETIME NOT NULL,
    Deposit DECIMAL(10, 2) DEFAULT 0.00,
    Refund DECIMAL(10, 2) DEFAULT 0.00,
    Tax DECIMAL(10, 2) DEFAULT 0.00,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
);