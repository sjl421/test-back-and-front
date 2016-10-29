"""Configuration module."""

# Api version
API_VERSION = '1.0'

# In memory database-dict to store the information

DATABASE = {
    'business': {}
}

# Base amount for the loan criteria
BASE_AMOUNT = 50000

# Loan statuses
status = {
    'APPROVED': 'Approved',
    'DECLINED': 'Declined',
    'UNDECIDED': 'Undecided'
}
