import random
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
    """)
    # Create scores table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        username TEXT,
        subject TEXT,
        score INTEGER,
        FOREIGN KEY (username) REFERENCES users(username)
    )
    """)
    conn.commit()
    conn.close()

# User registration
def register():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    name = input("Enter a username: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (name,))
    if cursor.fetchone():
        print("User already exists!")
        conn.close()
        return False
    pwd = input("Enter a password: ")
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, pwd))
    conn.commit()
    conn.close()
    print("Registration successful!")
    return True

# User login
def login():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    name = input("Enter your username: ")
    pwd = input("Enter your password: ")
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (name, pwd))
    if cursor.fetchone():
        print("Login successful!")
        conn.close()
        return name
    print("Invalid username or password!")
    conn.close()
    return None

# Quiz functionality
def quiz(subject, user, quiz_data):
    print(f"\nStarting {subject} quiz!")
    score = 0
    questions = random.sample(quiz_data[subject], len(quiz_data[subject]))[:5]

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}: {q['q']}")
        for idx, option in enumerate(q['o'], 1):
            print(f"{idx}. {option}")
        try:
            ans = int(input("Your answer (1/2/3/4): "))
            if q['o'][ans - 1] == q['a']:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! The correct answer was: {q['a']}")
        except (ValueError, IndexError):
            print("Invalid input! Skipping this question.")

    print(f"\n{user}, your score is {score}/5.")
    save_score(user, subject, score)

# Save score to database
def save_score(username, subject, score):
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (username, subject, score) VALUES (?, ?, ?)", (username, subject, score))
    conn.commit()
    conn.close()

# Main function
def main():
    setup_database()
    print("Welcome to the Quiz Application!")
    user = None

    while not user:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            if register():
                continue
        elif choice == "2":
            user = login()
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice!")

    while True:
        print("\nSubjects:\n1. C++\n2. Python\n3. DSA")
        choice = input("Choose a subject (1-3): ")
        if choice == "1":
            quiz("C++", user, quiz_data)
        elif choice == "2":
            quiz("Python", user, quiz_data)
        elif choice == "3":
            quiz("DSA", user, quiz_data)
        else:
            print("Invalid choice!")
            continue

        play_again = input("Do you want to take another quiz? (yes/no): ").lower()
        if play_again != "yes":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
