""" Test database """
from models.cause import Cause
from models.donor import Donor
from models.recipient import Recipient
from models.contract import Contract
from models import storage as db

def test_cause():
    pass

def test_donor():
    new_donor = Donor(first_name='Sigma', second_name='Chad')
    db.new(new_donor)


if __name__ == "__main__":
    test_donor()
