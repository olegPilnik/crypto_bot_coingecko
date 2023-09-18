import pytest

from connect_db import get_coin

"""Test module coin_functions"""



    
def test_get_coin():
    assert get_coin(0) == True