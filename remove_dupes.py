with open("output.txt", "r") as f:
    unique = set(f.readlines())
    with open("clean_output.txt", "w") as new_f:
        new_f.writelines(set(unique))
