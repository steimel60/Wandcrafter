response = ["LOAD_GAME", "DATA GOES HERE", "NEW_GAME", "HARD_MODE"]
response_1 = ["LOAD_GAME", "DATA GOES HERE"]
response_2 = ["LOAD_GAME", None]
response_3 = ["LOAD_GAME"]

def test_func(data, tags):
    print("Data:", data,"\nTags:", tags)

for r in [response, response_1, response_2, response_3]:
    match r:
        case ["CHANGE_STATE", new_state]: print(1)
        case ["LOAD_GAME", data, *tags]: test_func(data, tags) 
        case _: print("INVALID")