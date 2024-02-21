-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products ADD CONSTRAINT chk_unit_price CHECK (unit_price > 0);
-- проверить, что ограничение было добавлено (результат запроса должен быть пустым)
SELECT *
FROM products
WHERE unit_price <= 0;

-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products ADD CONSTRAINT chk_discontinued CHECK (discontinued IN(0, 1));
-- проверить, что ограничение было добавлено (результат запроса должен быть пустым)
SELECT *
FROM products
WHERE discontinued NOT IN (0, 1);

-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
SELECT *
INTO discontinued_products
FROM products
WHERE discontinued = 1;
-- проверка зполнения
SELECT * FROM discontinued_products

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.

--1. - Удаляем связь для снятия ограничения
ALTER TABLE order_details DROP CONSTRAINT fk_order_details_products;
--2. - Удаляем данные из таблицы products
DELETE FROM products
WHERE discontinued = 1;
--3. - Удаляем данные из таблицы order_details
DELETE FROM order_details
WHERE discount = 1;
--4. - Восстанавливаем связь между таблицами (имя связи можно посмотреть в свойствах таблицы)
ALTER TABLE order_details
ADD CONSTRAINT fk_order_details_products
FOREIGN KEY (product_id)
REFERENCES products(product_id);
-- проверить данные таблицы:
SELECT * FROM products