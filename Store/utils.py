from datetime import datetime


# Functions

# Generating a unique code used as order or transaction id
# Or cookie to identify unique customers
def generateUniqueId():
    return str(datetime.now().timestamp()).replace('.', '-')

