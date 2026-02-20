import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import mysql.connector

# ─────────────────────────────────────────────
#  DB CONNECTION
# ─────────────────────────────────────────────
DB_CONFIG = dict(user="root", host="localhost", passwd="1234", database="Library")

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ─────────────────────────────────────────────
#  THEME / PALETTE
# ─────────────────────────────────────────────
BG        = "#0f1117"
PANEL     = "#1a1d27"
CARD      = "#22263a"
ACCENT    = "#f5a623"
ACCENT2   = "#e05c5c"
TEXT      = "#e8eaf0"
MUTED     = "#6b7280"
SUCCESS   = "#4ade80"
BORDER    = "#2e3347"

FONT_HEAD = ("Georgia", 22, "bold")
FONT_SUB  = ("Georgia", 13, "italic")
FONT_LABEL= ("Courier New", 10, "bold")
FONT_BODY = ("Courier New", 10)
FONT_BTN  = ("Courier New", 11, "bold")
FONT_TITLE= ("Georgia", 14, "bold")


# ─────────────────────────────────────────────
#  REUSABLE WIDGETS
# ─────────────────────────────────────────────
def styled_frame(parent, bg=PANEL, **kw):
    return tk.Frame(parent, bg=bg, **kw)

def styled_label(parent, text, font=FONT_BODY, fg=TEXT, bg=PANEL, **kw):
    return tk.Label(parent, text=text, font=font, fg=fg, bg=bg, **kw)

def styled_entry(parent, width=28, **kw):
    e = tk.Entry(parent, width=width, font=FONT_BODY,
                 bg=CARD, fg=TEXT, insertbackground=ACCENT,
                 relief="flat", highlightthickness=1,
                 highlightbackground=BORDER, highlightcolor=ACCENT, **kw)
    return e

def styled_button(parent, text, command, color=ACCENT, fg="#0f1117", width=18):
    return tk.Button(parent, text=text, command=command,
                     font=FONT_BTN, bg=color, fg=fg,
                     relief="flat", cursor="hand2",
                     activebackground=TEXT, activeforeground="#0f1117",
                     padx=10, pady=6, width=width)

def section_title(parent, text, bg=PANEL):
    f = styled_frame(parent, bg=bg)
    f.pack(fill="x", padx=20, pady=(18, 4))
    tk.Label(f, text="▌ " + text, font=FONT_TITLE, fg=ACCENT, bg=bg).pack(side="left")
    tk.Frame(f, bg=BORDER, height=1).pack(side="left", fill="x", expand=True, padx=10, pady=10)
    return f


# ─────────────────────────────────────────────
#  FORM BUILDER HELPER
# ─────────────────────────────────────────────
def build_form(parent, fields, bg=PANEL):
    """Returns dict of {field_name: Entry widget}"""
    entries = {}
    for label, key in fields:
        row = styled_frame(parent, bg=bg)
        row.pack(fill="x", padx=30, pady=4)
        styled_label(row, f"{label}:", font=FONT_LABEL, fg=MUTED, bg=bg,
                     width=22, anchor="w").pack(side="left")
        e = styled_entry(row, width=32)
        e.pack(side="left", padx=(6, 0))
        entries[key] = e
    return entries


# ─────────────────────────────────────────────
#  TOAST NOTIFICATION
# ─────────────────────────────────────────────
def toast(root, message, color=SUCCESS):
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(bg=color)
    tk.Label(win, text=f"  {message}  ", font=FONT_BTN,
             bg=color, fg="#0f1117", pady=10, padx=16).pack()
    # Position bottom-right
    root.update_idletasks()
    x = root.winfo_x() + root.winfo_width() - 340
    y = root.winfo_y() + root.winfo_height() - 80
    win.geometry(f"+{x}+{y}")
    win.after(2400, win.destroy)


# ─────────────────────────────────────────────
#  RESULTS TABLE
# ─────────────────────────────────────────────
def build_table(parent, columns, bg=PANEL):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Custom.Treeview",
                    background=CARD, foreground=TEXT,
                    rowheight=28, fieldbackground=CARD,
                    borderwidth=0, font=FONT_BODY)
    style.configure("Custom.Treeview.Heading",
                    background=BORDER, foreground=ACCENT,
                    relief="flat", font=FONT_LABEL)
    style.map("Custom.Treeview",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#0f1117")])

    frame = styled_frame(parent, bg=bg)
    frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree = ttk.Treeview(frame, columns=columns, show="headings",
                        style="Custom.Treeview", height=10)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=max(100, len(col)*12))

    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return tree


# ═══════════════════════════════════════════════════════════════════
#   BOOK MANAGEMENT TAB
# ═══════════════════════════════════════════════════════════════════
class BookTab(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg=PANEL)
        self.root = root
        self._build()

    def _build(self):
        # ── ADD BOOK ─────────────────────────
        section_title(self, "Add New Book", bg=PANEL)
        fields = [
            ("Book Code",        "bno"),
            ("Book Name",        "bname"),
            ("Author",           "auth"),
            ("Price (₹)",        "price"),
            ("Publisher",        "publ"),
            ("Quantity",         "qty"),
            ("Purchase Date (YYYY-MM-DD)", "dop"),
        ]
        self.add_entries = build_form(self, fields)
        row = styled_frame(self, bg=PANEL)
        row.pack(pady=8)
        styled_button(row, "➕  Add Book", self.add_book).pack(side="left", padx=6)
        styled_button(row, "🗑  Delete Book", self.delete_book, color=ACCENT2, fg=TEXT).pack(side="left", padx=6)

        # ── SEARCH / UPDATE ───────────────────
        section_title(self, "Search / Update Book", bg=PANEL)
        srow = styled_frame(self, bg=PANEL)
        srow.pack(fill="x", padx=30, pady=4)
        styled_label(srow, "Book Code:", font=FONT_LABEL, fg=MUTED, bg=PANEL, width=22, anchor="w").pack(side="left")
        self.search_entry = styled_entry(srow, width=20)
        self.search_entry.pack(side="left", padx=6)
        styled_button(srow, "🔍  Search", self.search_book, width=12).pack(side="left", padx=4)
        styled_button(srow, "✏️  Update", self.update_book, color="#6366f1", fg=TEXT, width=12).pack(side="left", padx=4)

        # ── RESULTS TABLE ─────────────────────
        section_title(self, "Results", bg=PANEL)
        cols = ("Code", "Name", "Author", "Price", "Publisher", "Qty", "Date")
        self.tree = build_table(self, cols)

    # ─── CRUD ───────────────────────────────
    def _form_values(self):
        e = self.add_entries
        return (
            e["bno"].get().strip(),
            e["bname"].get().strip(),
            e["auth"].get().strip(),
            e["price"].get().strip(),
            e["publ"].get().strip(),
            e["qty"].get().strip(),
            e["dop"].get().strip(),
        )

    def _clear_form(self):
        for e in self.add_entries.values():
            e.delete(0, "end")

    def add_book(self):
        bno, bname, auth, price, publ, qty, dop = self._form_values()
        if not all([bno, bname, auth, price, publ, qty, dop]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute(
                "INSERT INTO BOOKRECORDS VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (bno, bname, auth, price, publ, qty, dop)
            )
            cnx.commit(); cur.close(); cnx.close()
            toast(self.root, "✔ Book added successfully!")
            self._clear_form()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def delete_book(self):
        bno = self.add_entries["bno"].get().strip()
        if not bno:
            messagebox.showwarning("Missing", "Enter Book Code to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete book {bno}?"):
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("DELETE FROM bookrecords WHERE bno=%s", (bno,))
            cnx.commit()
            toast(self.root, f"✔ {cur.rowcount} book(s) deleted.", color=ACCENT2)
            cur.close(); cnx.close()
            self._clear_form()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def search_book(self):
        bno = self.search_entry.get().strip()
        if not bno:
            messagebox.showwarning("Missing", "Enter a Book Code to search.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("SELECT * FROM bookrecords WHERE bno=%s", (bno,))
            rows = cur.fetchall(); cur.close(); cnx.close()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
            if not rows:
                toast(self.root, "No records found.", color=MUTED)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def update_book(self):
        bno = self.search_entry.get().strip()
        _, bname, auth, price, publ, qty, dop = self._form_values()
        if not all([bno, bname, auth, price, publ, qty, dop]):
            messagebox.showwarning("Missing", "Enter Book Code in search box and fill all fields.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute(
                "UPDATE bookrecords SET bname=%s,auth=%s,price=%s,publ=%s,qty=%s,date_of_purchase=%s WHERE bno=%s",
                (bname, auth, price, publ, qty, dop, bno)
            )
            cnx.commit()
            toast(self.root, f"✔ {cur.rowcount} book(s) updated!")
            cur.close(); cnx.close()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))


# ═══════════════════════════════════════════════════════════════════
#   MEMBER MANAGEMENT TAB
# ═══════════════════════════════════════════════════════════════════
class MemberTab(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg=PANEL)
        self.root = root
        self._build()

    def _build(self):
        section_title(self, "Add New Member", bg=PANEL)
        fields = [
            ("Member Code",              "mno"),
            ("Member Name",              "mname"),
            ("Membership Date (YYYY-MM-DD)", "dom"),
            ("Address",                  "addr"),
            ("Mobile Number",            "mob"),
        ]
        self.add_entries = build_form(self, fields)
        row = styled_frame(self, bg=PANEL)
        row.pack(pady=8)
        styled_button(row, "➕  Add Member", self.add_member).pack(side="left", padx=6)
        styled_button(row, "🗑  Delete Member", self.delete_member, color=ACCENT2, fg=TEXT).pack(side="left", padx=6)

        section_title(self, "Search / Update Member", bg=PANEL)
        srow = styled_frame(self, bg=PANEL)
        srow.pack(fill="x", padx=30, pady=4)
        styled_label(srow, "Member Code:", font=FONT_LABEL, fg=MUTED, bg=PANEL, width=22, anchor="w").pack(side="left")
        self.search_entry = styled_entry(srow, width=20)
        self.search_entry.pack(side="left", padx=6)
        styled_button(srow, "🔍  Search", self.search_member, width=12).pack(side="left", padx=4)
        styled_button(srow, "✏️  Update", self.update_member, color="#6366f1", fg=TEXT, width=12).pack(side="left", padx=4)

        section_title(self, "Results", bg=PANEL)
        cols = ("Code", "Name", "Membership Date", "Address", "Mobile")
        self.tree = build_table(self, cols)

    def _form_values(self):
        e = self.add_entries
        return (e["mno"].get().strip(), e["mname"].get().strip(),
                e["dom"].get().strip(), e["addr"].get().strip(),
                e["mob"].get().strip())

    def _clear_form(self):
        for e in self.add_entries.values():
            e.delete(0, "end")

    def add_member(self):
        mno, mname, dom, addr, mob = self._form_values()
        if not all([mno, mname, dom, addr, mob]):
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("INSERT INTO MEMBER VALUES (%s,%s,%s,%s,%s)",
                        (mno, mname, dom, addr, mob))
            cnx.commit(); cur.close(); cnx.close()
            toast(self.root, "✔ Member added successfully!")
            self._clear_form()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def delete_member(self):
        mno = self.add_entries["mno"].get().strip()
        if not mno:
            messagebox.showwarning("Missing", "Enter Member Code to delete.")
            return
        if not messagebox.askyesno("Confirm", f"Delete member {mno}?"):
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("DELETE FROM member WHERE mno=%s", (mno,))
            cnx.commit()
            toast(self.root, f"✔ {cur.rowcount} member(s) deleted.", color=ACCENT2)
            cur.close(); cnx.close()
            self._clear_form()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def search_member(self):
        mno = self.search_entry.get().strip()
        if not mno:
            messagebox.showwarning("Missing", "Enter a Member Code to search.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("SELECT * FROM member WHERE mno=%s", (mno,))
            rows = cur.fetchall(); cur.close(); cnx.close()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
            if not rows:
                toast(self.root, "No records found.", color=MUTED)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def update_member(self):
        mno = self.search_entry.get().strip()
        _, mname, dom, addr, mob = self._form_values()
        if not all([mno, mname, dom, addr, mob]):
            messagebox.showwarning("Missing", "Enter Member Code in search box and fill all fields.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute(
                "UPDATE member SET mname=%s,date_of_membership=%s,addr=%s,mob=%s WHERE mno=%s",
                (mname, dom, addr, mob, mno)
            )
            cnx.commit()
            toast(self.root, f"✔ {cur.rowcount} member(s) updated!")
            cur.close(); cnx.close()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))


# ═══════════════════════════════════════════════════════════════════
#   ISSUE / RETURN TAB
# ═══════════════════════════════════════════════════════════════════
class IssueTab(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg=PANEL)
        self.root = root
        self._build()

    def _build(self):
        # ── ISSUE ─────────────────────────────
        section_title(self, "Issue a Book", bg=PANEL)
        issue_fields = [
            ("Book Code",                   "bno"),
            ("Member Code",                 "mno"),
            ("Issue Date (YYYY-MM-DD)",     "doi"),
        ]
        self.issue_entries = build_form(self, issue_fields)
        row = styled_frame(self, bg=PANEL)
        row.pack(pady=6)
        styled_button(row, "📤  Issue Book", self.issue_book).pack(side="left", padx=6)

        # ── RETURN ────────────────────────────
        section_title(self, "Return a Book", bg=PANEL)
        ret_fields = [
            ("Book Code",   "bno_r"),
            ("Member Code", "mno_r"),
        ]
        self.return_entries = build_form(self, ret_fields)
        row2 = styled_frame(self, bg=PANEL)
        row2.pack(pady=6)
        styled_button(row2, "📥  Return Book", self.return_book, color=SUCCESS, fg="#0f1117").pack(side="left", padx=6)

        # ── SEARCH ────────────────────────────
        section_title(self, "Search Issues by Member", bg=PANEL)
        srow = styled_frame(self, bg=PANEL)
        srow.pack(fill="x", padx=30, pady=4)
        styled_label(srow, "Member Code:", font=FONT_LABEL, fg=MUTED, bg=PANEL, width=22, anchor="w").pack(side="left")
        self.search_entry = styled_entry(srow, width=20)
        self.search_entry.pack(side="left", padx=6)
        styled_button(srow, "🔍  Search", self.search_issue, width=12).pack(side="left", padx=4)

        section_title(self, "Results", bg=PANEL)
        cols = ("Book Code", "Member Code", "Issue Date", "Return Date")
        self.tree = build_table(self, cols)

    def issue_book(self):
        bno = self.issue_entries["bno"].get().strip()
        mno = self.issue_entries["mno"].get().strip()
        doi = self.issue_entries["doi"].get().strip()
        if not all([bno, mno, doi]):
            messagebox.showwarning("Missing", "Fill in all fields.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("INSERT INTO ISSUE(bno,mno,d_o_issue) VALUES(%s,%s,%s)",
                        (bno, mno, doi))
            cnx.commit(); cur.close(); cnx.close()
            toast(self.root, "✔ Book issued successfully!")
            for e in self.issue_entries.values():
                e.delete(0, "end")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def return_book(self):
        bno = self.return_entries["bno_r"].get().strip()
        mno = self.return_entries["mno_r"].get().strip()
        if not all([bno, mno]):
            messagebox.showwarning("Missing", "Enter Book Code and Member Code.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            rd = str(date.today())
            cur.execute(
                "UPDATE issue SET d_o_ret=%s WHERE bno=%s AND mno=%s AND d_o_ret IS NULL",
                (rd, bno, mno)
            )
            cnx.commit()
            if cur.rowcount == 0:
                toast(self.root, "No matching active issue found.", color=ACCENT2)
            else:
                toast(self.root, f"✔ Book returned on {rd}!", color=SUCCESS)
            cur.close(); cnx.close()
            for e in self.return_entries.values():
                e.delete(0, "end")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def search_issue(self):
        mno = self.search_entry.get().strip()
        if not mno:
            messagebox.showwarning("Missing", "Enter a Member Code.")
            return
        try:
            cnx = get_connection(); cur = cnx.cursor()
            cur.execute("SELECT * FROM issue WHERE mno=%s", (mno,))
            rows = cur.fetchall(); cur.close(); cnx.close()
            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)
            if not rows:
                toast(self.root, "No records found.", color=MUTED)
        except Exception as ex:
            messagebox.showerror("Error", str(ex))


# ═══════════════════════════════════════════════════════════════════
#   DASHBOARD TAB
# ═══════════════════════════════════════════════════════════════════
class DashboardTab(tk.Frame):
    def __init__(self, parent, root):
        super().__init__(parent, bg=PANEL)
        self.root = root
        self._build()

    def _build(self):
        # Header
        header = styled_frame(self, bg=PANEL)
        header.pack(fill="x", padx=30, pady=(28, 6))
        styled_label(header, "Library at a Glance", font=FONT_HEAD, fg=ACCENT, bg=PANEL).pack(anchor="w")
        styled_label(header, f"Today — {date.today().strftime('%A, %d %B %Y')}",
                     font=FONT_SUB, fg=MUTED, bg=PANEL).pack(anchor="w")

        # Stats row
        stats_row = styled_frame(self, bg=PANEL)
        stats_row.pack(fill="x", padx=30, pady=16)
        self.stat_frames = {}
        for key, label, color in [
            ("books",    "Total Books",       ACCENT),
            ("members",  "Total Members",     "#60a5fa"),
            ("issued",   "Currently Issued",  ACCENT2),
            ("returned", "Returned Today",    SUCCESS),
        ]:
            card = tk.Frame(stats_row, bg=CARD, padx=20, pady=16,
                            highlightthickness=1, highlightbackground=color)
            card.pack(side="left", expand=True, fill="both", padx=8)
            tk.Label(card, text="—", font=("Georgia", 28, "bold"),
                     fg=color, bg=CARD).pack()
            tk.Label(card, text=label, font=FONT_LABEL,
                     fg=MUTED, bg=CARD).pack()
            self.stat_frames[key] = card.winfo_children()[0]  # the number label

        # Recent activity table
        section_title(self, "Recent Issues", bg=PANEL)
        cols = ("Book Code", "Member Code", "Issue Date", "Return Date")
        self.tree = build_table(self, cols)

        # Refresh button
        btn_row = styled_frame(self, bg=PANEL)
        btn_row.pack(pady=8)
        styled_button(btn_row, "🔄  Refresh Dashboard", self.refresh, width=22).pack()

        self.refresh()

    def refresh(self):
        try:
            cnx = get_connection(); cur = cnx.cursor()

            cur.execute("SELECT COUNT(*) FROM bookrecords")
            books = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM member")
            members = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM issue WHERE d_o_ret IS NULL")
            issued = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM issue WHERE d_o_ret=%s", (str(date.today()),))
            returned = cur.fetchone()[0]

            cur.execute("SELECT * FROM issue ORDER BY d_o_issue DESC LIMIT 20")
            rows = cur.fetchall()
            cur.close(); cnx.close()

            labels = [books, members, issued, returned]
            for lbl, val in zip(self.stat_frames.values(), labels):
                lbl.config(text=str(val))

            self.tree.delete(*self.tree.get_children())
            for r in rows:
                self.tree.insert("", "end", values=r)

        except Exception as ex:
            messagebox.showerror("DB Error", str(ex))


# ═══════════════════════════════════════════════════════════════════
#   MAIN APP
# ═══════════════════════════════════════════════════════════════════
class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("1100x780")
        self.minsize(900, 640)
        self.configure(bg=BG)
        self._build_ui()

    def _build_ui(self):
        # ── SIDEBAR ──────────────────────────────────────────────
        sidebar = tk.Frame(self, bg=BG, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(sidebar, bg=BG)
        logo_frame.pack(fill="x", pady=(28, 30), padx=16)
        tk.Label(logo_frame, text="📚", font=("", 32), bg=BG).pack()
        tk.Label(logo_frame, text="LIBRARY", font=("Georgia", 13, "bold"),
                 fg=ACCENT, bg=BG).pack()
        tk.Label(logo_frame, text="SYSTEM", font=("Courier New", 9),
                 fg=MUTED, bg=BG).pack()

        tk.Frame(sidebar, bg=BORDER, height=1).pack(fill="x", padx=16)

        # Tab buttons
        self.tab_buttons = {}
        self.active_tab = tk.StringVar(value="dashboard")
        nav_items = [
            ("dashboard", "🏠  Dashboard"),
            ("books",     "📖  Books"),
            ("members",   "👥  Members"),
            ("issue",     "🔄  Issue / Return"),
        ]
        nav_frame = tk.Frame(sidebar, bg=BG)
        nav_frame.pack(fill="x", pady=16)

        for key, label in nav_items:
            btn = tk.Button(nav_frame, text=label,
                            font=("Courier New", 10, "bold"),
                            bg=BG, fg=MUTED, anchor="w", relief="flat",
                            padx=20, pady=10, cursor="hand2",
                            activebackground=CARD, activeforeground=ACCENT,
                            command=lambda k=key: self.switch_tab(k))
            btn.pack(fill="x")
            self.tab_buttons[key] = btn

        # Version tag at bottom
        tk.Label(sidebar, text="v2.0 GUI", font=("Courier New", 8),
                 fg=BORDER, bg=BG).pack(side="bottom", pady=12)

        # ── CONTENT AREA ─────────────────────────────────────────
        self.content = tk.Frame(self, bg=PANEL)
        self.content.pack(side="left", fill="both", expand=True)

        # Build all tabs
        self.tabs = {
            "dashboard": DashboardTab(self.content, self),
            "books":     BookTab(self.content, self),
            "members":   MemberTab(self.content, self),
            "issue":     IssueTab(self.content, self),
        }

        self.switch_tab("dashboard")

    def switch_tab(self, key):
        # Hide all
        for tab in self.tabs.values():
            tab.pack_forget()
        # Reset button styles
        for k, btn in self.tab_buttons.items():
            if k == key:
                btn.config(bg=CARD, fg=ACCENT)
            else:
                btn.config(bg=BG, fg=MUTED)
        # Show selected
        self.tabs[key].pack(fill="both", expand=True)
        self.active_tab.set(key)


# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
