from pyspark.sql.functions import col


def create_dimension_tables(
    final_df,
    capacity,
    cost,
    products,
    freight
):

    dim_warehouses = (
        capacity
        .join(
            cost,
            on="plant_code",
            how="left"
        )
        .select(
            "plant_code",
            "daily_capacity",
            "unit_storage_cost"
        )
        .dropDuplicates()
    )

    print("Dimension : Warehouses Created")

    dim_products = (
        products
        .select(
            "product_id"
        )
        .dropDuplicates()
    )

    print("Dimension : Products Created")

    dim_carriers = (
        freight
        .select(
            col("freight_carrier").alias("carrier_id"),
            col("orig_port_cd").alias("origin_port"),
            col("dest_port_cd").alias("destination_port"),
            "tpt_day_cnt",
            "svc_cd",
            "mode_dsc",
            "carrier_type"
        )
        .dropDuplicates()
    )

    print("Dimension : Carriers Created")

    bridge_products_per_plant = (
        products
        .select(
            "plant_code",
            "product_id"
        )
        .dropDuplicates()
    )

    print("Bridge Table Created")


    fact_orders = (
        final_df
        .select(
            col("order_id"),
            col("order_date"),
            col("product_id"),
            col("plant_code"),
            col("carrier").alias("carrier_id"),
            col("destination_port"),
            col("unit_quantity"),
            col("weight").alias("unit_weight"),
            col("tpt_day_cnt").alias("estimated_transit_days"),
            col("estimated_delivery_date")
        )
        .dropDuplicates()
    )

    print("Fact Orders Created")


    return (
        dim_warehouses,
        dim_products,
        dim_carriers,
        bridge_products_per_plant,
        fact_orders
    )