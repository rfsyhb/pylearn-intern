import utils.helper as hp
import time

region_to_ss = hp.get_region()
print("siapkan lokasi")
time.sleep(5)
text_detected = hp.get_text_from_region(region_to_ss, config="--psm 6", save_debug=True)
print(text_detected)