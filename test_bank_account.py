from bank_account import BankAccount


def test_creat_account():
    """checking create new account"""
    test_account = BankAccount("Yossi", 1000)
    assert test_account.get_owner_name() == "Yossi"
    assert test_account.get_balance() == 1000
    



def test_creat_account_and_deposit():
    """checking create new account and deposit"""
    test_account = BankAccount("Yossi", 1000)
    test_account.deposit(5000)
    assert test_account.get_balance() == 6000
    

def test_validate_static_method():
    """checking the is valid amount function"""
    assert BankAccount.is_valid_amount(-5) == False
    assert BankAccount.is_valid_amount(100) == True