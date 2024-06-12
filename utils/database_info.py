from utils.database import create_category, create_product_pic, add_item_to_basket, create_user_basket, \
    basket_total_value, delete_basket, get_basket, get_categories, delete_order

# delete_order(6)
# create_category('binoculars')
# create_category('flashlights')
# create_category('backpacks')
# create_category('radios')
# create_category('radio_accessories')
#
# create_product_pic(product_name="Binoculars 8x40",
#                    brand="Bedell",
#                    description="Magnification: x8, Frontal lens: 40mm",
#                    price=750.00,
#                    category_id=1,
#                    quantity_available=100,
#                    photo_url='pictures/bedell840.jpg',
#                    photo="D:\Python\goadventure_bot\pictures\dbbedell840.png")
#
# create_product_pic(product_name="Binoculars 20x50",
#                    brand="Bedell",
#                    description="Magnification: x20, Frontal lens: 50mm",
#                    price=1100.00,
#                    category_id=1,
#                    quantity_available=100,
#                    photo_url='pictures/bedell2050.jpg',
#                    photo="D:\Python\goadventure_bot\pictures\dbbedell2050.png")
#
# create_product_pic(product_name="Binoculars 12x60",
#                    brand="Sakura",
#                    description="Magnification: x12, Frontal lens: 60mm",
#                    price=1820.00,
#                    category_id=1,
#                    quantity_available=100,
#                    photo_url='pictures/sakura1260.jpg',
#                    photo="D:\Python\goadventure_bot\pictures\dbsakura1260.png")
#
#
# print(get_categories())
# create_user_basket(1572426988)
# add_item_to_basket(1572426988, 4, 20, 3)
# add_item_to_basket(1572426988, 5, 30, 1)
# add_item_to_basket(1572426988, 5, 50, 2)
# print(basket_total_value(7))
# delete_basket(695904835)
# delete_basket(1572426988)
#
# print(get_basket(695904835))
# # print(get_basket(6254963765))
# #
# # 531877876,Софія Оржеховська,,,
# # 6254963765,GoAdventure,,,
# # 695904835,Olga,olga.tsybko@gmail.com,593992361104,"{'country_code': 'UA', 'state': 'Cherkasy', 'city': 'Cherkasy', 'street_line1': 'Gagarina', 'street_line2': '1', 'post_code': '18000'}"
