GLOBAL_VAR = 1
def main(x: int) -> None:
    """
    Increments the input integer by 1 and prints the result.

    Args:
        x (int): The integer to be incremented.

    Returns:
        None
    """
    try:
        if x is None:
            raise TypeError("x must not be None")
        new_x: int = x + GLOBAL_VAR
        print(new_x)
    except Exception as e:
        print(f"An error occurred: {e}")
print(GLOBAL_VAR)
x_init = 5
main(x_init)