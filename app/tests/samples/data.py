"""Creates fake Spark DataFrames to be used on test cases.

This module is mainly used by a conftest file for creating fixtures using fake
Spark DataFrames. The idea behind this script file is to provide data to be
used to test features from other library modules.

___
"""

# Importing libraries
from pyspark.sql.types import StringType, IntegerType

# Creating a dicionary with all infos needed to create sample DataFrames
SAMPLES_DICT = {
    "tbl_brecommerce_orders": {
        "schema": {
            "idx": IntegerType,
            "order_id": StringType,
            "customer_id": StringType,
            "order_status": StringType,
            "order_purchase_ts": StringType,
            "order_approved_at": StringType,
            "order_deliv_carrier_dt": StringType,
            "order_deliv_customer_dt": StringType,
            "order_estim_deliv_dt": StringType
        },
        "data": [
            (1, "e481f51cbdc54678b7cc49136f2d6af7", "9ef432eb6251297304e76186b10a928d", "delivered", "02/10/2017 10:56", "02/10/2017 11:07", "04/10/2017 19:55", "10/10/2017 21:25", "18/10/2017 00:00"),
            (2, "53cdb2fc8bc7dce0b6741e2150273451", "b0830fb4747a6c6d20dea0b8c802d7ef", "delivered", "24/07/2018 20:41", "26/07/2018 03:24", "26/07/2018 14:31", "07/08/2018 15:27", "13/08/2018 00:00"),
            (3, "47770eb9100c2d0c44946d9cf07ec65d", "41ce2a54c0b03bf3443c3d931a367089", "delivered", "08/08/2018 08:38", "08/08/2018 08:55", "08/08/2018 13:50", "17/08/2018 18:06", "04/09/2018 00:00"),
            (4, "949d5b44dbf5de918fe9c16f97b45f8a", "f88197465ea7920adcdbec7375364d82", "delivered", "18/11/2017 19:28", "18/11/2017 19:45", "22/11/2017 13:39", "02/12/2017 00:28", "15/12/2017 00:00"),
            (5, "ad21c59c0840e6cb83a9ceb5573f8159", "8ab97904e6daea8866dbdbc4fb7aad2c", "delivered", "13/02/2018 21:18", "13/02/2018 22:20", "14/02/2018 19:46", "16/02/2018 18:17", "26/02/2018 00:00"),
            (6, "a4591c265e18cb1dcee52889e2d8acc3", "503740e9ca751ccdda7ba28e9ab8f608", "delivered", "09/07/2017 21:57", "09/07/2017 22:10", "11/07/2017 14:58", "26/07/2017 10:57", "01/08/2017 00:00"),
            (7, "136cce7faa42fdb2cefd53fdc79a6098", "ed0271e0b7da060a393796590e7b737a", "invoiced", "11/04/2017 12:22", "13/04/2017 13:25", "09/05/2017 00:00", "", ""),
            (8, "6514b8ad8028c9f2cc2374ded245783f", "9bdf08b4b3b52b5526ff42d37d47f222", "delivered", "16/05/2017 13:10", "16/05/2017 13:22", "22/05/2017 10:07", "26/05/2017 12:55", "07/06/2017 00:00"),
            (9, "76c6e866289321a7c93b82b54852dc33", "f54a9f0e6b351c431402b8461ea51999", "delivered", "23/01/2017 18:29", "25/01/2017 02:50", "26/01/2017 14:16", "02/02/2017 14:08", "06/03/2017 00:00"),
            (10, "e69bfb5eb88e0ed6a785585b27e16dbf", "31ad1d1b63eb9962463f764d4e6e0c9d", "delivered", "29/07/2017 11:55", "29/07/2017 12:05", "10/08/2017 19:45", "16/08/2017 17:14", "23/08/2017 00:00")
        ]
    }
}
