from psycopg2.extras import execute_values
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from sql.schema.db_connection import get_connection


def dataframe_to_tuples(df):
    return [tuple(row) for row in df.collect()]



def load_dim_warehouses(conn, dim_warehouses):

    cur = conn.cursor()

    query = """
        INSERT INTO dim_warehouses
        (
            plant_id,
            daily_capacity,
            unit_storage_cost
        )
        VALUES %s
        ON CONFLICT (plant_id)
        DO NOTHING;
    """

    data = dataframe_to_tuples(dim_warehouses)

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("dim_warehouses Loaded")


# ===============================
# DIM PRODUCTS
# ===============================

def load_dim_products(conn, dim_products):

    cur = conn.cursor()

    query = """
        INSERT INTO dim_products
        (
            product_id
        )
        VALUES %s
        ON CONFLICT (product_id)
        DO NOTHING;
    """

    data = dataframe_to_tuples(dim_products)

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("dim_products Loaded")


# ===============================
# DIM CARRIERS
# ===============================

def load_dim_carriers(conn, dim_carriers):

    cur = conn.cursor()

    query = """
        INSERT INTO dim_carriers
        (
            carrier_id,
            origin_port,
            destination_port,
            tpt_day_cnt
        )
        VALUES %s
        ON CONFLICT (carrier_id)
        DO NOTHING;
    """

    data = dataframe_to_tuples(dim_carriers)

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("dim_carriers Loaded")

    # ===============================
# BRIDGE TABLE
# ===============================

def load_bridge_products_per_plant(
    conn,
    bridge_products_per_plant
):

    cur = conn.cursor()

    query = """
        INSERT INTO bridge_products_per_plant
        (
            plant_id,
            product_id
        )
        VALUES %s
        ON CONFLICT (plant_id, product_id)
        DO NOTHING;
    """

    data = dataframe_to_tuples(
        bridge_products_per_plant
    )

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("bridge_products_per_plant Loaded")


# ===============================
# FACT ORDERS
# ===============================

def load_fact_orders(
    conn,
    fact_orders
):

    cur = conn.cursor()

    query = """
        INSERT INTO fact_orders
        (
            order_id,
            product_id,
            plant_id,
            carrier_id,
            destination_port,
            unit_quantity,
            unit_weight,
            order_date,
            estimated_transit_days,
            estimated_delivery_date
        )
        VALUES %s
        ON CONFLICT (order_id)
        DO NOTHING;
    """

    data = dataframe_to_tuples(
        fact_orders
    )

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("fact_orders Loaded")

    # ===============================
# WAREHOUSE HEALTH
# ===============================

def load_warehouse_health(
    conn,
    warehouse_health
):

    cur = conn.cursor()

    query = """
        INSERT INTO analytics.warehouse_health
        (
            plant_id,
            report_date,
            daily_order_count,
            utilization_pct,
            unit_storage_cost
        )
        VALUES %s;
    """

    data = dataframe_to_tuples(warehouse_health)

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("warehouse_health Loaded")


# ===============================
# CARRIER PERFORMANCE
# ===============================

def load_carrier_performance(
    conn,
    carrier_performance
):

    cur = conn.cursor()

    query = """
        INSERT INTO analytics.carrier_performance
        (
            carrier_id,
            destination_port,
            avg_transit_days,
            order_count,
            rank_by_speed
        )
        VALUES %s;
    """

    data = dataframe_to_tuples(carrier_performance)

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("carrier_performance Loaded")


# ===============================
# ORDER ROUTING PRIORITY
# ===============================

def load_order_routing_priority(
    conn,
    order_routing_priority
):

    cur = conn.cursor()

    query = """
        INSERT INTO analytics.order_routing_priority
        (
            order_id,
            utilization_pct,
            estimated_transit_days,
            risk_score,
            risk_rank
        )
        VALUES %s;
    """

    data = dataframe_to_tuples(order_routing_priority)

    execute_values(
        cur,
        query,
        data
    )

    cur.close()

    print("order_routing_priority Loaded")


# ===============================
# MASTER LOADER
# ===============================

def load_to_postgres(
    dim_warehouses,
    dim_products,
    dim_carriers,
    bridge_products_per_plant,
    fact_orders,
    warehouse_health,
    carrier_performance,
    order_routing_priority
):

    conn = get_connection()

    try:

        load_dim_warehouses(
            conn,
            dim_warehouses
        )

        load_dim_products(
            conn,
            dim_products
        )

        load_dim_carriers(
            conn,
            dim_carriers
        )

        load_bridge_products_per_plant(
            conn,
            bridge_products_per_plant
        )

        load_fact_orders(
            conn,
            fact_orders
        )

        load_warehouse_health(
            conn,
            warehouse_health
        )

        load_carrier_performance(
            conn,
            carrier_performance
        )

        load_order_routing_priority(
            conn,
            order_routing_priority
        )

        conn.commit()

        print("=" * 60)
        print("All Tables Successfully Loaded Into PostgreSQL")
        print("=" * 60)

    except Exception as e:

        conn.rollback()

        print(f"Loading Failed : {e}")

        raise

    finally:

        conn.close()