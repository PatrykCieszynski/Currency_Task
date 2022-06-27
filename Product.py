class Product:
    def __init__(self, productid, departmentid, category, idsku, productname, quantity, unitprice, unitpriceusd,
                 unitpriceeuro, ranking, productdesc, unitsinstock, unitsinorder):
        self.product_ID = productid
        self.department_ID = departmentid
        self.category = category
        self.IDSKU = idsku
        self.product_name = productname
        self.quantity = quantity
        self.unit_price = unitprice
        self.unit_price_USD = unitpriceusd
        self.unit_price_EUR = unitpriceeuro
        self.ranking = ranking
        self.product_desc = productdesc
        self.units_in_stock = unitsinstock
        self.units_in_order = unitsinorder
