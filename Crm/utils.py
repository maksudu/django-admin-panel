from django.conf import settings
from datetime import datetime
from dateutil.relativedelta import relativedelta
ordinal_suffix={1:'st', 2: 'nd', 3: 'rd'}
from hashids import Hashids

SECRET_KEY = '(0%gm^z6s2&y4h^m_vvcq+m7_vl*meg+yggy6@g)!1i_b2o9q_'
hashids = Hashids(salt = SECRET_KEY, min_length = 20)


def get_encoded_id(id):
	return hashids.encrypt(id)

def get_decoded_id(encoded_id):
	return hashids.decrypt(encoded_id)[0]

def get_ordinal(num):
	return str(num)+(ordinal_suffix[num%10] if num%10 in ordinal_suffix.keys() else "th")

