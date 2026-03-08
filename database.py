import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12543hRGB2001",
        database="furniture_factory"
    )

    return connection


def get_materials():

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT 
    m.id,
    m.name,
    mt.name,
    m.stock_quantity,
    m.min_quantity
    FROM materials m
    JOIN material_types mt
    ON mt.id = m.type_id
    """

    cursor.execute(query)

    materials = cursor.fetchall()

    connection.close()

    return materials


def add_material(name, type_id, stock, minimum):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO materials
    (name,type_id,stock_quantity,min_quantity)
    VALUES (%s,%s,%s,%s)
    """

    cursor.execute(query, (name, type_id, stock, minimum))

    connection.commit()
    connection.close()


def update_material(material_id, name, type_id, stock, minimum):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    UPDATE materials
    SET name=%s,
    type_id=%s,
    stock_quantity=%s,
    min_quantity=%s
    WHERE id=%s
    """

    cursor.execute(query, (name, type_id, stock, minimum, material_id))

    connection.commit()
    connection.close()


def get_material_types():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id,name FROM material_types")

    types = cursor.fetchall()

    connection.close()

    return types


def get_products_by_material(material_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT p.name
    FROM products p
    JOIN product_materials pm
    ON p.id = pm.product_id
    WHERE pm.material_id = %s
    """

    cursor.execute(query, (material_id,))

    products = cursor.fetchall()

    connection.close()

    return products


def get_required_quantity(material_id):

    connection = get_connection()
    cursor = connection.cursor()

    query = """
    SELECT SUM(quantity)
    FROM product_materials
    WHERE material_id=%s
    """

    cursor.execute(query, (material_id,))

    result = cursor.fetchone()

    connection.close()

    if result[0] is None:
        return 0

    return round(result[0], 2)