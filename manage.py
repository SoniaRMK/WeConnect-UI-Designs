import os
import unittest
from flask_script import Manager 
from resources import app

manage = Manager(app)

@manage.command
def migrator():
    #os.system('set FLASK_APP=run'):
        
    #os.system('flask db init')
    os.system('flask db migrate')
    os.system('flask db upgrade')

@manage.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests' , pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manage.run()