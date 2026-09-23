from flask import Flask
from db.conn import open_connection 
from db.utils import get_df, execute_query
import pandas as pd
from utils import write_log


app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <p>Video Game Store and entertainment articles</p>
    </body>
    </html>
    """

@app.route("/reports", methods=["GET"])
def reports_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Reports</h2>
        <p>General reports Game Store. </p>
    </body>
    </html>
    """

@app.route("/reports/sales", methods=["GET"])
def sales_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Sales Reports</h2>
        <p>Reports for sales</p>
    </body>
    </html>
    """

@app.route("/reports/sales/<fecha>", methods=["GET"])
def sales_month_page(fecha):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Sales Reports</h2>
        <p>Reports for sales: {fecha} </p>
    </body>
    </html>
    """

@app.route("/reports/sales/hist", methods=["GET"])
def sales_hist_page():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Game Store</title>
    </head>
    <body>
        <h1>Game Store</h1>
        <h2>Sales Reports</h2>
        <p>Reports for sales Historia </p>
        <table border="1" id="salesTable">
            <thead>
                <tr>
                    <th>Month Example</th>
                    <th>Import Example</th>
                </tr>
            </thead>
            <tbody id="salesTableBody">
                <tr>
                    <th>2026-05</th>
                    <th>10,000</th>
                </tr>
                <tr>
                    <th>2026-04</th>
                    <th>12,000</th>
                </tr>
            </tbody>
        </table>

    </body>
    </html>
    """

@app.route("/api/reports/sales/hist", methods=["GET"])
def sales_rp_hist():
    conn = open_connection()

    query = """SELECT 
	    LAST_DAY(purchase_date) as month,
        SUM(import) as import
    FROM game_store.sales
    GROUP BY LAST_DAY(purchase_date);"""

    # datetime to format data: YYYY-MM-DD. Example 2026-03-02
    df_rp_hist = get_df(conn, query)
    df_rp_hist["month"]= pd.to_datetime(df_rp_hist["month"]).dt.strftime("%Y-%m-%d")

    return df_rp_hist.values.tolist()
from flask import jsonify
import pandas as pd
import os
import logging
from datetime import datetime


@app.route("/api/reports/product/hist", methods=["GET"])
def sales_rp_hist():
    conn = None

    try:
        conn = open_connection()
    except Exception as e:
        write_log(
            "Error al establecer la conexión con la base de datos.",
            e
        )

        return jsonify({
            "status": "error",
            "message": "No fue posible establecer conexión con la base de datos."
        }), 500

    # ============================================================
    # 1. CREAR TABLA PRV_PRODUCT_REPORT
    # ============================================================

    create_prv_table = """
        CREATE TABLE IF NOT EXISTS prv_product_report (
            DATE DATE,
            prod_name VARCHAR(100),
            TOT_PROD_SL BIGINT,
            TOT_CLIE_SL DECIMAL(10,2),
            MONEY DECIMAL(32,2)
        );
    """

    try:
        execute_query(conn, create_prv_table)

    except Exception as e:
        write_log(
            "Error al crear la tabla prv_product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible crear la tabla temporal del reporte."
        }), 500

    # ============================================================
    # 2. TRUNCATE TABLA PRV_PRODUCT_REPORT
    # ============================================================

    truncate_prv_table = """
        TRUNCATE TABLE prv_product_report 
    """

    try:
        execute_query(conn, truncate_prv_table)

    except Exception as e:
        write_log(
            "Error al truncar la tabla prv_product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible truncar la tabla temporal del reporte."
        }), 500

    # ============================================================
    # 3. INSERTAR DATOS EN PRV_PRODUCT_REPORT
    # ============================================================

    insert_prv_table = """
        INSERT INTO prv_product_report
        (
            DATE,
            prod_name,
            TOT_PROD_SL,
            TOT_CLIE_SL,
            MONEY
        )
        WITH SALES AS (
            SELECT 
                LAST_DAY(PURCHASE_DATE) AS DATE,
                PROD_ID,
                COUNT(*) AS TOT_PROD_SL,
                COUNT(DISTINCT id_client) AS TOT_CLIE_SL,
                SUM(import) AS MONEY
            FROM game_store.sales
            GROUP BY LAST_DAY(PURCHASE_DATE), PROD_ID
        ),
        ARTICLES AS (
            SELECT
                prod_id,
                prod_name
            FROM game_store.products
        )
        SELECT 
            a.DATE,
            b.prod_name,
            a.TOT_PROD_SL,
            a.TOT_CLIE_SL,
            a.MONEY
        FROM SALES a
        LEFT JOIN ARTICLES b
            ON a.prod_id = b.prod_id
        ORDER BY a.DATE, b.prod_name;
    """

    try:
        execute_query(conn, insert_prv_table)

    except Exception as e:
        write_log(
            "Error al insertar datos en prv_product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible generar los datos temporales del reporte."
        }), 500


    # ============================================================
    # 4. OBTENER DATOS DE PRV_PRODUCT_REPORT
    # ============================================================

    query_prv_data = """
        SELECT *
        FROM prv_product_report;
    """

    try:
        prv_data = get_df(conn, query_prv_data)

    except Exception as e:
        write_log(
            "Error al obtener los datos de prv_product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible obtener los datos temporales del reporte."
        }), 500


    # ============================================================
    # 5. VALIDAR DATOS DE PRV_PRODUCT_REPORT
    # ============================================================

    try:

        required_columns = [
            "date",
            "prod_name",
            "tot_prod_sl",
            "tot_clie_sl",
            "money"
        ]

        # Validar que existan las columnas
        missing_columns = [
            column
            for column in required_columns
            if column not in prv_data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Faltan columnas requeridas: {missing_columns}"
            )

        # Validar datos nulos
        if prv_data[required_columns].isnull().any().any():

            null_columns = (
                prv_data[required_columns]
                .columns[
                    prv_data[required_columns]
                    .isnull()
                    .any()
                ]
                .tolist()
            )

            raise ValueError(
                f"Se encontraron valores nulos en: {null_columns}"
            )

        # Validar valores negativos
        numeric_columns = [
            "tot_prod_sl",
            "tot_clie_sl",
            "money"
        ]

        negative_data = (
            prv_data[numeric_columns] < 0
        ).any()

        negative_columns = (
            negative_data[
                negative_data
            ]
            .index
            .tolist()
        )

        if negative_columns:
            raise ValueError(
                f"Se encontraron valores negativos en: "
                f"{negative_columns}"
            )

        # Validar y normalizar fecha
        prv_data["date"] = pd.to_datetime(
            prv_data["date"],
            errors="raise"
        ).dt.strftime("%Y-%m-%d")

    except Exception as e:

        write_log(
            "Error en la validación de los datos de prv_product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "Los datos temporales del reporte no son válidos."
        }), 422


    # ============================================================
    # 6. CREAR TABLA PRODUCT_REPORT
    # ============================================================

    create_prod_table = """
        CREATE TABLE IF NOT EXISTS product_report (
            DATE DATE,
            prod_name VARCHAR(100),
            TOT_PROD_SL BIGINT,
            TOT_CLIE_SL DECIMAL(10,2),
            MONEY DECIMAL(32,2)
        );
    """

    try:
        execute_query(conn, create_prod_table)

    except Exception as e:
        write_log(
            "Error al crear la tabla product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible crear la tabla final del reporte."
        }), 500


    # ============================================================
    # 7. INSERTAR DATOS EN PRODUCT_REPORT
    # ============================================================

    insert_prod_table = """
        INSERT INTO product_report
        (
            DATE,
            prod_name,
            TOT_PROD_SL,
            TOT_CLIE_SL,
            MONEY
        )
        WITH SALES AS (
            SELECT 
                LAST_DAY(PURCHASE_DATE) AS DATE,
                PROD_ID,
                COUNT(*) AS TOT_PROD_SL,
                COUNT(DISTINCT id_client) AS TOT_CLIE_SL,
                SUM(import) AS MONEY
            FROM game_store.sales
            GROUP BY LAST_DAY(PURCHASE_DATE), PROD_ID
        ),
        ARTICLES AS (
            SELECT
                prod_id,
                prod_name
            FROM game_store.products
        )
        SELECT 
            a.DATE,
            b.prod_name,
            a.TOT_PROD_SL,
            a.TOT_CLIE_SL,
            a.MONEY
        FROM SALES a
        LEFT JOIN ARTICLES b
            ON a.prod_id = b.prod_id
        ORDER BY a.DATE, b.prod_name;
    """

    try:
        execute_query(conn, insert_prod_table)

    except Exception as e:
        write_log(
            "Error al insertar datos en product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible generar los datos finales del reporte."
        }), 500

    # ============================================================
    # 2. TRUNCATE TABLA PRODUCT_REPORT
    # ============================================================

    truncate_prv_table = """
        TRUNCATE TABLE product_report 
    """

    try:
        execute_query(conn, truncate_prod_table)

    except Exception as e:
        write_log(
            "Error al truncar la tabla prod_product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible truncar la tabla productiva del reporte."
        }), 500



    # ============================================================
    # 9. OBTENER DATOS DE PRODUCT_REPORT
    # ============================================================

    query_prod_data = """
        SELECT *
        FROM product_report;
    """

    try:
        prod_data = get_df(conn, query_prod_data)

    except Exception as e:
        write_log(
            "Error al obtener los datos de product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "No fue posible obtener los datos finales del reporte."
        }), 500


    # ============================================================
    # 8. VALIDAR DATOS DE PRODUCT_REPORT
    # ============================================================

    try:

        required_columns = [
            "date",
            "prod_name",
            "tot_prod_sl",
            "tot_clie_sl",
            "money"
        ]

        # Validar columnas
        missing_columns = [
            column
            for column in required_columns
            if column not in prod_data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Faltan columnas requeridas: {missing_columns}"
            )

        # Validar nulos
        if prod_data[required_columns].isnull().any().any():

            null_columns = (
                prod_data[required_columns]
                .columns[
                    prod_data[required_columns]
                    .isnull()
                    .any()
                ]
                .tolist()
            )

            raise ValueError(
                f"Se encontraron valores nulos en: {null_columns}"
            )

        # Validar negativos
        numeric_columns = [
            "tot_prod_sl",
            "tot_clie_sl",
            "money"
        ]

        negative_data = (
            prod_data[numeric_columns] < 0
        ).any()

        negative_columns = (
            negative_data[
                negative_data
            ]
            .index
            .tolist()
        )

        if negative_columns:
            raise ValueError(
                f"Se encontraron valores negativos en: "
                f"{negative_columns}"
            )

        # Convertir fecha
        prod_data["date"] = pd.to_datetime(
            prod_data["date"],
            errors="raise"
        ).dt.strftime("%Y-%m-%d")

    except Exception as e:

        write_log(
            "Error en la validación de los datos de product_report.",
            e
        )

        if conn:
            conn.close()

        return jsonify({
            "status": "error",
            "message": "Los datos finales del reporte no son válidos."
        }), 422


    # ============================================================
    # 9. CERRAR CONEXIÓN
    # ============================================================

    try:
        conn.close()

    except Exception as e:
        write_log(
            "Error al cerrar la conexión con la base de datos.",
            e
        )


    # ============================================================
    # 10. RESPONSE DE LA API
    # ============================================================

    return jsonify({
        "status": "success",
        "message": "Reporte histórico de productos generado correctamente.",
        "data": prod_data.to_dict(orient="records")
    }), 200


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)