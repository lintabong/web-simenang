import os
import csv
import string
import secrets
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def generate_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def generate_unique_passwords(count, length):
    unique_passwords = set()

    while len(unique_passwords) < count:
        password = generate_password(length)
        unique_passwords.add(password)

    return list(unique_passwords)

def insert_dpt():
    for prefix in prefixs:
        with open(f'dpt/dpt_{prefix}.csv', 'r') as file_csv:
            csv_reader = csv.reader(file_csv)

            for i, row in enumerate(csv_reader):
                if i >= 1:
                    query = f"""INSERT INTO `dpt_{prefix}`(`name`, `gender`, `age`, `village`, 
                            `household`, `homeResidents`, `electionPlace`, `subdistrict`, `regency`) 
                            VALUES ('{row[1]}','{row[2]}',{row[3]},'{row[4]}',{row[5]},{row[6]},{row[7]},
                            '{row[8]}','{row[9]}')
                            """
                    cursor.execute(query)
                    conn.commit()

def create_table_kirka():
    pass

def create_table_user():
    pass

def insert_user():
    volunteer = []

    for prefix in prefixs:
        with open(f'dpt/dpt_{prefix}.csv', 'r') as file_csv:
            csv_reader = csv.reader(file_csv)

            for i, row in enumerate(csv_reader):
                if i >= 1:
                    user = f'{row[4].lower()}{row[7]}'
                    user = [user, row[4], row[7], row[8], row[9]]
                    if user not in volunteer:
                        volunteer.append(user)

        user_result = []
        for pre in ['str', 'rlwn']:
            for user in volunteer:
                user_result.append([f'{pre}-{user[0]}', user[1], user[2], user[3], user[4]])

    generated_passwords = generate_unique_passwords(len(user_result), 20)

    for i, password in enumerate(generated_passwords):
        query = f"""INSERT INTO `users`(`username`, `password`, `createdAt`, `role`, `village`, 
                `subdistrict`, `regency`, `electionPlace`, `status`) 
                VALUES ('{user_result[i][0]}','{password}',NOW(),'volunteer','{user_result[i][1]}','{user_result[i][3]}',
                '{user_result[i][4]}',{user_result[i][2]}, 'active')"""
        
        cursor.execute(query)
        conn.commit()

        print(f'{i}\t{user_result[i][0]}\t\t{password}')

if __name__ == '__main__':
    prefixs = ['jaten', 'kebakkramat', 'tasikmadu']

    conn = mysql.connector.connect(
        host=os.getenv('DATABASE_HOST'),
        port=os.getenv('DATABASE_PORT'),
        user=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASS'),
        database=os.getenv('DATABASE_NAME')
    )

    cursor = conn.cursor()

    # insert_user()
