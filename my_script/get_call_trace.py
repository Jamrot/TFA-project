import pymysql

def write_output(output, output_path):
    with open(output_path, "w") as f:
        for line in output:
            f.write(str(line) + "\n")
    
    print("Output saved to", output_path)

def get_hash(cursor, func_name):
    cursor.execute(f"SELECT * FROM caller_table WHERE func_name='{func_name}'")
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    elif len(results) > 1:
        raise ValueError("Multiple rows found for the same callee")
    else:
        return results[0][1]
    
def get_func_name(cursor, hash):
    cursor.execute(F"SELECT * FROM caller_table WHERE func_set_hash='{hash}'")
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    elif len(results) > 1:
        raise ValueError("Multiple rows found for the same callee")
    else:
        return results[0][-1]

    
def get_caller_names(cursor, callee_hash):
    cursor.execute(F"SELECT * FROM icall_target_table WHERE target_set_hash='{callee_hash}'")
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    else:
        return [result[2] for result in results]

def get_callee_hashs(cursor, caller_name):
    cursor.execute(F"SELECT * FROM icall_target_table WHERE caller_func='{caller_name}'")
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    else:
        return [result[-2] for result in results]


def get_callers(callee_name, cursor, level=0):
    """Recursively get the call trace, with indentation for each level."""
    # Write the callee at the current level
    output.append("    " * level + callee_name)  # Indentation for tree structure

    # Get the callee hash for the callee name
    callee_hash = get_hash(cursor, callee_name)
    if callee_hash is None:
        output.append(f"Call of '{callee_name}' not found")
        return

    caller_names = get_caller_names(cursor, callee_hash)

    # Recursively process each caller
    if caller_names:
        for caller_name in caller_names:
            get_callers(caller_name, cursor, level + 1)  # Increase indentation for the next level


def get_callees(cursor, func_name, level=0):
    """add all callees and their call chain recursively."""
    callee_hashs = get_callee_hashs(cursor, func_name)
    if callee_hashs is None:
        output.append(f"Callees of '{func_name}' not found")
        return
    for callee_hash in callee_hashs:
        callee_name = get_func_name(cursor, callee_hash)
        if callee_name:
            output.append("    " * level + callee_name)  # output.append the callee name with indentation
            # Recursively get callees for this callee
            get_callees(cursor, callee_name, level + 1)
        


def get_call_trace(callee_name):
    """Main function to initialize and start the call trace process."""
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="000",
        database="icall_data"
    )

    cursor = connection.cursor()
    
    # Start the recursive call trace
    get_callers(callee_name, cursor)
    get_callees(cursor, callee_name)

    cursor.close()
    connection.close()

    # Write the output to a file after the trace is completed
    write_output(output, output_path)


output = []
callee = "ieee80211_do_open"
callee_hash = ""
output_path = "/home/jamrot/TFA-project/test/output.txt"

# Example of usage
get_call_trace(callee)


