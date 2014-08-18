from json import loads, dumps
from saving import save_item
import MySQLdb as mdb
import numpy as np
from secret import pw

def normalize_categories(cat):
	if 'Pet' in cat:
		return 'Pets'
	if 'Toys and Hobbies' in cat:
		return 'Toys and Hobbies'
	if 'Blanket' in cat:
		return 'Blankets'
	if 'Home' in cat:
		return 'Home'
	if 'Components' in cat:
		return 'Components'
	if 'Cardigan' in cat:
		return 'Cardigans'
	if 'Sweater' in cat :
		return 'Sweaters'
	if 'Clothing' in cat:
		return 'Other Clothing'
	if 'Bag' in cat:
		return 'Bags'
	if 'Feet / Legs' in cat:
		return 'Feet/Leg Accessories'
	if 'Hands' in cat:
		return 'Hand Accessories'
	if 'Hat' in cat:
		return 'Hats'
	if 'Neck / Torso' in cat:
		return 'Neck/Torso Accessories'
	if 'Accessories' in cat:
		return 'Other Accessories'

def craft_type(number):
	if number == 1:
		return 'crochet'
	if number == 2:
		return 'knit'

db = mdb.connect('localhost', 'iva', pw, 'Ravelry', charset='utf8')
with db:    
	cur = db.cursor()
	cur.execute("SELECT pattern_id, categories, craft_id FROM Patterns;")	
	
	categories = {int(row[0]): normalize_categories(row[1]) for row in cur if row[1]}
	crafts = {int(row[0]): craft_type(int(row[2])) for row in cur if int(row[2]) < 3}
	
save_item('data/categories', categories)
save_item('data/crafts', crafts)

