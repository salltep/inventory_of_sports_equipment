PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS Damage;
DROP TABLE IF EXISTS Operation;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Role;

CREATE TABLE Role (
    RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
    name   TEXT NOT NULL UNIQUE
);

CREATE TABLE User (
    UserID       INTEGER PRIMARY KEY AUTOINCREMENT,
    login        TEXT NOT NULL UNIQUE,
    passwordHash TEXT NOT NULL,
    RoleID       INTEGER NOT NULL,
    FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);

CREATE TABLE Inventory (
    InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    type        TEXT NOT NULL,
    status      TEXT NOT NULL DEFAULT 'исправен',
    quantity    INTEGER NOT NULL DEFAULT 1 CHECK (quantity >= 0)
);

CREATE TABLE Operation (
    OperationID INTEGER PRIMARY KEY AUTOINCREMENT,
    InventoryID INTEGER NOT NULL,
    UserID      INTEGER NOT NULL,
    type        TEXT NOT NULL CHECK (type IN ('issue', 'return', 'repair', 'writeoff', 'check')),
    date        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    comment     TEXT,
    FOREIGN KEY (InventoryID) REFERENCES Inventory(InventoryID),
    FOREIGN KEY (UserID)      REFERENCES User(UserID)
);

CREATE TABLE Damage (
    DamageID    INTEGER PRIMARY KEY AUTOINCREMENT,
    InventoryID INTEGER NOT NULL,
    description TEXT NOT NULL,
    date        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (InventoryID) REFERENCES Inventory(InventoryID)
);


INSERT INTO Role (name) VALUES
    ('Тренер'),
    ('Управляющий');

INSERT INTO User (login, passwordHash, RoleID) VALUES
    ('ivanov',  '6f86ded7f21c4fa38e743da647865b1fba355b6535758132285772e8d2fde2fc', 1),
    ('petrova', 'e30f8d2095a74f90a374186a7b8106bbe59b67b38f5ebcc937c312e70506c670', 1),
    ('sidorov', '307cd1d8dc74449d092c4d7683a525ecd93f867181ed0013e3ff213306c5eca1', 2);

INSERT INTO Inventory (name, type, status, quantity) VALUES
    ('Футбольный мяч',     'Мячи',             'исправен',  10),
    ('Баскетбольный мяч',  'Мячи',             'исправен',  8),
    ('Гантели 5 кг',       'Силовой инвентарь','исправен',  12),
    ('Скакалка',           'Гимнастика',       'в ремонте', 2),
    ('Волейбольная сетка', 'Сетки',            'списан',    1);

INSERT INTO Operation (InventoryID, UserID, type, date, comment) VALUES
    (1, 1, 'issue',    '2026-10-10 09:00:00', 'Выдано 5 мячей на тренировку'),
    (1, 1, 'return',   '2026-10-10 11:00:00', 'Возвращено 5 мячей'),
    (4, 3, 'repair',   '2026-10-12 14:30:00', 'Отправлена на ремонт после поломки'),
    (5, 3, 'writeoff', '2026-10-13 10:00:00', 'Сетка порвана, ремонту не подлежит'),
    (3, 3, 'check',    '2026-10-14 16:00:00', 'Плановая проверка, всё в порядке');

INSERT INTO Damage (InventoryID, description, date) VALUES
    (4, 'Порвалась ручка у скакалки', '2026-10-11 15:20:00'),
    (5, 'Порван край сетки',          '2026-10-12 12:00:00');
