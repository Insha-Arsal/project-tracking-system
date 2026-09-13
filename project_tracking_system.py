import datetime
import pandas as pd
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets


# ============================================================
# THEME & DISPLAY HELPERS
# ============================================================

PURPLE = "#7c3aed"
VIOLET = "#a78bfa"
PINK = "#f472b6"
GREEN = "#10b981"
AMBER = "#f59e0b"
RED = "#ef4444"
NAVY = "#0f0a1e"
SLATE = "#1a1030"
CARD = "#1e1535"


def show_banner():
    display(HTML(f"""
    <div style="background:linear-gradient(135deg,{NAVY},{SLATE});
    border:1px solid {PURPLE};border-radius:18px;padding:28px 24px;
    text-align:center;margin-bottom:16px;
    box-shadow:0 0 40px rgba(124,58,237,0.3);">
      <div style="font-size:3em;margin-bottom:8px;">◆</div>
      <h1 style="color:{VIOLET};font-size:2.2em;font-family:Courier New;
      letter-spacing:5px;text-shadow:0 0 18px {VIOLET};margin:0 0 6px;">
      PROJECT TRACKING</h1>
      <h2 style="color:{PINK};font-size:1em;font-family:Courier New;
      letter-spacing:3px;margin:0 0 12px;font-weight:normal;">
      — TEAM PRODUCTIVITY SYSTEM —</h2>
    </div>
    """))


def _msg(text, color, icon):
    display(HTML(f"""
    <div style="border-left:4px solid {color};border-radius:8px;
    padding:10px 16px;margin:5px 0;font-family:Courier New;
    color:{color};font-size:0.93em;">{icon} {text}</div>"""))


def ok(t):
    _msg(t, GREEN, "✓")


def err(t):
    _msg(t, RED, "✕")


def warn(t):
    _msg(t, AMBER, "⚠")


def info(t):
    _msg(t, VIOLET, "ℹ")


def section(title, icon="◆"):
    display(HTML(f"""
    <div style="background:linear-gradient(90deg,{SLATE},{NAVY});
    border-left:5px solid {PURPLE};border-radius:10px;
    padding:12px 18px;margin:16px 0 8px;font-family:Courier New;
    color:{VIOLET};font-size:1.2em;letter-spacing:2px;">
    {icon} {title}</div>"""))


def show_table(rows, title=""):
    if not rows:
        info("No records found.")
        return

    df = pd.DataFrame(rows)
    html_table = df.to_html(index=False, border=0, classes="pts-table")

    display(HTML(f"""
    <style>
    .pts-table{{width:100%;border-collapse:collapse;
    font-family:Courier New;font-size:0.86em;}}
    .pts-table th{{background:linear-gradient(90deg,#1a0a3e,#2d1b69);
    color:{VIOLET};padding:9px 12px;text-align:left;
    border-bottom:2px solid {PURPLE};}}
    .pts-table td{{padding:8px 12px;border-bottom:1px solid #2d1b50;
    color:#ddd6fe;background:{CARD};}}
    .pts-table tr:hover td{{background:#2d1b69;color:#fff;}}
    </style>
    <div style="background:{NAVY};border-radius:12px;padding:14px;
    border:1px solid #3b1f8a;overflow-x:auto;margin:8px 0;">
      <p style="color:{PINK};font-family:Courier New;font-size:0.9em;
      margin:0 0 8px;">◆ {title}</p>
      {html_table}
    </div>"""))


def kpi_cards(items):
    cards = "".join(f"""
    <div style="flex:1;min-width:130px;background:linear-gradient(135deg,{CARD},{SLATE});
    border-radius:14px;padding:18px;text-align:center;
    border:1px solid {color}44;box-shadow:0 6px 20px rgba(0,0,0,0.4);">
      <div style="font-size:1.8em;">{icon}</div>
      <div style="font-size:1.6em;font-weight:bold;color:{color};
      font-family:Courier New;margin:4px 0;">{val}</div>
      <div style="color:#7c5cbf;font-family:Courier New;font-size:0.78em;">
      {label}</div>
    </div>"""
                    for icon, val, label, color in items)

    display(HTML(
        f'<div style="display:flex;gap:10px;flex-wrap:wrap;margin:12px 0;">'
        f'{cards}</div>'
    ))


# ============================================================
# DATABASE
# ============================================================

class ProjectDB:
    def __init__(self):
        self.projects = {}       # prid -> dict
        self.members = {}        # mid -> dict
        self.tasks = {}          # tid -> dict
        self.bugs = {}           # bid -> dict
        self.milestones = {}     # msid -> dict

        self._prid = 1000
        self._mid = 2000
        self._tid = 3000
        self._bid = 4000
        self._msid = 5000

    def _prid_(self):
        i = f"PRJ-{self._prid}"
        self._prid += 1
        return i

    def _mid_(self):
        i = f"MEM-{self._mid}"
        self._mid += 1
        return i

    def _tid_(self):
        i = f"TSK-{self._tid}"
        self._tid += 1
        return i

    def _bid_(self):
        i = f"BUG-{self._bid}"
        self._bid += 1
        return i

    def _msid_(self):
        i = f"MLS-{self._msid}"
        self._msid += 1
        return i

    def now(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    # --------------------------------------------------------
    # PROJECTS
    # --------------------------------------------------------

    def add_project(self, name, description, client, deadline,
                    budget, manager, priority):
        prid = self._prid_()

        self.projects[prid] = dict(
            id=prid,
            name=name,
            description=description,
            client=client,
            deadline=deadline,
            budget=float(budget),
            manager=manager,
            priority=priority,
            status="Active",
            progress=0,
            created=self.now()
        )

        return prid

    def update_progress(self, prid, progress):
        if prid not in self.projects:
            return False, "Project not found."

        self.projects[prid]["progress"] = int(progress)

        if int(progress) == 100:
            self.projects[prid]["status"] = "Completed"

        return True, f"Progress updated to {progress}%"

    def close_project(self, prid):
        if prid not in self.projects:
            return False, "Project not found."

        self.projects[prid]["status"] = "Closed"
        return True, "Project closed."

    # --------------------------------------------------------
    # TEAM MEMBERS
    # --------------------------------------------------------

    def add_member(self, name, role, email, phone, department, skills):
        mid = self._mid_()

        self.members[mid] = dict(
            id=mid,
            name=name,
            role=role,
            email=email,
            phone=phone,
            department=department,
            skills=skills,
            status="Active",
            joined=self.now()
        )

        return mid

    # --------------------------------------------------------
    # TASKS
    # --------------------------------------------------------

    def add_task(self, prid, mid, title, description,
                 priority, deadline, estimated_hours):
        if prid not in self.projects:
            return None, "Project not found."

        if mid not in self.members:
            return None, "Member not found."

        tid = self._tid_()

        self.tasks[tid] = dict(
            id=tid,
            project_id=prid,
            member_id=mid,
            project_name=self.projects[prid]["name"],
            member_name=self.members[mid]["name"],
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            estimated_hours=int(estimated_hours),
            status="To Do",
            created=self.now()
        )

        return tid, "Task added."

    def update_task_status(self, tid, status):
        if tid not in self.tasks:
            return False, "Task not found."

        valid = ["To Do", "In Progress", "In Review", "Done", "Blocked"]

        if status not in valid:
            return False, f"Invalid status. Use: {valid}"

        self.tasks[tid]["status"] = status
        return True, f"Task status -> {status}"

    # --------------------------------------------------------
    # BUGS
    # --------------------------------------------------------

    def report_bug(self, prid, reported_by, title,
                   description, severity, assigned_to):
        if prid not in self.projects:
            return None, "Project not found."

        bid = self._bid_()

        self.bugs[bid] = dict(
            id=bid,
            project_id=prid,
            project_name=self.projects[prid]["name"],
            reported_by=reported_by,
            title=title,
            description=description,
            severity=severity,
            assigned_to=assigned_to,
            status="Open",
            reported_on=self.now()
        )

        return bid, "Bug reported."

    def resolve_bug(self, bid):
        if bid not in self.bugs:
            return False, "Bug not found."

        self.bugs[bid]["status"] = "Resolved"
        return True, "Bug resolved."

    # --------------------------------------------------------
    # MILESTONES
    # --------------------------------------------------------

    def add_milestone(self, prid, title, due_date, description):
        if prid not in self.projects:
            return None, "Project not found."

        msid = self._msid_()

        self.milestones[msid] = dict(
            id=msid,
            project_id=prid,
            project_name=self.projects[prid]["name"],
            title=title,
            due_date=due_date,
            description=description,
            status="Pending",
            created=self.now()
        )

        return msid, "Milestone added."

    def complete_milestone(self, msid):
        if msid not in self.milestones:
            return False, "Milestone not found."

        self.milestones[msid]["status"] = "Completed"
        return True, "Milestone completed."

    # --------------------------------------------------------
    # STATS
    # --------------------------------------------------------

    def stats(self):
        active = sum(
            1 for p in self.projects.values()
            if p["status"] == "Active"
        )

        completed = sum(
            1 for p in self.projects.values()
            if p["status"] == "Completed"
        )

        done_t = sum(
            1 for t in self.tasks.values()
            if t["status"] == "Done"
        )

        open_bugs = sum(
            1 for b in self.bugs.values()
            if b["status"] == "Open"
        )

        crit_bugs = sum(
            1 for b in self.bugs.values()
            if b["severity"] == "Critical" and b["status"] == "Open"
        )

        budget = sum(
            p["budget"] for p in self.projects.values()
        )

        return dict(
            projects=len(self.projects),
            active=active,
            completed=completed,
            members=len(self.members),
            tasks=len(self.tasks),
            done_tasks=done_t,
            bugs=len(self.bugs),
            open_bugs=open_bugs,
            critical_bugs=crit_bugs,
            milestones=len(self.milestones),
            total_budget=budget
        )


# ============================================================
# SEED SAMPLE DATA
# ============================================================

def seed(db):
    # Team Members
    m1 = db.add_member(
        "Ali Hassan", "Frontend Dev", "ali@dev.pk",
        "0300-1111111", "Engineering", "React, HTML, CSS"
    )

    m2 = db.add_member(
        "Sara Khan", "Backend Dev", "sara@dev.pk",
        "0300-2222222", "Engineering", "Python, Django, SQL"
    )

    m3 = db.add_member(
        "Usman Tariq", "UI/UX Designer", "usman@dev.pk",
        "0300-3333333", "Design", "Figma, Adobe XD"
    )

    m4 = db.add_member(
        "Ayesha Malik", "QA Engineer", "ayesha@dev.pk",
        "0300-4444444", "QA", "Testing, Selenium"
    )

    m5 = db.add_member(
        "Bilal Ahmed", "Project Manager", "bilal@dev.pk",
        "0300-5555555", "Management", "Agile, Scrum"
    )

    m6 = db.add_member(
        "Hina Qureshi", "Data Analyst", "hina@dev.pk",
        "0300-6666666", "Analytics", "Python, PowerBI"
    )

    # Projects
    p1 = db.add_project(
        "E-Commerce Platform",
        "Full-stack online store with cart & payment",
        "FashionPK Ltd", "2025-08-30", 500000,
        "Bilal Ahmed", "High"
    )

    p2 = db.add_project(
        "Hospital Management System",
        "Patient, doctor & billing management",
        "City Hospital", "2025-07-15", 350000,
        "Bilal Ahmed", "High"
    )

    p3 = db.add_project(
        "School ERP",
        "Student records, attendance, result management",
        "Beacon House", "2025-10-01", 250000,
        "Bilal Ahmed", "Medium"
    )

    p4 = db.add_project(
        "Delivery Tracking App",
        "Real-time GPS delivery tracking mobile app",
        "QuickShip PK", "2025-09-20", 180000,
        "Bilal Ahmed", "Medium"
    )

    db.update_progress(p1, 45)
    db.update_progress(p2, 80)
    db.update_progress(p3, 20)
    db.update_progress(p4, 60)

    # Tasks
    db.add_task(
        p1, m1, "Design Homepage UI",
        "Create responsive homepage layout",
        "High", "2025-05-20", 16
    )

    db.add_task(
        p1, m2, "Build Product API",
        "REST API for product listing & search",
        "High", "2025-05-25", 24
    )

    db.add_task(
        p1, m3, "Wireframes for Cart",
        "Design cart & checkout wireframes",
        "Medium", "2025-05-18", 10
    )

    db.add_task(
        p2, m2, "Patient Module",
        "CRUD operations for patient records",
        "High", "2025-05-22", 20
    )

    db.add_task(
        p2, m4, "Test Billing Flow",
        "End-to-end testing of billing module",
        "High", "2025-05-28", 12
    )

    db.add_task(
        p3, m1, "Student Dashboard",
        "Build student portal dashboard",
        "Medium", "2025-06-10", 18
    )

    db.add_task(
        p4, m2, "GPS Integration",
        "Integrate Google Maps SDK for tracking",
        "High", "2025-06-05", 30
    )

    db.add_task(
        p4, m6, "Analytics Dashboard",
        "Build delivery stats dashboard",
        "Low", "2025-06-15", 14
    )

    # Update some task statuses
    db.update_task_status("TSK-3000", "In Progress")
    db.update_task_status("TSK-3001", "In Progress")
    db.update_task_status("TSK-3002", "Done")
    db.update_task_status("TSK-3003", "In Progress")
    db.update_task_status("TSK-3004", "To Do")

    # Bugs
    db.report_bug(
        p1, "Ayesha Malik", "Login button not working on mobile",
        "Tap on login button does nothing on iOS Safari",
        "Critical", "Ali Hassan"
    )

    db.report_bug(
        p1, "Sara Khan", "Cart total calculation wrong",
        "Discount not applied correctly in cart",
        "High", "Sara Khan"
    )

    db.report_bug(
        p2, "Ayesha Malik", "Bill PDF not generating",
        "PDF export crashes for bills above 5 items",
        "Critical", "Sara Khan"
    )

    db.report_bug(
        p4, "Usman Tariq", "Map not loading on Android",
        "GPS map blank on Android 12 devices",
        "High", "Ali Hassan"
    )

    db.resolve_bug("BUG-4002")

    # Milestones
    db.add_milestone(
        p1, "MVP Launch", "2025-06-01",
        "Core e-commerce features live"
    )

    db.add_milestone(
        p1, "Payment Integration", "2025-07-01",
        "JazzCash & EasyPaisa integration complete"
    )

    db.add_milestone(
        p2, "Phase 1 Complete", "2025-06-15",
        "Patient & doctor modules live"
    )

    db.add_milestone(
        p3, "Database Design", "2025-05-30",
        "All ERDs and schema finalized"
    )

    db.complete_milestone("MLS-5002")


# ============================================================
# MAIN APPLICATION
# ============================================================

def run_tracker():
    db = ProjectDB()
    seed(db)

    show_banner()
    ok("System initialised! Sample data loaded successfully.")

    # Widget helpers
    BW = widgets.Layout(width="200px", height="44px", margin="5px")
    FW = widgets.Layout(width="390px")
    HW = widgets.Layout(width="270px")
    NW = widgets.Layout(width="190px")
    ST = {"description_width": "150px"}

    def text(d, ph=""):
        return widgets.Text(
            description=d,
            placeholder=ph,
            layout=FW,
            style=ST
        )

    def num(d, v=0):
        return widgets.IntText(
            description=d,
            value=v,
            layout=NW,
            style=ST
        )

    def flt(d, v=0.0):
        return widgets.FloatText(
            description=d,
            value=v,
            layout=NW,
            style=ST
        )

    def drop(d, opts):
        return widgets.Dropdown(
            description=d,
            options=opts,
            layout=HW,
            style=ST
        )

    def btn(label, style="info"):
        return widgets.Button(
            description=label,
            button_style=style,
            layout=BW
        )

    def out():
        return widgets.Output()

    # --------------------------------------------------------
    # Menu
    # --------------------------------------------------------

    section("CONTROL PANEL — SELECT A MODULE")

    btns = {
        "dashboard": btn("◆ Dashboard", "success"),
        "project": btn("◆ Projects", "info"),
        "member": btn("◆ Team Members", "info"),
        "task": btn("◆ Tasks", "warning"),
        "bug": btn("◆ Bug Tracker", "danger"),
        "milestone": btn("◆ Milestones", "warning"),
        "reports": btn("◆ Reports", "success"),
        "search": btn("◆ Search Project", "info"),
    }

    grid = widgets.GridBox(
        list(btns.values()),
        layout=widgets.Layout(
            grid_template_columns="repeat(4,auto)",
            grid_gap="5px"
        )
    )

    main_out = out()
    display(grid, main_out)

    # --------------------------------------------------------
    # MODULE: DASHBOARD
    # --------------------------------------------------------

    def show_dashboard(b):
        with main_out:
            clear_output(wait=True)

            section("LIVE DASHBOARD", "◆")
            s = db.stats()

            kpi_cards([
                ("◆", s["projects"], "Total Projects", VIOLET),
                ("◆", s["active"], "Active", GREEN),
                ("◆", s["completed"], "Completed", GREEN),
                ("◆", s["members"], "Team Members", PINK),
                ("◆", s["tasks"], "Total Tasks", AMBER),
                ("✓", s["done_tasks"], "Tasks Done", GREEN),
                ("◆", s["open_bugs"], "Open Bugs", RED),
                ("◆", s["critical_bugs"], "Critical Bugs", RED),
            ])

            # Projects overview
            section("ALL PROJECTS", "◆")

            rows = [
                {
                    "ID": p["id"],
                    "Project": p["name"],
                    "Client": p["client"],
                    "Manager": p["manager"],
                    "Priority": p["priority"],
                    "Progress": f'{p["progress"]}%',
                    "Deadline": p["deadline"],
                    "Budget (Rs)": f'{p["budget"]:,.0f}',
                    "Status": p["status"]
                }
                for p in db.projects.values()
            ]

            show_table(rows, "Project Overview")

            # Open bugs alert
            open_bugs = [
                b for b in db.bugs.values()
                if b["status"] == "Open"
            ]

            if open_bugs:
                section("OPEN BUGS ALERT", "⚠")

                rows = [
                    {
                        "ID": b["id"],
                        "Project": b["project_name"],
                        "Title": b["title"],
                        "Severity": b["severity"],
                        "Assigned To": b["assigned_to"]
                    }
                    for b in open_bugs
                ]

                show_table(
                    rows,
                    f"{len(open_bugs)} open bugs require attention!"
                )

    # --------------------------------------------------------
    # MODULE: ADD PROJECT
    # --------------------------------------------------------

    def show_project(b):
        with main_out:
            clear_output(wait=True)

            section("PROJECT MANAGEMENT", "◆")

            w_name = text("Project Name", "e.g. E-Commerce App")
            w_desc = text("Description", "Brief description")
            w_client = text("Client Name", "e.g. XYZ Corp")
            w_mgr = text("Manager", "e.g. Ali Hassan")
            w_ddl = text("Deadline", "YYYY-MM-DD")
            w_bgt = flt("Budget (Rs)", 100000)
            w_pri = drop("Priority", ["High", "Medium", "Low"])

            add_btn = btn("◆ Add Project", "success")
            list_btn = btn("◆ View All", "info")
            form_out = out()

            display(widgets.VBox([
                widgets.HBox([w_name, w_desc]),
                widgets.HBox([w_client, w_mgr]),
                widgets.HBox([w_ddl, w_bgt, w_pri]),
                widgets.HBox([add_btn, list_btn]),
                form_out
            ]))

            def do_add(b):
                with form_out:
                    clear_output(wait=True)

                    if not w_name.value.strip():
                        err("Project name is required!")
                        return

                    prid = db.add_project(
                        w_name.value,
                        w_desc.value,
                        w_client.value,
                        w_ddl.value,
                        w_bgt.value,
                        w_mgr.value,
                        w_pri.value
                    )

                    ok(f"Project added! ID: {prid}")

            def do_list(b):
                with form_out:
                    clear_output(wait=True)

                    rows = [
                        {
                            "ID": p["id"],
                            "Name": p["name"],
                            "Client": p["client"],
                            "Progress": f'{p["progress"]}%',
                            "Deadline": p["deadline"],
                            "Status": p["status"]
                        }
                        for p in db.projects.values()
                    ]

                    show_table(rows, "All Projects")

            add_btn.on_click(do_add)
            list_btn.on_click(do_list)

    # --------------------------------------------------------
    # MODULE: TEAM MEMBERS
    # --------------------------------------------------------

    def show_member(b):
        with main_out:
            clear_output(wait=True)

            section("TEAM MEMBER MANAGEMENT", "◆")

            w_name = text("Full Name", "e.g. Sara Khan")
            w_role = text("Role", "e.g. Backend Dev")
            w_email = text("Email", "e.g. sara@dev.pk")
            w_phone = text("Phone", "0300-XXXXXXX")
            w_dept = drop(
                "Department",
                ["Engineering", "Design", "QA",
                 "Management", "Analytics", "DevOps"]
            )
            w_skills = text("Skills", "e.g. Python, Django")

            add_btn = btn("◆ Add Member", "success")
            list_btn = btn("◆ View Team", "info")
            form_out = out()

            display(widgets.VBox([
                widgets.HBox([w_name, w_role]),
                widgets.HBox([w_email, w_phone]),
                widgets.HBox([w_dept, w_skills]),
                widgets.HBox([add_btn, list_btn]),
                form_out
            ]))

            def do_add(b):
                with form_out:
                    clear_output(wait=True)

                    if not w_name.value.strip():
                        err("Name required!")
                        return

                    mid = db.add_member(
                        w_name.value,
                        w_role.value,
                        w_email.value,
                        w_phone.value,
                        w_dept.value,
                        w_skills.value
                    )

                    ok(f"Member added! ID: {mid}")

            def do_list(b):
                with form_out:
                    clear_output(wait=True)

                    rows = [
                        {
                            "ID": m["id"],
                            "Name": m["name"],
                            "Role": m["role"],
                            "Dept": m["department"],
                            "Skills": m["skills"],
                            "Email": m["email"],
                            "Status": m["status"]
                        }
                        for m in db.members.values()
                    ]

                    show_table(rows, "Team Members")

            add_btn.on_click(do_add)
            list_btn.on_click(do_list)

    # --------------------------------------------------------
    # MODULE: TASKS
    # --------------------------------------------------------

    def show_task(b):
        with main_out:
            clear_output(wait=True)

            section("TASK MANAGEMENT", "◆")

            proj_opts = {
                p["name"]: k
                for k, p in db.projects.items()
            }

            mem_opts = {
                m["name"]: k
                for k, m in db.members.items()
            }

            w_proj = drop(
                "Project",
                list(proj_opts.keys()) or ["No projects"]
            )

            w_mem = drop(
                "Assign To",
                list(mem_opts.keys()) or ["No members"]
            )

            w_title = text("Task Title", "e.g. Build Login API")
            w_desc = text("Description", "Task details")
            w_pri = drop("Priority", ["High", "Medium", "Low"])
            w_ddl = text("Deadline", "YYYY-MM-DD")
            w_hrs = num("Est. Hours", 8)
            w_tid = text("Task ID", "TSK-XXXX (to update status)")
            w_stat = drop(
                "New Status",
                ["To Do", "In Progress", "In Review", "Done", "Blocked"]
            )

            add_btn = btn("◆ Add Task", "success")
            upd_btn = btn("◆ Update Status", "warning")
            list_btn = btn("◆ View Tasks", "info")
            form_out = out()

            display(widgets.VBox([
                widgets.HBox([w_proj, w_mem]),
                widgets.HBox([w_title, w_desc]),
                widgets.HBox([w_pri, w_ddl, w_hrs]),
                add_btn,
                widgets.HBox([w_tid, w_stat, upd_btn]),
                list_btn,
                form_out
            ]))

            def do_add(b):
                with form_out:
                    clear_output(wait=True)

                    prid = proj_opts.get(w_proj.value)
                    mid = mem_opts.get(w_mem.value)

                    tid, msg = db.add_task(
                        prid,
                        mid,
                        w_title.value,
                        w_desc.value,
                        w_pri.value,
                        w_ddl.value,
                        w_hrs.value
                    )

                    if tid:
                        ok(f"Task added! ID: {tid}")
                    else:
                        err(msg)

            def do_update(b):
                with form_out:
                    clear_output(wait=True)

                    ok_, msg = db.update_task_status(
                        w_tid.value.strip(),
                        w_stat.value
                    )

                    if ok_:
                        ok(msg)
                    else:
                        err(msg)

            def do_list(b):
                with form_out:
                    clear_output(wait=True)

                    rows = [
                        {
                            "ID": t["id"],
                            "Project": t["project_name"],
                            "Title": t["title"],
                            "Assigned": t["member_name"],
                            "Priority": t["priority"],
                            "Est. Hrs": t["estimated_hours"],
                            "Deadline": t["deadline"],
                            "Status": t["status"]
                        }
                        for t in db.tasks.values()
                    ]

                    show_table(rows, "All Tasks")

            add_btn.on_click(do_add)
            upd_btn.on_click(do_update)
            list_btn.on_click(do_list)

    # --------------------------------------------------------
    # MODULE: BUGS
    # --------------------------------------------------------

    def show_bug(b):
        with main_out:
            clear_output(wait=True)

            section("BUG TRACKER", "◆")

            proj_opts = {
                p["name"]: k
                for k, p in db.projects.items()
            }

            w_proj = drop(
                "Project",
                list(proj_opts.keys()) or ["None"]
            )

            w_rep = text("Reported By", "Your name")
            w_title = text("Bug Title", "Brief title")
            w_desc = text("Description", "Detailed description")
            w_sev = drop(
                "Severity",
                ["Critical", "High", "Medium", "Low"]
            )
            w_asgn = text("Assigned To", "Developer name")
            w_bid = text("Bug ID", "BUG-XXXX (to resolve)")

            rep_btn = btn("◆ Report Bug", "danger")
            res_btn = btn("◆ Resolve Bug", "success")
            list_btn = btn("◆ View Bugs", "warning")
            form_out = out()

            display(widgets.VBox([
                widgets.HBox([w_proj, w_rep]),
                widgets.HBox([w_title, w_desc]),
                widgets.HBox([w_sev, w_asgn]),
                rep_btn,
                widgets.HBox([w_bid, res_btn]),
                list_btn,
                form_out
            ]))

            def do_report(b):
                with form_out:
                    clear_output(wait=True)

                    prid = proj_opts.get(w_proj.value)

                    bid, msg = db.report_bug(
                        prid,
                        w_rep.value,
                        w_title.value,
                        w_desc.value,
                        w_sev.value,
                        w_asgn.value
                    )

                    if bid:
                        ok(f"Bug reported! ID: {bid}")
                    else:
                        err(msg)

            def do_resolve(b):
                with form_out:
                    clear_output(wait=True)

                    ok_, msg = db.resolve_bug(
                        w_bid.value.strip()
                    )

                    if ok_:
                        ok(msg)
                    else:
                        err(msg)

            def do_list(b):
                with form_out:
                    clear_output(wait=True)

                    rows = [
                        {
                            "ID": bg["id"],
                            "Project": bg["project_name"],
                            "Title": bg["title"],
                            "Severity": bg["severity"],
                            "Reported By": bg["reported_by"],
                            "Assigned To": bg["assigned_to"],
                            "Status": bg["status"]
                        }
                        for bg in db.bugs.values()
                    ]

                    show_table(rows, "All Bugs")

            rep_btn.on_click(do_report)
            res_btn.on_click(do_resolve)
            list_btn.on_click(do_list)

    # --------------------------------------------------------
    # MODULE: MILESTONES
    # --------------------------------------------------------

    def show_milestone(b):
        with main_out:
            clear_output(wait=True)

            section("MILESTONE TRACKER", "◆")

            proj_opts = {
                p["name"]: k
                for k, p in db.projects.items()
            }

            w_proj = drop(
                "Project",
                list(proj_opts.keys()) or ["None"]
            )

            w_title = text("Title", "e.g. MVP Launch")
            w_due = text("Due Date", "YYYY-MM-DD")
            w_desc = text("Description", "Milestone details")
            w_msid = text(
                "Milestone ID",
                "MLS-XXXX (to complete)"
            )

            add_btn = btn("◆ Add Milestone", "success")
            done_btn = btn("◆ Mark Complete", "warning")
            list_btn = btn("◆ View All", "info")
            form_out = out()

            display(widgets.VBox([
                widgets.HBox([w_proj, w_title]),
                widgets.HBox([w_due, w_desc]),
                add_btn,
                widgets.HBox([w_msid, done_btn]),
                list_btn,
                form_out
            ]))

            def do_add(b):
                with form_out:
                    clear_output(wait=True)

                    prid = proj_opts.get(w_proj.value)

                    msid, msg = db.add_milestone(
                        prid,
                        w_title.value,
                        w_due.value,
                        w_desc.value
                    )

                    if msid:
                        ok(f"Milestone added! ID: {msid}")
                    else:
                        err(msg)

            def do_done(b):
                with form_out:
                    clear_output(wait=True)

                    ok_, msg = db.complete_milestone(
                        w_msid.value.strip()
                    )

                    if ok_:
                        ok(msg)
                    else:
                        err(msg)

            def do_list(b):
                with form_out:
                    clear_output(wait=True)

                    rows = [
                        {
                            "ID": ms["id"],
                            "Project": ms["project_name"],
                            "Title": ms["title"],
                            "Due Date": ms["due_date"],
                            "Status": ms["status"]
                        }
                        for ms in db.milestones.values()
                    ]

                    show_table(rows, "All Milestones")

            add_btn.on_click(do_add)
            done_btn.on_click(do_done)
            list_btn.on_click(do_list)

    # --------------------------------------------------------
    # MODULE: REPORTS
    # --------------------------------------------------------

    def show_reports(b):
        with main_out:
            clear_output(wait=True)

            section("PROJECT REPORTS", "◆")
            s = db.stats()

            # Summary
            kpi_cards([
                ("◆", s["projects"], "Projects", VIOLET),
                ("◆", s["done_tasks"], "Tasks Done", GREEN),
                ("◆", s["open_bugs"], "Open Bugs", RED),
                ("◆", s["milestones"], "Milestones", AMBER),
                ("◆", f'Rs {s["total_budget"]:,.0f}',
                 "Total Budget", PINK),
            ])

            # Tasks by status
            section("TASKS BY STATUS", "◆")

            statuses = [
                "To Do",
                "In Progress",
                "In Review",
                "Done",
                "Blocked"
            ]

            rows = [
                {
                    "Status": st,
                    "Count": sum(
                        1 for t in db.tasks.values()
                        if t["status"] == st
                    )
                }
                for st in statuses
            ]

            show_table(rows, "Task Status Summary")

            # Bug severity breakdown
            section("BUG SEVERITY REPORT", "◆")

            sevs = ["Critical", "High", "Medium", "Low"]

            rows = [
                {
                    "Severity": sv,
                    "Total": sum(
                        1 for bg in db.bugs.values()
                        if bg["severity"] == sv
                    ),
                    "Open": sum(
                        1 for bg in db.bugs.values()
                        if bg["severity"] == sv
                        and bg["status"] == "Open"
                    ),
                    "Resolved": sum(
                        1 for bg in db.bugs.values()
                        if bg["severity"] == sv
                        and bg["status"] == "Resolved"
                    )
                }
                for sv in sevs
            ]

            show_table(rows, "Bug Severity Breakdown")

    # --------------------------------------------------------
    # MODULE: SEARCH PROJECT
    # --------------------------------------------------------

    def show_search(b):
        with main_out:
            clear_output(wait=True)

            section("SEARCH PROJECT", "◆")

            w_q = text(
                "Search",
                "Project name or client..."
            )

            srch_btn = btn("◆ Search", "info")
            form_out = out()

            display(
                widgets.HBox([w_q, srch_btn]),
                form_out
            )

            def do_search(b):
                with form_out:
                    clear_output(wait=True)

                    q = w_q.value.strip().lower()

                    if not q:
                        err("Enter search keyword!")
                        return

                    results = [
                        p for p in db.projects.values()
                        if q in p["name"].lower()
                        or q in p["client"].lower()
                        or q in p["manager"].lower()
                    ]

                    if results:
                        rows = [
                            {
                                "ID": p["id"],
                                "Name": p["name"],
                                "Client": p["client"],
                                "Manager": p["manager"],
                                "Progress": f'{p["progress"]}%',
                                "Status": p["status"]
                            }
                            for p in results
                        ]

                        show_table(
                            rows,
                            f"Found {len(results)} result(s)"
                        )
                    else:
                        warn(
                            f"No projects found for '{w_q.value}'"
                        )

            srch_btn.on_click(do_search)

    # --------------------------------------------------------
    # Wire buttons
    # --------------------------------------------------------

    btns["dashboard"].on_click(show_dashboard)
    btns["project"].on_click(show_project)
    btns["member"].on_click(show_member)
    btns["task"].on_click(show_task)
    btns["bug"].on_click(show_bug)
    btns["milestone"].on_click(show_milestone)
    btns["reports"].on_click(show_reports)
    btns["search"].on_click(show_search)

    # Auto-load dashboard
    show_dashboard(None)


# ============================================================
# ENTRY POINT
# ============================================================

run_tracker()

# Project Tracking System | Programming Fundamentals | Python + Google Colab
