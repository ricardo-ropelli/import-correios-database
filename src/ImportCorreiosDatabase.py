import os
import psycopg2


GENERAL_CONFIG = {
    'root_dir': './',
    'host': '',
    'database': '',
    'port': '',
    'user': '',
    'password': '',
    'commit_each': 25
}


FILE_TO_TABLE = {
    "LOG_BAIRRO.TXT": "endereco_bairro",
    "LOG_LOGRADOURO_": "endereco_logradouro"
}


def parse_file_information(file, line):
    if "LOG_LOGRADOURO_" in file:
        table_name = FILE_TO_TABLE['LOG_LOGRADOURO_']
    else:
        table_name = FILE_TO_TABLE[file]

    print("Parsing insert statement to table: '" + table_name + "'.")

    info_array = line.rstrip().split("@")
    normalized_info_array = ["'" + info.replace("'", "''") + "'" if info != '' else "null" for info in info_array]
    insert_values = ", ".join(normalized_info_array)

    insert_statement = "insert into " + table_name + " values(" + insert_values + ");"
    print("Parsed insert statement: " + insert_statement)

    return insert_statement


def read_all_file_lines_and_perform_insert(file, path, connection):
    print("Ready to read file: '" + file + "'.")
    opened_file = open(path, encoding="ISO-8859-1")

    cur = connection.cursor()

    commit_controller = 0
    for line in opened_file:
        print("Read line: '" + str(line.rstrip()) + "'.")
        cur.execute(parse_file_information(file, line))
        commit_controller = commit_controller + 1

        if commit_controller >= GENERAL_CONFIG['commit_each']:
            print("Executing commit...")
            connection.commit()
            commit_controller = 0


def read_all_file(connection):
    # r=root, d=directories, f = files
    for root, dirs, files in os.walk(GENERAL_CONFIG['root_dir']):
        for file in files:
            if '.txt' in file or '.TXT' in file:
                path = os.path.join(root, file)
                read_all_file_lines_and_perform_insert(file, path, connection)

    connection.close()


def establish_connection_to_database():
    print("Establishing connection to database: '" + GENERAL_CONFIG['database'] + "'.")
    connection = psycopg2.connect(
        host=GENERAL_CONFIG['host'],
        port=GENERAL_CONFIG['port'],
        database=GENERAL_CONFIG['database'],
        user=GENERAL_CONFIG['user'],
        password=GENERAL_CONFIG['password'])
    return connection


def main():
    connection = establish_connection_to_database()
    read_all_file(connection)


if __name__ == "__main__":
    print("----------------------------------------------------------------------------")
    print("Initialization of import Correios database: '" + GENERAL_CONFIG['root_dir'] + "'.")
    print("----------------------------------------------------------------------------")
    main()
