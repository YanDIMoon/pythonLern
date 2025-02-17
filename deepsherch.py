data = {"name":"Dima",
        "details":
        {"age": 24,
         "stats": {"weight": "84","height": "195"},
         "hobbies": {"Vgames": "Cs"}
         }
}

def iterate_nested_dict(d, parent_key=""):
    for key, value in d.items():

        full_key = f"{parent_key}.{key}" if parent_key else key 

        if isinstance(value, dict):
            iterate_nested_dict(value, full_key)  

        else:
            print(f"{full_key}: {value}") 


iterate_nested_dict(data)