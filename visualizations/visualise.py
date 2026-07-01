from pyspark.sql.functions import col, count

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from pyspark_folder.elt.config import CURATED_PATH

sns.set_style("whitegrid")


class LogisticsVisualization:

    def __init__(
            
        self,
        final_df,
        warehouse_health,
        carrier_performance,
        fact_orders
    ):
        
        self.final_df = final_df
        self.warehouse_health = warehouse_health.toPandas()
        self.carrier_performance = carrier_performance.toPandas()
        self.fact_orders = fact_orders.toPandas()
        
   

    
    def order_volume_trend(self,plant_code=None):

        trend = (
            self.final_df.groupby(["order_date", "plant_code"]).agg(count("order_id").alias("count")).orderBy("order_date")
        )
        print(
        self.final_df.select("order_date")
        .distinct()
        .orderBy("order_date")
        .show(20, False)
)
        pdf=trend.toPandas()
        if plant_code:
            pdf = pdf[pdf["plant_code"] == plant_code]
        
        pdf=pdf.sort_values("order_date")
        plt.figure(figsize=(10, 6))
        if plant_code:
            plt.plot(pdf["order_date"], pdf["count"], marker="o", label=f"Plant {plant_code}") 
            plt.title("Daily Order Volume Trend By Warehouse")
        else:
            for plant in pdf["plant_code"].unique():
                plant_data = pdf[pdf["plant_code"] == plant]
                plt.plot(plant_data["order_date"], plant_data["count"], marker="o", label=f"Plant {plant}")
            plt.title("Daily Order Volume Trend By Warehouse")
        plt.xlabel("Order Date")
        plt.ylabel("Order Count")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

   
    