"""Putting together user inputs to help on building fixtures and test cases.

This file aims to put together all variables used on fixture definitions and
test cases that requires user inputs as a way to configure or validate
something.

___
"""

# Defining a dictionary with all source data used on the Glue Job
SOURCE_DATAFRAMES_DICT = {
    "tbl_brecommerce_orders": {
        "name": "tbl_brecommerce_orders",
        "dataframe_reference": "df_orders",
        "empty": False,
        "fake_data": False,
        "fields": [
            {
                "Name": "idx",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_status",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_purchase_ts",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_approved_at",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_deliv_carrier_dt",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_deliv_customer_dt",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_estim_deliv_dt",
                "Type": "string",
                "nullable": True
            }
        ],
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
    },
    "tbl_brecommerce_order_items": {
        "name": "tbl_brecommerce_order_items",
        "dataframe_reference": "df_order_items",
        "empty": False,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_item_id",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "product_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "seller_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "shipping_limit_date",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "freight_value",
                "Type": "double",
                "nullable": True
            }
        ],
        "data": [
            ["a4591c265e18cb1dcee52889e2d8acc3", 1, "060cb19345d90064d1015407193c233d", "8581055ce74af1daba164fdbd55a40de", "2017-07-13 22:10:13", 147.9, 27.36],
            ["ad21c59c0840e6cb83a9ceb5573f8159", 1, "65266b2da20d04dbe00c5c2d3bb7859e", "2c9e548be18521d1c43cde1c582c6de8", "2018-02-19 20:31:37", 19.9, 8.72],
            ["e481f51cbdc54678b7cc49136f2d6af7", 1, "87285b34884572647811a353c7ac498a", "3504c0cb71d7fa48d967e0e4c94d59d9", "2017-10-06 11:07:15", 29.99, 8.72],
            ["e69bfb5eb88e0ed6a785585b27e16dbf", 1, "9a78fb9862b10749a117f7fc3c31f051", "7c67e1448b00f6e969d365cea6b010ab", "2017-08-11 12:05:32", 149.99, 19.77]
        ]
    },
    "tbl_brecommerce_customers": {
        "name": "tbl_brecommerce_customers",
        "dataframe_reference": "df_customers",
        "empty": False,
        "fake_data": False,
        "fields": [
            {
                "Name": "customer_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_unique_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_zip_code_prefix",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "customer_city",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_state",
                "Type": "string",
                "nullable": True
            }
        ],
        "data": [
            ["f54a9f0e6b351c431402b8461ea51999", "39382392765b6dc74812866ee5ee92a7", 0, "faxinalzinho", "RS"],
            ["f88197465ea7920adcdbec7375364d82", "7c142cf63193a1473d2e66489a9ae977", 0, "sao goncalo do amarante", "RN"],
            ["ed0271e0b7da060a393796590e7b737a", "36edbb3fb164b1f16485364b6fb04c73", 0, "santa rosa", "RS"],
            ["b0830fb4747a6c6d20dea0b8c802d7ef", "af07308b275d755c9edb36a90c618231", 0, "barreiras", "BA"]
        ]
    },
    "tbl_brecommerce_payments": {
        "name": "tbl_brecommerce_payments",
        "dataframe_reference": "df_payments",
        "empty": False,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "payment_sequential",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "payment_type",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "payment_installments",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "payment_value",
                "Type": "double",
                "nullable": True
            }
        ],
        "data": [                
            ["e481f51cbdc54678b7cc49136f2d6af7", 1, "credit_card", 1, 18.12],
            ["e69bfb5eb88e0ed6a785585b27e16dbf", 2, "voucher", 1, 161.42],
            ["a4591c265e18cb1dcee52889e2d8acc3", 1, "credit_card", 6, 175.26],
            ["e481f51cbdc54678b7cc49136f2d6af7", 3, "voucher", 1, 2.0],
            ["e69bfb5eb88e0ed6a785585b27e16dbf", 1, "credit_card", 1, 8.34],
            ["ad21c59c0840e6cb83a9ceb5573f8159", 1, "credit_card", 1, 28.62],
            ["e481f51cbdc54678b7cc49136f2d6af7", 2, "voucher", 1, 18.59]
        ]
    },
    "tbl_brecommerce_reviews": {
        "name": "tbl_brecommerce_reviews",
        "dataframe_reference": "df_reviews",
        "empty": False,
        "fake_data": False,
        "fields": [
            {
                "Name": "review_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "review_score",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "review_comment_title",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "review_comment_message",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "review_creation_date",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "review_answer_timestamp",
                "Type": "string",
                "nullable": True
            }
        ],
        "data": [                
            ["7bc2406110b926393aa56f80a40eba40", "73fc7af87114b39712e6da79b0a377eb", 4, "", "", "2018-01-18 00:00:00", "2018-01-18 21:46:59"],
            ["80e641a11e56f04c1ad469d5645fdfde", "a548910a1c6147796b98fdf73dbeba33", 5, "", "", "2018-03-10 00:00:00", "2018-03-11 03:05:13"],
            ["228ce5500dc1d8e020d8d1322874b6f0", "f9e4b658b201a9f2ecdecbb34bed034b", 5, "", "", "2018-02-17 00:00:00", "2018-02-18 14:36:24"],
            ["e64fb393e7b32834bb789ff8bb30750e", "658677c97b385a9be170737859d3511b", 5, "", "Recebi bem antes do prazo estipulado.", "2017-04-21 00:00:00", "2017-04-21 22:02:06"],
            ["f7c4243c7fe1938f181bec41a392bdeb", "8e6bfb81e283fa7e4f11123a3fb894f1", 5, "", "Parabéns lojas lannister adorei comprar pela Internet seguro e prático Parabéns a todos feliz Páscoa", "2018-03-01 00:00:00", "2018-03-02 10:26:53"],
            ["15197aa66ff4d0650b5434f1b46cda19", "b18dcdf73be66366873cd26c5724d1dc", 1, "", "", "2018-04-13 00:00:00", "2018-04-16 00:39:37"],
            ["07f9bee5d1b850860defd761afa7ff16", "e48aa0d2dcec3a2e87348811bcfdf22b", 5, "", "", "2017-07-16 00:00:00", "2017-07-18 19:30:34"],
            ["7c6400515c67679fbee952a7525281ef", "c31a859e34e3adac22f376954e19b39d", 5, "", "", "2018-08-14 00:00:00", "2018-08-14 21:36:06"],
            ["a3f6f7f6f433de0aefbb97da197c554c", "9c214ac970e84273583ab523dfafd09b", 5, "", "", "2017-05-17 00:00:00", "2017-05-18 12:05:37"],
            ["8670d52e15e00043ae7de4c01cc2fe06", "b9bf720beb4ab3728760088589c62129", 4, "", "recomendo aparelho eficiente. no site a marca do aparelho esta impresso como 3desinfector e ao chegar esta com outro nome...atualizar com a marca correta uma vez que é o mesmo aparelho", "2018-05-22 00:00:00", "2018-05-23 16:45:47"]
        ]
    },
}

# Defining a dictionary with all the expected results of transformation methods
EXPECTED_DATAFRAMES_DICT = {
    "tbl_brecommerce_orders": {
        "dataframe_reference": "df_orders_prep",
        "empty": True,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_status",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_approved_at",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_deliv_carrier_dt",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_deliv_customer_dt",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_estim_deliv_dt",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_purchase_ts",
                "Type": "date",
                "nullable": True
            },
            {
                "Name": "year_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "quarter_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "month_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "dayofmonth_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "dayofweek_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "dayofyear_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "weekofyear_order_purchase_ts",
                "Type": "int",
                "nullable": True
            }
        ],
        "data": []
    },
    "tbl_brecommerce_order_items": {
        "dataframe_reference": "df_order_items_prep",
        "empty": True,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "qty_order_items",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "sum_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "mean_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "max_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "min_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "mean_order_freight_value",
                "Type": "double",
                "nullable": True
            }
        ],
        "data": []
    },
    "tbl_brecommerce_customers": {
        "dataframe_reference": "df_customers_prep",
        "empty": True,
        "fake_data": False,
        "fields": [
            {
                "Name": "customer_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_city",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_state",
                "Type": "string",
                "nullable": True
            }
        ],
        "data": []
    },
    "tbl_brecommerce_payments": {
        "dataframe_reference": "df_payments_prep",
        "empty": True,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "sum_payment_value",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "mean_payment_value",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "count_payment_value",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "most_common_payment_type",
                "Type": "string",
                "nullable": True
            }
        ],
        "data": []
    },
    "tbl_brecommerce_reviews": {
        "dataframe_reference": "df_reviews_prep",
        "empty": True,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "review_best_score",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "review_comment_message",
                "Type": "string",
                "nullable": True
            }
        ],
        "data": []
    },
    "tbl_sot": {
        "dataframe_reference": "df_sot_prep",
        "empty": True,
        "fake_data": False,
        "fields": [
            {
                "Name": "order_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_id",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_status",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "order_purchase_ts",
                "Type": "date",
                "nullable": True
            },
            {
                "Name": "order_approved_at",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_deliv_carrier_dt",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_deliv_customer_dt",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "order_estim_deliv_dt",
                "Type": "timestamp",
                "nullable": True
            },
            {
                "Name": "year_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "quarter_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "month_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "dayofmonth_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "dayofweek_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "dayofyear_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "weekofyear_order_purchase_ts",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "qty_order_items",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "sum_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "mean_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "max_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "min_order_price",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "mean_order_freight_value",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "customer_city",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "customer_state",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "sum_payment_value",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "mean_payment_value",
                "Type": "double",
                "nullable": True
            },
            {
                "Name": "count_payment_value",
                "Type": "bigint",
                "nullable": True
            },
            {
                "Name": "most_common_payment_type",
                "Type": "string",
                "nullable": True
            },
            {
                "Name": "review_best_score",
                "Type": "int",
                "nullable": True
            },
            {
                "Name": "review_comment_message",
                "Type": "string",
                "nullable": True
            }
        ],
        "data": []
    }
}
