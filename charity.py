import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import mysql.connector
from datetime import datetime
import decimal

class AuthenticationGUI:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title(" Charity Donation Tracker - Login")
        
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Prateeth123@',
            database='donate'
        )
        self.cursor = self.db_connection.cursor()

        self.create_tables()  # Create tables including donation_user
        self.create_widgets()

    def create_tables(self):
        # Create 'donation_user' table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS donation_user (
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        """)

        # Insert admin user if not exists
        self.cursor.execute("""
            INSERT IGNORE INTO donation_user (username, password) VALUES ('admin', 'adminpassword')
        """)
        self.db_connection.commit()

    def create_widgets(self):
        # Main frame
        self.main_frame = tk.Frame(self.parent, bg="#f0f0f0")
        self.main_frame.pack(expand=True, padx=250, pady=150)  # Adjusted padding to center the widgets

        # Title label
        self.title_label = tk.Label(self.main_frame, text="Charity Donation Tracker", font=("Arial", 24, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=(0, 20))

        # Username label and entry
        self.username_label = tk.Label(self.main_frame, text="Username:", font=("Arial", 14), bg="#f0f0f0")
        self.username_label.pack(anchor=tk.W)
        self.username_entry = tk.Entry(self.main_frame, font=("Arial", 14), width=30)
        self.username_entry.pack(pady=(0, 10))

        # Password label and entry
        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Arial", 14), bg="#f0f0f0")
        self.password_label.pack(anchor=tk.W)
        self.password_entry = tk.Entry(self.main_frame, font=("Arial", 14), width=30, show="*")
        self.password_entry.pack(pady=(0, 20))

        # Login button
        self.login_button = tk.Button(self.main_frame, text="Login", command=self.login, font=("Arial", 14), bg="#009688", fg="white", width=10)
        self.login_button.pack()

        # Status label
        self.status_label = tk.Label(self.main_frame, text="", font=("Arial", 12), fg="red", bg="#f0f0f0")
        self.status_label.pack()

    def login(self):
        # Define admin username and password
        admin_username = "admin"
        admin_password = "adminpassword"

        # Retrieve username and password from the entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == admin_username and password == admin_password:
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            self.open_donation_tracker()
        else:
            self.status_label.config(text="Invalid username or password.")

    def open_donation_tracker(self):
        self.parent.destroy()
        gui = DonationTrackerGUI()
        gui.run()

class DonationTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" Charity Donation Tracker")

        # Calculate window dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.97)
        window_height = int(screen_height * 0.97)
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set window geometry
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Set background color
        self.root.configure(bg="#f0f0f0")

        # Connect to MySQL database
        self.db_connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Prateeth123@',
            database='donate'
        )
        self.cursor = self.db_connection.cursor()

        # Create tables if they don't exist
        self.create_tables()

        # Fetch organizations from the database
        self.fetch_organizations()

        self.filter_variable = tk.StringVar()
        self.filter_variable.set(self.organizations[0])  # Set default filter option

        self.create_widgets()

    def fetch_organizations(self):
        try:
            self.cursor.execute("SELECT organization FROM organizations")
            result = self.cursor.fetchall()
            self.organizations = [row[0] for row in result]
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch organizations: {err}")
            self.organizations = []

    def create_tables(self):
        # Create 'donors' table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS donors (
                donor_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL  
            )
        """)

        # Create 'donations' table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS donations (
                donation_id INT AUTO_INCREMENT PRIMARY KEY,
                donor_id INT NOT NULL,
                organization VARCHAR(100) NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                donation_date DATETIME NOT NULL,
                FOREIGN KEY (donor_id) REFERENCES donors(donor_id)
            )
        """)

        # Create 'organizations' table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS organizations (
                organization_id INT AUTO_INCREMENT PRIMARY KEY,
                organization VARCHAR(100) NOT NULL  
            )
        """)

    def create_widgets(self):
        # Header
        self.header_frame = tk.Frame(self.root, bg="#009688", height=100)
        self.header_frame.pack(fill=tk.X)

        self.logo_label = tk.Label(self.header_frame, text="CHARITY DONATION TRACKER", font=("Arial", 30, "bold"), bg="#009688", fg="white")
        self.logo_label.pack(pady=10)

        # Donor name entry
        self.donor_name_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.donor_name_frame.pack(pady=20)
        self.donor_name_label = tk.Label(self.donor_name_frame, text="Donor Name:", font=("Arial", 16), bg="#f0f0f0")
        self.donor_name_label.pack(side=tk.LEFT, padx=10)
        self.donor_name_entry = tk.Entry(self.donor_name_frame, font=("Arial", 16), width=30)
        self.donor_name_entry.pack(side=tk.LEFT, padx=10)

        # Amount entry
        self.amount_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.amount_frame.pack(pady=10)
        self.amount_label = tk.Label(self.amount_frame, text="Amount (₹):", font=("Arial", 16), bg="#f0f0f0")
        self.amount_label.pack(side=tk.LEFT, padx=10)
        self.amount_entry = tk.Entry(self.amount_frame, font=("Arial", 16), width=15)
        self.amount_entry.pack(side=tk.LEFT, padx=10)

        # Organization selection
        self.org_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.org_frame.pack(pady=10)
        self.org_label = tk.Label(self.org_frame, text="Select Organization:", font=("Arial", 16), bg="#f0f0f0")
        self.org_label.pack(side=tk.LEFT, padx=10)
        self.org_combobox = ttk.Combobox(self.org_frame, values=self.organizations, font=("Arial", 16), width=27, textvariable=self.filter_variable)
        self.org_combobox.pack(side=tk.LEFT, padx=10)

        # Buttons
        self.button_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.button_frame.pack(pady=20)
        self.add_donor_button = tk.Button(self.button_frame, text="Add Donor", command=self.add_donor, font=("Arial", 16), bg="#009688", fg="white", width=12)
        self.add_donor_button.pack(side=tk.LEFT, padx=10)
        self.record_donation_button = tk.Button(self.button_frame, text="Record Donation", command=self.record_donation, font=("Arial", 16), bg="#FF5722", fg="white", width=15)
        self.record_donation_button.pack(side=tk.LEFT, padx=10)
        self.get_total_donated_button = tk.Button(self.button_frame, text="Get Total Donated", command=self.show_total_donated, font=("Arial", 16), bg="#673AB7", fg="white", width=17)
        self.get_total_donated_button.pack(side=tk.LEFT, padx=10)
        self.add_org_button = tk.Button(self.button_frame, text="Add Organization", command=self.add_organization, font=("Arial", 16), bg="#3F51B5", fg="white", width=15)
        self.add_org_button.pack(side=tk.LEFT, padx=10)
        self.remove_org_button = tk.Button(self.button_frame, text="Remove Organization", command=self.remove_organization, font=("Arial", 16), bg="#FF9800", fg="white", width=18)
        self.remove_org_button.pack(side=tk.LEFT, padx=10)
        self.update_org_button = tk.Button(self.button_frame, text="Update Organization", command=self.update_organization, font=("Arial", 16), bg="#4CAF50", fg="white", width=17)
        self.update_org_button.pack(side=tk.LEFT, padx=10)

        # Donation Summary Treeview
        self.donation_summary_tree = ttk.Treeview(self.root, columns=("Donor", "Organization", "Total Donated", "Number of Donations", "Date and Time"), show="headings")
        self.donation_summary_tree.heading("Donor", text="Donor", anchor=tk.CENTER)
        self.donation_summary_tree.heading("Organization", text="Organization", anchor=tk.CENTER)
        self.donation_summary_tree.heading("Total Donated", text="Total Donated", anchor=tk.CENTER)
        self.donation_summary_tree.heading("Number of Donations", text="Number of Donations", anchor=tk.CENTER)
        self.donation_summary_tree.heading("Date and Time", text="Date and Time", anchor=tk.CENTER)
        self.donation_summary_tree.pack(fill="both", expand=True)

    def add_donor(self):
        donor_name = self.donor_name_entry.get()
        if donor_name:
            try:
                # Check if the donor already exists
                self.cursor.execute("SELECT COUNT(*) FROM donors WHERE name = %s", (donor_name,))
                count = self.cursor.fetchone()[0]
                if count > 0:
                    messagebox.showinfo("Duplicate Donor", f"{donor_name} already exists as a donor.")
                else:
                    self.cursor.execute("INSERT INTO donors (name) VALUES (%s)", (donor_name,))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", f"{donor_name} has been added as a donor.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add donor: {err}")
        else:
            messagebox.showerror("Error", "Please enter a donor name.")

    def record_donation(self):
        donor_name = self.donor_name_entry.get()
        amount = self.amount_entry.get()
        organization = self.org_combobox.get()
        if donor_name and amount:
            try:
                now = datetime.now()
                donation_date = now.strftime("%Y-%m-%d %H:%M:%S")
                self.cursor.execute("SELECT donor_id FROM donors WHERE name = %s", (donor_name,))
                result = self.cursor.fetchone()
                if result:
                    donor_id = result[0]
                    # Convert amount to Decimal
                    amount_decimal = decimal.Decimal(amount)
                    self.cursor.execute("INSERT INTO donations (donor_id, organization, amount, donation_date) VALUES (%s, %s, %s, %s)", (donor_id, organization, amount_decimal, donation_date))
                    self.db_connection.commit()
                    messagebox.showinfo("Success", f"Donation of ₹{amount} recorded for {donor_name} to {organization}.")
                else:
                    messagebox.showerror("Error", f"Donor {donor_name} not found.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to record donation: {err}")
        else:
            messagebox.showerror("Error", "Please enter both donor name and amount.")

    def show_total_donated(self):
        try:
            filter_organization = self.filter_variable.get()  # Get the selected filter organization
            if filter_organization == "All Organizations":
                self.cursor.execute("""
                    SELECT donors.name, donations.organization, SUM(donations.amount), COUNT(donations.amount), MAX(donations.donation_date)
                    FROM donors 
                    LEFT JOIN donations ON donors.donor_id = donations.donor_id
                    GROUP BY donors.name, donations.organization
                """)
            else:
                self.cursor.execute("""
                    SELECT donors.name, donations.organization, SUM(donations.amount), COUNT(donations.amount), MAX(donations.donation_date)
                    FROM donors 
                    LEFT JOIN donations ON donors.donor_id = donations.donor_id
                    WHERE donations.organization = %s
                    GROUP BY donors.name, donations.organization
                """, (filter_organization,))
                
            donations = self.cursor.fetchall()
            if donations:
                # Clear existing treeview
                for child in self.donation_summary_tree.get_children():
                    self.donation_summary_tree.delete(child)

                # Insert new data into treeview
                for donation in donations:
                    self.donation_summary_tree.insert("", tk.END, values=donation)
            else:
                messagebox.showinfo("Donations Summary", "No donations found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to get donations: {err}")

    def add_organization(self):
        new_organization = simpledialog.askstring("Add Organization", "Enter the name of the new organization:")
        if new_organization:
            try:
                # Check if the organization already exists
                self.cursor.execute("SELECT COUNT(*) FROM organizations WHERE organization = %s", (new_organization,))
                count = self.cursor.fetchone()[0]
                if count > 0:
                    messagebox.showinfo("Duplicate Organization", f"{new_organization} already exists as an organization.")
                else:
                    self.cursor.execute("INSERT INTO organizations (organization) VALUES (%s)", (new_organization,))
                    self.db_connection.commit()
                    self.organizations.append(new_organization)
                    self.org_combobox['values'] = self.organizations
                    messagebox.showinfo("Success", f"{new_organization} has been added as an organization.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add organization: {err}")

    def remove_organization(self):
        organization_to_remove = self.org_combobox.get()
        if organization_to_remove != "All Organizations":
            confirmation = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove the organization '{organization_to_remove}'?")
            if confirmation:
                try:
                    self.cursor.execute("DELETE FROM organizations WHERE organization = %s", (organization_to_remove,))
                    self.db_connection.commit()
                    self.organizations.remove(organization_to_remove)
                    self.org_combobox['values'] = self.organizations
                    messagebox.showinfo("Success", f"{organization_to_remove} has been removed.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to remove organization: {err}")
        else:
            messagebox.showerror("Error", "Cannot remove 'All Organizations' option.")

    def update_organization(self):
        selected_organization = self.org_combobox.get()
        if selected_organization != "All Organizations":
            new_organization_name = simpledialog.askstring("Update Organization", "Enter the new name for the organization:", initialvalue=selected_organization)
            if new_organization_name:
                try:
                    self.cursor.execute("UPDATE organizations SET organization = %s WHERE organization = %s", (new_organization_name, selected_organization))
                    self.db_connection.commit()
                    index = self.organizations.index(selected_organization)
                    self.organizations[index] = new_organization_name
                    self.org_combobox['values'] = self.organizations
                    self.filter_variable.set(new_organization_name)
                    messagebox.showinfo("Success", f"Organization updated to {new_organization_name}.")
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Failed to update organization: {err}")
        else:
            messagebox.showerror("Error", "Cannot update 'All Organizations' option.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    auth_root = tk.Tk()
    authentication = AuthenticationGUI(auth_root)
    auth_root.mainloop()

