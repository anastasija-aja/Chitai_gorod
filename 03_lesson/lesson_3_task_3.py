from address import Address
from mailing import Mailing
from_address = Address("143000", "Moscow","Parkovaya", "1", "11")
to_address = Address("143001", "Moscow","Parkovaya", "2", "22")
mailing = Mailing(to_address, from_address,123, "AA322223")
print(mailing)