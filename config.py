_sec = 1
_min = 60 * _sec
_hour = 60*_min
_day = 24*_hour
week1 = 7*_day
month1 = 30*_day


tempFolder = 'temp'
DeviceID = 1001
COM = '/dev/ttyUSB0'
BAUD =  115200

camera1 = 0
camera2 = 1

view = False

url = "https://noque.online/wp-json/wc/v3/products?search="
headers = {
    'Cookie': 'woocommerce_cart_hash=8c51e47121af273b053c8aee7cc7a0a9; woocommerce_items_in_cart=1; wp_woocommerce_session_2feee0a6069da1c70f986bccda3f1c5b=1%7C%7C1646818973%7C%7C1646815373%7C%7Ca3511c00402733b104873477f681e32b'
    }