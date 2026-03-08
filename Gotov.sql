-- =====================================
-- СОЗДАНИЕ БАЗЫ ДАННЫХ
-- =====================================

DROP DATABASE IF EXISTS furniture_factory;
CREATE DATABASE furniture_factory;
USE furniture_factory;


-- =====================================
-- ТИПЫ МАТЕРИАЛОВ
-- =====================================

CREATE TABLE material_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    loss_percent DECIMAL(10,5)
);

INSERT INTO material_types (name, loss_percent) VALUES
('Дерево', 0.0055),
('Древесная плита', 0.0030),
('Текстиль', 0.0015),
('Стекло', 0.0045),
('Металл', 0.0010);


-- =====================================
-- МАТЕРИАЛЫ
-- =====================================

CREATE TABLE materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type_id INT,
    quantity_in_pack DECIMAL(10,2),
    unit VARCHAR(50),
    description TEXT,
    image VARCHAR(255),
    price DECIMAL(10,2),
    stock_quantity DECIMAL(10,2),
    min_quantity DECIMAL(10,2),

    FOREIGN KEY (type_id) REFERENCES material_types(id)
);

INSERT INTO materials (name, type_id, quantity_in_pack, unit, price, stock_quantity, min_quantity) VALUES
('Цельный массив дерева Дуб 1000х600 мм', 1, 1.00, 'м2', 3500.00, 50, 10),
('Клееный массив дерева Дуб 1000х600 мм', 1, 1.00, 'м2', 3200.00, 40, 10),
('Шпон облицовочный Дуб натуральный 2750х480 мм', 1, 1.00, 'м2', 1800.00, 60, 15),
('Фанера 2200х1000 мм', 2, 1.00, 'м2', 900.00, 70, 20),
('ДСП 2750х1830 мм', 2, 1.00, 'м2', 750.00, 80, 25),
('Ткань мебельная', 3, 1.00, 'м', 500.00, 100, 30),
('Стекло закаленное', 4, 1.00, 'м2', 1200.00, 30, 10),
('Металлическая труба', 5, 1.00, 'м', 600.00, 90, 20);


-- =====================================
-- ТИПЫ ПРОДУКЦИИ
-- =====================================

CREATE TABLE product_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    coefficient DECIMAL(10,2)
);

INSERT INTO product_types (name, coefficient) VALUES
('Кресла', 1.95),
('Полки', 2.50),
('Стеллажи', 4.35),
('Столы', 5.50),
('Тумбы', 7.60);


-- =====================================
-- ПРОДУКЦИЯ
-- =====================================

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    article VARCHAR(50),
    name VARCHAR(255),
    product_type_id INT,
    min_partner_price DECIMAL(10,2),

    FOREIGN KEY (product_type_id) REFERENCES product_types(id)
);

INSERT INTO products (article, name, product_type_id, min_partner_price) VALUES
('KR001', 'Кресло офисное мягкое', 1, 15324.99),
('KR002', 'Кресло офисное премиум', 1, 21443.99),
('KR003', 'Кресло офисное люкс', 1, 24760.00),
('PL001', 'Полка настенная', 2, 2670.89),
('ST001', 'Стеллаж офисный', 3, 12000.00),
('TB001', 'Тумба офисная', 5, 8000.00),
('STL001', 'Стол офисный', 4, 14000.00);


-- =====================================
-- СВЯЗЬ ПРОДУКЦИИ И МАТЕРИАЛОВ
-- =====================================

CREATE TABLE product_materials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    material_id INT,
    quantity DECIMAL(10,2),

    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (material_id) REFERENCES materials(id)
);

INSERT INTO product_materials (product_id, material_id, quantity) VALUES
(1, 4, 0.85),
(1, 6, 1.50),
(1, 8, 1.00),

(2, 4, 1.20),
(2, 6, 2.00),
(2, 8, 1.30),

(3, 1, 1.50),
(3, 6, 2.50),

(4, 5, 0.80),

(5, 5, 2.00),
(5, 8, 1.50),

(6, 5, 1.20),
(6, 8, 0.80),

(7, 1, 2.00),
(7, 8, 1.00);


-- =====================================
-- ПРОСМОТР СПИСКА МАТЕРИАЛОВ
-- =====================================

SELECT 
m.id,
m.name AS material_name,
mt.name AS material_type,
m.stock_quantity,
m.min_quantity
FROM materials m
JOIN material_types mt ON mt.id = m.type_id;


-- =====================================
-- РАСЧЕТ ТРЕБУЕМОГО КОЛИЧЕСТВА МАТЕРИАЛА
-- =====================================

SELECT 
m.name,
SUM(pm.quantity) AS required_quantity
FROM materials m
JOIN product_materials pm 
ON pm.material_id = m.id
GROUP BY m.name;