import pyodbc
import csv
import matplotlib.pyplot as plt

# 1. Establish database connection using standard windows authentication credentials
conn = pyodbc.connect('DRIVER={SQL Server};SERVER=KNOCKKNOCK01\\SQLEXPRESS;DATABASE=ExpenseDB;Trusted_Connection=yes;')
cursor = conn.cursor()

def check_budget_alert(spent, budget):
    """Feature 1: Dynamic Budget vs Expense Alert Calculation Engine"""
    print("\n----------------------------------------")
    print("             BUDGET ANALYSIS            ")
    print("----------------------------------------")
    print(f"Total Amount Spent This Month: INR {spent:.2f}")
    print(f"Allocated Monthly Budget Limit: INR {budget:.2f}")
    
    # Conditional branches to evaluate budget violation scenarios
    if spent > budget:
        over = spent - budget
        print(f"⚠️ CRITICAL: Budget limit breached by INR {over:.2f}!")
    elif spent >= (budget * 0.85):
        print("⚠️ WARNING: You have utilized over 85% of your allocated budget!")
    else:
        left = budget - spent
        print(f"✅ STATUS: Under budget limit. INR {left:.2f} remaining safe.")

def export_to_csv(user_id, month, year):
    """Feature 2: Analytical Data Extraction and Export Engine (CSV/Excel format)"""
    # SQL query to extract complete itemized log rows for validation checks
    cursor.execute("""
        SELECT Category, Amount, ExpenseDate 
        FROM GroupExpenses 
        WHERE UserID = ? AND MONTH(ExpenseDate) = ? AND YEAR(ExpenseDate) = ?
    """, (user_id, month, year))
    rows = cursor.fetchall()
    
    if not rows:
        print("❌ System Error: No matching operational transactions found to export!")
        return

    # Utilizing standard Python filesystem writing pipeline
    filename = f"User_{user_id}_Statement_M{month}_Y{year}.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Defining logical spreadsheet schema headers
        writer.writerow(["Expense Category", "Transaction Amount (INR)", "Date of Record"])
        # Linear tracking loop to commit rows down to structural format
        for row in rows:
            writer.writerow([row[0], float(row[1]), str(row[2])])
            
    print(f"📊 REPORT EXPORTED: File successfully created as '{filename}'!")

def show_history_graph(user_id):
    """Feature 3: Long-term Historical Chronological Trend Charts (Data Visualizer)"""
    # Triggering T-SQL Analytical Cluster Stored Procedure
    cursor.execute("{CALL GetUserHistory (?)}", (user_id,))
    history_data = cursor.fetchall()
    
    if not history_data:
        print("❌ Visualization Error: Insufficient aggregate history data for tracking graph!")
        return
        
    months_labels = []
    amounts_spent = []
    
    # Translating row structures into standard programmatic tracking arrays
    for row in history_data:
        label = f"Month {row[0]}/{row[1]}"
        months_labels.append(label)
        amounts_spent.append(float(row[2]))
      
        
    # Rendering interface parameters using standard Matplotlib lab layout
    plt.figure(figsize=(9, 5))
    plt.bar(months_labels, amounts_spent, color='royalblue', edgecolor='navy')
    plt.xlabel("Timeline Milestones (Month/Year)", fontsize=11)
    plt.ylabel("Total Consolidated Expenses (INR)", fontsize=11)
    plt.title("Long-term Historical Expenditure Analysis & Consumption Trend", fontsize=13)
    plt.grid(axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.show()

# ====================================================================
#              MAIN ENGINE RUNTIME EXECUTION FRAMEWORK
# ====================================================================
def view_database_audit_report():
    """Feature 4: Complete System Audit Engine to extract cross-tabulated user profiles and group expenses"""
    try:
        query = """
            SELECT 
                u.UserID, 
                u.UserName, 
                u.MonthlyBudget, 
                ISNULL(e.Category, 'NO EXPENSE RECORD') AS Category, 
                ISNULL(e.Amount, 0.0) AS Amount, 
                ISNULL(CONVERT(VARCHAR, e.ExpenseDate, 105), 'N/A') AS ExpenseDate
            FROM ProjectUsers u
            LEFT JOIN GroupExpenses e ON u.UserID = e.UserID
            ORDER BY u.UserID ASC, e.ExpenseDate DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        if not rows:
            print("\n[X] System Error: No matching user profiles found in database store!")
            return
            
        print("\n=========================================================================================================")
        print("                                  COMPLETE SYSTEM AUDIT & LEDGER REPORT                                  ")
        print("=========================================================================================================")
        print(f"{'UID':<4} | {'Workspace Profile Label':<25} | {'Budget (INR)':<13} | {'Expense Category':<20} | {'Amount (INR)':<12} | {'Date'}")
        print("-" * 105)
        
        for row in rows:
            uid = str(row[0])
            name = str(row[1])
            budget = f"{float(row[2]):.2f}"
            category = str(row[3])
            amount = f"INR {float(row[4]):.2f}" if float(row[4]) > 0 else "N/A"
            dt = str(row[5])
            
            print(f"{uid:<4} | {name:<25} | {budget:<13} | {category:<20} | {amount:<12} | {dt}")
        print("=========================================================================================================")
        
    except Exception as e:
        print(f"\n[X] Pipeline Failure: Critical breakdown during database audit compilation -> {e}")
while True:
    print("\n==================================================")
    print("      HYBRID WORKSPACE EXPENSE TRACKER ENGINE     ")
    print("==================================================")
    print("1. Register New Workspace Account (Single/Group Profiles)")
    print("2. Commit Fresh Expense Transaction Entry")
    print("3. Execute Monthly Budget Verification (Stored Procedure)")
    print("4. Generate Extracted Spreadsheet Accounts (Excel/CSV Export)")
    print("5. Launch Timeline Analytical Bar Chart (Visual Insights)")
    print("6. Delete a Specific Expense Record")
    print("7. Delete a User / Group Workspace Profile")
    print("8. View Complete Database Audit Report (Cross-Tabulated Ledger)")
    print("9. Terminate Operational System Application")
    print("====================================================")
        
    choice = input("\nSelect system execution parameter (1-9): ")

    
    if choice == '1':
        name = input("Enter operational profile / group label: ")
        budget = float(input("Configure active monthly budget benchmark (INR): "))
        
        cursor.execute("INSERT INTO ProjectUsers (UserName, MonthlyBudget) VALUES (?, ?)", (name, budget))
        conn.commit()
        print(f"✅ Accounts Registry updated. Workspace '{name}' is active.")
        
    elif choice == '2':
        # Prompt live users from current memory lookup blocks
        cursor.execute("SELECT UserID, UserName FROM ProjectUsers")
        users = cursor.fetchall()
        print("\n--- Currently Active System Accounts ---")
        for u in users:
            print(f"System ID: {u[0]} | Target Label: {u[1]}")
            
        uid = int(input("\nEnter specific target User ID mapping: "))
        cat = input("Enter expense group target classification (e.g., Rent, Food): ")
        amt = float(input("Enter transactional value (INR): "))
        dt = input("Enter date calendar alignment (YYYY-MM-DD format): ")
        
        cursor.execute("INSERT INTO GroupExpenses (UserID, Category, Amount, ExpenseDate) VALUES (?, ?, ?, ?)", (uid, cat, amt, dt))
        conn.commit()
        print("✅ Entry saved. Transaction database pipelines updated successfully.")
        
    elif choice == '3':
        uid = int(input("Enter query target Account ID: "))
        m = int(input("Enter processing tracking month (1-12): "))
        y = int(input("Enter calendar processing target year: "))
        
        # Dispatching execution frame to core T-SQL Stored Procedure 1
        cursor.execute("{CALL GetUserMonthlyStatus (?, ?, ?)}", (uid, m, y))
        result = cursor.fetchone()
        
        if result and result is not None:
            user_name = result[0]
            user_budget = float(result[1])
            total_spent = float(result[2])
            
            print(f"\nTarget Workspace Profile: {user_name}")
            # Transfer execution data stack to verification module
            check_budget_alert(total_spent, user_budget)
        else:
            print("❌ Query Failure: Target record data parameters unavailable in database store!")
            
    elif choice == '4':
        uid = int(input("Enter extraction profile ID parameter: "))
        m = int(input("Enter specific database tracking calendar month: "))
        y = int(input("Enter extraction processing baseline year: "))
        export_to_csv(uid, m, y)
        
    elif choice == '5':
        uid = int(input("Enter profiling data target ID for graphical modeling: "))
        show_history_graph(uid)
        
    elif choice == '6':
        print("\n--- Delete an Expense Record ---")
        uid = int(input("Enter User ID to view transactions: "))
        
                # Display current transactions for that user so they can pick which one to delete
        cursor.execute("SELECT ExpenseID, Category, Amount, ExpenseDate FROM GroupExpenses WHERE UserID = ?", (uid,))
        records = cursor.fetchall()
        
        if not records:
            print("❌ No expense records found for this user.")
        else:
            print("\nAvailable Records:")
            for r in records:
                print(f"Expense ID: {r[0]} | Category: {r[1]} | Amount: INR {r[2]} | Date: {r[3]}")
                
            id_to_delete = int(input("\nEnter the Expense ID you want to permanently delete: "))
            
            cursor.execute("DELETE FROM GroupExpenses WHERE ExpenseID = ?", (id_to_delete,))
            conn.commit()
            print("✅ Success: Expense record deleted successfully from database.")

    elif choice == '7':
        print("\n--- Delete a User/Group Workspace ---")
        cursor.execute("SELECT UserID, UserName FROM ProjectUsers")
        users = cursor.fetchall()
        
        print("\nActive System Accounts:")
        for u in users:
            print(f"User ID: {u[0]} | Profile Label: {u[1]}")
            
        uid_to_delete = int(input("\nEnter the User ID to delete permanently (This will clear all their expenses too): "))
        
        # Confirm once before deleting
        confirm = input(f"Are you sure you want to delete User ID {uid_to_delete}? (yes/no): ")
        if confirm.lower() == 'yes':
            cursor.execute("DELETE FROM ProjectUsers WHERE UserID = ?", (uid_to_delete,))
            conn.commit()
            print("✅ Success: Workspace profile and all associated data wiped successfully.")
        else:
            print("❌ Operation cancelled.")
    elif choice == '8':
            view_database_audit_report()

    elif choice == '9':
            print("\nClosing terminal connection frame. Safe shutdown successful!")
            conn.close()
            break
    else:
            print("\n[X] Selection Fault: Out of bounds option specified. Enter choices 1 through 9.")
