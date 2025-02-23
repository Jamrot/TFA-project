import pymysql

output = []

connection = pymysql.connect(
    host="localhost",
    user="root",
    password="000",
    database="icall_data"
)

cursor = connection.cursor()

output.append("------ICALL TABLE------")
cursor.execute("SELECT * FROM icall_target_table")

columns = [desc[0] for desc in cursor.description]
output.append(f"Column titles: {columns}")

results = cursor.fetchall()

for row in results:
    output.append(row)

output.append("------FUNC TABLE------")
cursor.execute("SELECT * FROM func_table")

columns = [desc[0] for desc in cursor.description]
output.append(f"Column titles: {columns}")

results = cursor.fetchall()

for row in results:
    output.append(row)

output.append("------CALLER TABLE------")
cursor.execute("SELECT * FROM caller_table")

columns = [desc[0] for desc in cursor.description]
output.append(f"Column titles: {columns}")

results = cursor.fetchall()

for row in results:
    output.append(row)

cursor.close()
connection.close()

output_path = "/home/jamrot/TFA-project/test/output-all.txt"

with open(output_path, "w") as f:
    for line in output:
        f.write(str(line) + "\n")

print("Output saved to", output_path)