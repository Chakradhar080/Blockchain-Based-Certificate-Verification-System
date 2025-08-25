import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter.filedialog import askopenfilename
from Blockchain import Blockchain
from hashlib import sha256
import os
import desktop_main
import datetime

def load_blockchain():
    if os.path.exists('blockchain_contract.txt'):
        return Blockchain.load_object('blockchain_contract.txt')
    return Blockchain()

def launch_admin_ui():
    blockchain = load_blockchain()
    root = tb.Window(themename="superhero")
    root.title("Admin Panel")
    root.state('zoomed')

    sidebar = tb.Frame(root, width=300, padding=20, bootstyle="dark")
    sidebar.pack(side="left", fill="y")

    main_area = tb.Frame(root, padding=30)
    main_area.pack(side="right", expand=True, fill="both")

    text_area = tb.ScrolledText(main_area, font=("Courier", 14), height=30, width=100)
    text_area.pack(fill="both", expand=True, pady=10)

    tf_roll = tb.Entry(sidebar, font=("Courier", 16), width=25)
    tf_name = tb.Entry(sidebar, font=("Courier", 16), width=25)
    tf_contact = tb.Entry(sidebar, font=("Courier", 16), width=25)

    tb.Label(sidebar, text="Roll No:", font=("Courier", 16), bootstyle="inverse-dark").pack(pady=10)
    tf_roll.pack(pady=5)
    tb.Label(sidebar, text="Name:", font=("Courier", 16), bootstyle="inverse-dark").pack(pady=10)
    tf_name.pack(pady=5)
    tb.Label(sidebar, text="Contact No:", font=("Courier", 16), bootstyle="inverse-dark").pack(pady=10)
    tf_contact.pack(pady=5)

    def saveCertificate():
        text_area.delete('1.0', "end")
        file = askopenfilename()
        if not file:
            text_area.insert("end", "Warning: No certificate file selected.\n")
            return

        roll = tf_roll.get().strip()
        name = tf_name.get().strip()
        contact = tf_contact.get().strip()

        if not roll or not name or not contact:
            text_area.insert("end", "Warning: Please fill all fields.\n")
            return

        with open(file, 'rb') as f:
            content = f.read()
        signature = sha256(content).hexdigest()
        new_data = f"{roll}#{name}#{contact}#{signature}"

        for block in blockchain.chain:
            for txn in block.transactions:
                parts = txn.split('#')
                if len(parts) == 4 and parts[0] == roll and parts[1].lower() == name.lower() and parts[2] == contact:
                    text_area.insert("end", "Warning: Certificate already exists.\n")
                    return

        blockchain.add_new_transaction(new_data)
        block = blockchain.mine()
        blockchain.save_object('blockchain_contract.txt')

        if block:
            text_area.insert("end", "Success: Certificate Uploaded Successfully.\n")
            text_area.insert("end", "-"*80 + "\n")
            text_area.insert("end", f"Block Number: {block.index}\n")
            text_area.insert("end", f"Timestamp: {datetime.datetime.fromtimestamp(block.timestamp)}\n")
            text_area.insert("end", f"Previous Hash: {block.previous_hash}\n")
            text_area.insert("end", f"Block Hash: {block.hash}\n")
            text_area.insert("end", "Transactions:\n")
            for txn in block.transactions:
                p = txn.split('#')
                if len(p) == 4:
                    text_area.insert("end", f"  Roll No: {p[0]}\n")
                    text_area.insert("end", f"  Name: {p[1]}\n")
                    text_area.insert("end", f"  Contact: {p[2]}\n")
                    text_area.insert("end", f"  Digital Signature: {p[3]}\n")
                    text_area.insert("end", "-"*40 + "\n")
            text_area.insert("end", "-"*80 + "\n")
        else:
            text_area.insert("end", "Error: No transaction to mine.\n")

    def showUploadedCertificates():
        text_area.delete('1.0', "end")

        # Reload fresh blockchain
        current_blockchain = load_blockchain()

        total = 0
        for block in current_blockchain.chain:
            if block.index == 0:
                continue
            total += len(block.transactions)

        if total == 0:
            text_area.insert("end", "Warning: No certificates uploaded yet.\n")
            return

        text_area.insert("end", f"Total Uploaded Certificates: {total}\n")
        text_area.insert("end", "="*80 + "\n\n")

        for block in current_blockchain.chain:
            if block.index == 0:
                continue
            text_area.insert("end", f"Block Number: {block.index}\n")
            text_area.insert("end", f"Timestamp: {datetime.datetime.fromtimestamp(block.timestamp)}\n")
            text_area.insert("end", f"Previous Hash: {block.previous_hash}\n")
            text_area.insert("end", f"Block Hash: {block.hash}\n")
            text_area.insert("end", "Transactions:\n")
            for txn in block.transactions:
                p = txn.split('#')
                if len(p) == 4:
                    text_area.insert("end", f"  Roll No: {p[0]}\n")
                    text_area.insert("end", f"  Name: {p[1]}\n")
                    text_area.insert("end", f"  Contact: {p[2]}\n")
                    text_area.insert("end", f"  Digital Signature: {p[3]}\n")
                    text_area.insert("end", "-"*40 + "\n")
            text_area.insert("end", "="*80 + "\n\n")

    def goBack():
        root.destroy()
        desktop_main.login_window()

    tb.Button(sidebar, text="Upload Certificate", command=saveCertificate, bootstyle="success", width=28, padding=10).pack(pady=20)
    tb.Button(sidebar, text="Show Certificates", command=showUploadedCertificates, bootstyle="info", width=28, padding=10).pack(pady=20)
    tb.Button(sidebar, text="Go Back", command=goBack, bootstyle="danger", width=28, padding=10).pack(pady=30)

    root.mainloop()
