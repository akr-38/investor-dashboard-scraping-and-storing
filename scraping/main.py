import find_quaterly_sales
import combine_quaterly_sale
import push_to_db
years = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
quaters = [1,2,3,4]

# for year in years:
#     for quater in quaters:
#         find_quaterly_sales.find(year, quater)
#         combine_quaterly_sale.combine(year, quater)
#         push_to_db(year, quater)


# find_quaterly_sales.find(2010, 1)
# combine_quaterly_sale.combine(2010, 1)
# push_to_db.push(2010, 1)

# find_quaterly_sales.find(2010, 2)
# combine_quaterly_sale.combine(2010, 2)
# push_to_db.push(2010, 2)

# find_quaterly_sales.find(2015, 3)
# combine_quaterly_sale.combine(2015, 3)
# push_to_db.push(2015, 3)

for year in years:
    for quater in quaters:
        find_quaterly_sales.find(year, quater)
        combine_quaterly_sale.combine(year, quater)
        push_to_db.push(year, quater)

find_quaterly_sales.find(2025, 1)
combine_quaterly_sale.combine(2025, 1)
push_to_db.push(2025, 1)

find_quaterly_sales.find(2025, 2)
combine_quaterly_sale.combine(2025, 2)
push_to_db.push(2025, 2)



