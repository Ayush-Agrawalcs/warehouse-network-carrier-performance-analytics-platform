# from pyspark.sql import SparkSession
# from pyspark.sql.functions import (col,when,current_date,count,avg,round,dense_rank,date_add,row_number)
# from config import *
# from pyspark.sql.window import Window

# spark = (
#     SparkSession.builder
#     .appName("Warehouse")
#     .config(
#         "spark.jars.packages",
#         "org.apache.hadoop:hadoop-aws:3.4.1,"
#         "software.amazon.awssdk:bundle:2.29.52,"
#         "software.amazon.awssdk:url-connection-client:2.29.52"
#     )
#     .config("spark.hadoop.fs.s3a.endpoint", "s3.ap-south-1.amazonaws.com")
#     .config("spark.hadoop.fs.s3a.path.style.access", "true")
#     .config(
#         "spark.hadoop.fs.s3a.aws.credentials.provider",
#         "software.amazon.awssdk.auth.credentials.DefaultCredentialsProvider"
#     )
#     .getOrCreate()
# )

# orders=spark.read.csv(
#     ORDER_LIST ,
#     header=True,
#     inferSchema=True
# )

# freight=spark.read.csv(
#     FREIGHT_RATES,
#     header=True,
#     inferSchema=True
# )

# Capacity=spark.read.csv(
#     WH_CAPACITIES,
#     header=True,
#     inferSchema=True
# )

# cost=spark.read.csv(
#     WH_COSTS,
#     header=True,
#     inferSchema=True
# )

# product=spark.read.csv(
#     PRODUCTS_PER_PLANT,
#     header=True,
#     inferSchema=True
# )

# ports=spark.read.csv(
#     PLANT_PORTS,
#     header=True,
#     inferSchema=True
# )

# print("Succefully read data")
# print(orders.show(5))

# print("orderList")
# orders.printSchema()
# orders.show(5)

# print("FreightRates")
# freight.printSchema()

# print("WhCapacities")
# Capacity.printSchema()

# print("WhCosts")
# cost.printSchema()

# print("ProductsPerPlant")
# product.printSchema()

# print("PlantPorts")
# ports.printSchema()

# #check data quality
# print("Orders:", orders.count())
# print("Freight:", freight.count())
# print("Capacity:", Capacity.count())
# print("Cost:", cost.count())
# print("Products:", product.count())
# print("Ports:", ports.count())

# #check nyll values

# orders.filter(col("order Id").isNull()).show()

# #rename the column
# orders = (
#     orders
#     .withColumnRenamed("Order ID", "order_id")
#     .withColumnRenamed("Order Date", "order_date")
#     .withColumnRenamed("Origin Port", "origin_port")
#     .withColumnRenamed("Carrier", "carrier")
#     .withColumnRenamed("Product ID", "product_id")
#     .withColumnRenamed("Plant Code", "plant_code")
#     .withColumnRenamed("Destination Port", "destination_port")
#     .withColumnRenamed("Unit quantity", "unit_quantity")
#     .withColumnRenamed("Weight", "weight")
# )

# freight = (
#     freight
#     .withColumnRenamed("Carrier", "freight_carrier")
# )

# Capacity = (
#     Capacity
#     .withColumnRenamed("Plant ID", "plant_code")
#     .withColumnRenamed("Daily Capacity ", "daily_capacity")
# )

# cost = (
#     cost
#     .withColumnRenamed("WH", "plant_code")
#     .withColumnRenamed("Cost/unit", "unit_storage_cost")
# )

# product = (
#     product
#     .withColumnRenamed("Plant Code", "plant_code")
#     .withColumnRenamed("Product ID", "product_id")
# )

# ports = (
#     ports
#     .withColumnRenamed("Plant Code", "plant_code")
#     .withColumnRenamed("Port", "port")
# )

# orders.printSchema()


# #joining part
# orders_products = orders.join(
#     product,
#     on=["plant_code", "product_id"],
#     how="left"
# )
# print("Join 1 Completed")
# orders_products_freight = orders_products.join(
#     freight,
#     (orders_products.carrier == freight.freight_carrier) &
#     (orders_products.origin_port == freight.orig_port_cd) &
#     (orders_products.destination_port == freight.dest_port_cd),
#     "left"
# )
# print("Join 2 Completed")
# orders_products_freight_capacity = orders_products_freight.join(
#     Capacity,
#     on="plant_code",
#     how="left"
# )
# print("Join 3 Completed")
# final_df = orders_products_freight_capacity.join(
#     cost,
#     on="plant_code",
#     how="left"
# )
# print("Join 4 Completed")
# print("All Joins Completed Successfully")
# print("Total Records :", final_df.count())

# final_df.printSchema()

# final_df.show(10, truncate=False)

# #remove duplicate orders
# window_spec = Window.partitionBy("order_id").orderBy("order_date")

# final_df = (
#     final_df
#     .withColumn("row_num", row_number().over(window_spec))
#     .filter(col("row_num") == 1)
#     .drop("row_num")
# )

# print("Duplicate Removal Completed")
# print("Rows After Deduplication :", final_df.count())

# #Filter Invalid Quantity
# final_df = final_df.filter(
#     col("unit_quantity") > 0
# )

# print("Quantity Validation Completed")

# #handle missing value
# final_df = final_df.withColumn(
#     "weight",
#     when(col("weight").isNull(), 0)
#     .otherwise(col("weight"))
# )

# final_df = final_df.withColumn(
#     "estimated_delivery_date",
#     date_add(
#         col("order_date"),
#         col("tpt_day_cnt")
#     )
# )

# warehouse_health = (
#     final_df
#     .groupBy("plant_code")
#     .agg(
#         count("order_id").alias("daily_order_count"),
#         avg("daily_capacity").alias("daily_capacity"),
#         avg("unit_storage_cost").alias("unit_storage_cost")
#     )
# )

# carrier_performance = (
#     final_df
#     .groupBy(
#         "carrier",
#         "destination_port"
#     )
#     .agg(
#         avg("tpt_day_cnt").alias("avg_transit_days"),
#         count("order_id").alias("order_count")
#     )
# )

# final_df = final_df.withColumn(
#     "weight",
#     when(col("weight").isNull(), 0)
#     .otherwise(col("weight"))
# )

# print("Missing Weight Handled")

# final_df = final_df.withColumn(
#     "estimated_delivery_date",
#     date_add(
#         col("order_date"),
#         col("tpt_day_cnt")
#     )
# )

# print("Estimated Delivery Date Created")

# final_df.select(
#     "order_id",
#     "order_date",
#     "tpt_day_cnt",
#     "estimated_delivery_date"
# ).show(10, truncate=False)


# final_df.select(
#     "order_id",
#     "order_date",
#     "tpt_day_cnt",
#     "estimated_delivery_date"
# ).show(10, truncate=False)

# warehouse_health = (
#     final_df
#     .groupBy("plant_code")
#     .agg(
#         count("order_id").alias("daily_order_count"),
#         avg("daily_capacity").alias("daily_capacity"),
#         avg("unit_storage_cost").alias("unit_storage_cost")
#     )
# )

# warehouse_health = warehouse_health.withColumn(
#     "utilization_pct",
#     round(
#         (col("daily_order_count") / col("daily_capacity")) * 100,
#         2
#     )
# )

# print("Warehouse Health Created")

# warehouse_health.show(10, truncate=False)

# arrier_performance = (
#     final_df
#     .groupBy(
#         "carrier",
#         "destination_port"
#     )
#     .agg(
#         avg("tpt_day_cnt").alias("avg_transit_days"),
#         count("order_id").alias("order_count")
#     )
# )

# from pyspark.sql.window import Window
# from pyspark.sql.functions import dense_rank

# rank_window = Window.orderBy(
#     col("avg_transit_days")
# )

# carrier_performance = carrier_performance.withColumn(
#     "rank_by_speed",
#     dense_rank().over(rank_window)
# )

# print("Carrier Performance Created")

# carrier_performance.show(10, truncate=False)

# final_df = final_df.join(
#     warehouse_health.select(
#         "plant_code",
#         "utilization_pct"
#     ),
#     on="plant_code",
#     how="left"
# )
# final_df = final_df.withColumn(
#     "risk_score",
#     round(
#         (col("utilization_pct") * 0.6) +
#         (col("tpt_day_cnt") * 0.4),
#         2
#     )
# )
# risk_window = Window.orderBy(
#     col("risk_score").desc()
# )

# final_df = final_df.withColumn(
#     "risk_rank",
#     dense_rank().over(risk_window)
# )

# print("Order Routing Priority Created")

# final_df.select(
#     "order_id",
#     "plant_code",
#     "carrier",
#     "risk_score",
#     "risk_rank"
# ).show(10, truncate=False)


# final_df.write \
#     .mode("overwrite") \
#     .parquet(CURATED_PATH + "fact_orders")

# warehouse_health.write \
#     .mode("overwrite") \
#     .parquet(CURATED_PATH + "warehouse_health")

# carrier_performance.write \
#     .mode("overwrite") \
#     .parquet(CURATED_PATH + "carrier_performance")

# print("Curated Data Successfully Written to S3")

from extraction import create_spark, read_data, validate_data
from transformation import transform_data
from dimensions import create_dimension_tables
from analytics import create_analytics_tables
from loading import write_to_s3
from db_loader import load_to_postgres


def main():
    spark = create_spark()
    (
        orders,
        freight,
        capacity,
        cost,
        products,
        ports
    ) = read_data(spark)

    validate_data(
        orders,
        freight,
        capacity,
        cost,
        products,
        ports
    )
    (
        final_df,
        capacity,
        cost,
        products,
        freight
    ) = transform_data(
        orders,
        freight,
        capacity,
        cost,
        products,
        ports
    )
    (
        dim_warehouses,
        dim_products,
        dim_carriers,
        bridge_products_per_plant,
        fact_orders
    ) = create_dimension_tables(
        final_df,
        capacity,
        cost,
        products,
        freight
    )

    (
        warehouse_health,
        carrier_performance,
        order_routing_priority
    ) = create_analytics_tables(
        final_df
    )

    write_to_s3(
        dim_warehouses,
        dim_products,
        dim_carriers,
        bridge_products_per_plant,
        fact_orders,
        warehouse_health,
        carrier_performance,
        order_routing_priority
    )
    load_to_postgres(
    dim_warehouses,
    dim_products,
    dim_carriers,
    bridge_products_per_plant,
    fact_orders,
    warehouse_health,
    carrier_performance,
    order_routing_priority
)


    print("=" * 60)
    print("Warehouse ETL Pipeline Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()