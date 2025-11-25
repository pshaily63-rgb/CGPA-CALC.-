# GPA / CGPA Calculator with simple file handling
# Student: Bhumi, Roll No. 14, VIT

RESULTS_FILE = "results.txt"

GRADE_MAP = {
    "A+": 10.0,
    "A": 9.0,
    "B+": 8.0,
    "B": 7.0,
    "C": 6.0,
    "D": 5.0,
    "F": 0.0
}


def read_semesters_from_file():
    semesters = []  # list of tuples: (sem_no(int), gpa(float), credits(float))
    try:
        with open(RESULTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    sem_no = int(parts[0])
                    gpa = float(parts[1])
                    credits = float(parts[2])
                    semesters.append((sem_no, gpa, credits))
    except FileNotFoundError:
        pass
    return semesters


def save_semester_to_file(sem_no, gpa, credits):
    with open(RESULTS_FILE, "a") as f:
        f.write(f"{sem_no},{gpa:.3f},{credits}\n")


def input_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Please enter a valid number.")


def get_grade_point_from_user(grade_input):
    grade_input = grade_input.strip().upper()
    if grade_input in GRADE_MAP:
        return GRADE_MAP[grade_input]
    try:
        # try parse as numeric grade point
        gp = float(grade_input)
        if 0.0 <= gp <= 10.0:
            return gp
    except ValueError:
        pass
    return None


def calculate_semester_gpa():
    print("\n--- Calculate Semester GPA ---")
    n = int(input("Enter number of subjects: ").strip())
    total_credits = 0.0
    total_points = 0.0

    for i in range(1, n + 1):
        print(f"Subject {i}:")
        credits = input_float("  Enter credit hours: ")
        while True:
            grade_in = input("  Enter grade (letter like A+/A/B+ or grade point 0-10): ")
            gp = get_grade_point_from_user(grade_in)
            if gp is None:
                print("  Invalid grade. Use A+, A, B+, B, C, D, F or numeric grade point.")
            else:
                break

        total_credits += credits
        total_points += credits * gp

    if total_credits == 0:
        print("No credits entered. Cannot compute GPA.")
        return None, None

    gpa = total_points / total_credits
    print(f"\nSemester GPA = {gpa:.3f} (Total Credits: {total_credits})")

    # save
    sems = read_semesters_from_file()
    next_sem_no = 1
    if sems:
        existing = [s[0] for s in sems]
        next_sem_no = max(existing) + 1

    save_semester_to_file(next_sem_no, gpa, total_credits)
    print(f"Semester {next_sem_no} saved to {RESULTS_FILE}.")
    return gpa, total_credits


def calculate_cgpa():
    print("\n--- Calculate CGPA ---")
    semesters = read_semesters_from_file()
    if not semesters:
        print("No saved semester data found.")
        choice = input("Do you want to enter previous semester GPAs manually? (y/n): ")
        if choice.strip().lower() != "y":
            return None
        semesters = []
        k = int(input("How many previous semesters do you want to enter? "))
        for i in range(k):
            gpa = input_float(f" Enter GPA for semester {i+1}: ")
            credits = input_float(f" Enter total credits for semester {i+1}: ")
            semesters.append((i+1, gpa, credits))

    total_credits = sum(s[2] for s in semesters)
    if total_credits == 0:
        print("Total credits are zero. Cannot compute CGPA.")
        return None

    weighted = sum(s[1] * s[2] for s in semesters)
    cgpa = weighted / total_credits
    print(f"\nCGPA calculated from {len(semesters)} semesters: {cgpa:.3f}")
    return cgpa


def view_saved_semesters():
    print("\n--- Saved Semester Results ---")
    semesters = read_semesters_from_file()
    if not semesters:
        print("No saved data.")
        return
    print("SemNo | GPA   | Credits")
    for sem_no, gpa, credits in semesters:
        print(f"{sem_no:5d} | {gpa:5.3f} | {credits}")


def main():
    while True:
        print("\n===== GPA / CGPA CALCULATOR =====")
        print("1. Calculate Semester GPA and save")
        print("2. Calculate CGPA from saved semesters")
        print("3. View saved semester results")
        print("4. Clear saved results")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            calculate_semester_gpa()
        elif choice == "2":
            calculate_cgpa()
        elif choice == "3":
            view_saved_semesters()
        elif choice == "4":
            confirm = input("Are you sure you want to clear all saved results? (y/n): ")
            if confirm.lower() == "y":
                open(RESULTS_FILE, "w").close()
                print("Saved results cleared.")
        elif choice == "5":
            print("Thank you. Exiting...")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()