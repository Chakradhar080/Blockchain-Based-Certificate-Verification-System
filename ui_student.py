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

def log_verified_certificate(roll, name):
    with open("verified_log.txt", "a") as log:
        log.write(f"{roll},{name},{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

def launch_student_ui(username):
    blockchain = load_blockchain()
    root = tb.Window(themename="superhero")
    root.title("Student Panel - Certificate Verification")
    root.state('zoomed')

    sidebar = tb.Frame(root, width=300, padding=20, bootstyle="dark")
    sidebar.pack(side="left", fill="y")

    main_area = tb.Frame(root, padding=30)
    main_area.pack(side="right", expand=True, fill="both")

    text_area = tb.ScrolledText(main_area, font=("Courier", 14), height=30, width=100)
    text_area.pack(fill="both", expand=True, pady=10)

    tf_roll = tb.Entry(sidebar, font=("Courier", 16), width=25)
    tf_name = tb.Entry(sidebar, font=("Courier", 16), width=25)

    tb.Label(sidebar, text="Roll No:", font=("Courier", 16), bootstyle="inverse-dark").pack(pady=10)
    tf_roll.pack(pady=5)
    tb.Label(sidebar, text="Name:", font=("Courier", 16), bootstyle="inverse-dark").pack(pady=10)
    tf_name.pack(pady=5)

    def verify():
        text_area.delete('1.0', "end")
        roll = tf_roll.get().strip()
        name = tf_name.get().strip()
        file = askopenfilename()
        if not (roll and name and file):
            text_area.insert("end", "Warning: Please fill Roll No, Name and select a certificate file.\n")
            return

        with open(file, 'rb') as f:
            content = f.read()
        signature = sha256(content).hexdigest()

        for block in blockchain.chain:
            for txn in block.transactions:
                p = txn.split('#')
                if len(p) == 4 and p[0] == roll and p[1].lower() == name.lower() and p[3] == signature:
                    text_area.insert("end", "Success: Certificate Validation Successful.\n")
                    text_area.insert("end", "-"*80 + "\n")
                    text_area.insert("end", f"Block Number   : {block.index}\n")
                    text_area.insert("end", f"Timestamp      : {datetime.datetime.fromtimestamp(block.timestamp)}\n")
                    text_area.insert("end", f"Previous Hash  : {block.previous_hash}\n")
                    text_area.insert("end", f"Block Hash     : {block.hash}\n")
                    text_area.insert("end", f"Roll No        : {p[0]}\n")
                    text_area.insert("end", f"Name           : {p[1]}\n")
                    text_area.insert("end", f"Contact        : {p[2]}\n")
                    text_area.insert("end", f"Digital Signature:\n{p[3]}\n")
                    text_area.insert("end", "-"*80 + "\n")
                    log_verified_certificate(p[0], p[1])
                    return

        text_area.insert("end", "Error: Certificate Valiidation Failed.\n")

    def goBack():
        root.destroy()
        desktop_main.login_window()

    tb.Button(sidebar, text="Verify Certificate", command=verify, bootstyle="success", width=28, padding=10).pack(pady=20)
    tb.Button(sidebar, text="Go Back", command=goBack, bootstyle="danger", width=28, padding=10).pack(pady=30)

    root.mainloop()
