file_path = "src/eula.txt"
file = open(file_path, "r+")

lines = file.readlines()
for i in range(len(lines)):
    line = lines[i]
    if line.startswith("#"):
        continue
    if line.startswith("eula=false"):
        lines[i] = "eula=true\n"

        file.seek(0)
        file.truncate()
        file.seek(0)
        file.writelines(lines)
        
        print("Eula property changed to true")
        break
    elif line.startswith("eula=true"):
        print("Eula property is already set to true")
        break
    else:
        print("Eula property is invalid")
        break
