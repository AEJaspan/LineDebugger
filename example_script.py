# import weaviate

GLOBAL_VAR = 1
def main(x: int) -> None:
    """
    Increments the input integer by 1 and prints the result.

    Args:
        x (int): The integer to be incremented.

    Returns:
        None
    """
    return 1/0
#     global GLOBAL_VAR
#     # Create the connection parameters object
#     connection_params = weaviate.ConnectionParams(
#         url="http://localhost:8080"
#     )
#     client = weaviate.WeaviateClient(connection_params)    
#     if GLOBAL_VAR > 3:
#         raise ValueError("GLOBAL_VAR is too large")
#     for i in range(3):
#         try:
#             if x is None:
#                 raise TypeError("x must not be None")
#             new_x: int = x + GLOBAL_VAR
#             GLOBAL_VAR += 5
#             print(new_x)
#             yield new_x
#         except Exception as e:
#             print(f"An error occurred: {e}")
# x_init = 5
# print([x for x in main(x_init)])
# print(x_init)
main(1)