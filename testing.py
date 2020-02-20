from catan_py import roll_dice, robber # if i try to import the whole file it won't run (only goes if main)
import classes
import items


def test_sum():
    assert sum([1, 2, 3]) == 6, "Should be 6"

if __name__ == "__main__":
    test_sum()
    print("Everything passed")