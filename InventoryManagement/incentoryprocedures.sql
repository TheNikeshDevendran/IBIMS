create procedure CheckUser(
@email varchar(50),
@password varchar(5)
)
AS
BEGIN
select * from users where email=@email and password=@password
END
-----------------------------

create procedure AddProduct(
@ProductName varchar(50),
@quantity int,
@Price decimal,
@Active varchar(50)
)
AS
BEGIN
INSERT INTO Products (ProductName, Quantity, Price,Active) 
VALUES (@ProductName,@quantity ,@Price,@Active) 
END

--------------------------------------------

create procedure FetchActiveProduct
AS
BEGIN
select * from products where Active='active'
END

-------------------------------------
create Procedure GetProductByName(
@name varchar(50)
)
AS
BEGIN
select * from products where ProductName=@name
END

GetProductByName 'Milk'
select * from Products

