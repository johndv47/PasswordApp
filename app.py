from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import ttkbootstrap as tb
from ttkbootstrap.constants import BOTH, LEFT, RIGHT, X, Y


APP_TITLE = "PasswordApp"
DEFAULT_THEME = "darkly"
AVAILABLE_THEMES = ["darkly", "flatly", "superhero", "cosmo"]
ACTIVITY_HOVER_TAG = "activity-hover"
ACTIVITY_DEFAULT_TAG = "activity-default"
ACTIVITY_HOVER_BG = "#2b3035"
ACTIVITY_DEFAULT_BG = "#212529"
ACTIVITY_DEFAULT_FG = "#f8f9fa"


class PasswordAppShell(tb.Window):
    """UI-only desktop shell for future PasswordApp features."""

    def __init__(self) -> None:
        super().__init__(themename=DEFAULT_THEME)
        self.title(APP_TITLE)
        self.geometry("1366x820")
        self.minsize(1120, 700)

        self._build_layout()

    def _build_layout(self) -> None:
        self._build_topbar()
        self._build_main_content()
        self._build_statusbar()

    def _build_topbar(self) -> None:
        topbar = tb.Frame(self, bootstyle="dark")
        topbar.pack(fill=X)

        branding = tb.Frame(topbar, bootstyle="dark")
        branding.pack(side=LEFT, padx=18, pady=12)
        tb.Label(
            branding,
            text="PasswordApp",
            font=("Segoe UI", 15, "bold"),
            bootstyle="inverse-dark",
        ).pack(anchor="w")
        tb.Label(
            branding,
            text="Desktop Security Workspace",
            font=("Segoe UI", 9),
            bootstyle="inverse-secondary",
        ).pack(anchor="w")

        actions = tb.Frame(topbar, bootstyle="dark")
        actions.pack(side=RIGHT, padx=18, pady=12)

        self.theme_var = tk.StringVar(value=DEFAULT_THEME)
        theme_select = tb.Combobox(
            actions,
            textvariable=self.theme_var,
            values=AVAILABLE_THEMES,
            state="readonly",
            width=12,
        )
        theme_select.bind("<<ComboboxSelected>>", self._on_theme_change)
        theme_select.pack(side=RIGHT, padx=(8, 0))

        for label, style in [
            ("Settings", "outline-light"),
            ("Sync", "outline-light"),
            ("+ New Vault", "success"),
        ]:
            tb.Button(actions, text=label, bootstyle=style, cursor="hand2").pack(
                side=RIGHT,
                padx=6,
            )

    def _build_main_content(self) -> None:
        container = tb.Frame(self)
        container.pack(fill=BOTH, expand=True)

        self._build_sidebar(container)
        self._build_workspace(container)

    def _build_sidebar(self, parent: ttk.Frame) -> None:
        sidebar = tb.Frame(parent, padding=14, bootstyle="secondary")
        sidebar.pack(side=LEFT, fill=Y)

        tb.Label(
            sidebar,
            text="Navigation",
            font=("Segoe UI", 10, "bold"),
            bootstyle="inverse-secondary",
        ).pack(anchor="w", padx=4, pady=(2, 12))

        for section in ["Dashboard", "Vaults", "Password Generator", "Audit", "Reports", "Trash"]:
            tb.Button(
                sidebar,
                text=section,
                bootstyle="secondary-link",
                width=24,
                cursor="hand2",
            ).pack(fill=X, pady=2)

        separator = ttk.Separator(sidebar)
        separator.pack(fill=X, pady=16)

        tb.Label(
            sidebar,
            text="Quick Filters",
            font=("Segoe UI", 10, "bold"),
            bootstyle="inverse-secondary",
        ).pack(anchor="w", padx=4, pady=(0, 8))

        for label in ["Expiring Soon", "Weak Passwords", "2FA Enabled", "Shared Items"]:
            tb.Checkbutton(sidebar, text=label, bootstyle="round-toggle").pack(
                anchor="w",
                pady=3,
            )

    def _build_workspace(self, parent: ttk.Frame) -> None:
        workspace = tb.Frame(parent, padding=18)
        workspace.pack(side=LEFT, fill=BOTH, expand=True)

        header = tb.Frame(workspace)
        header.pack(fill=X, pady=(0, 14))

        tb.Label(
            header,
            text="Vault Overview",
            font=("Segoe UI", 19, "bold"),
        ).pack(side=LEFT)

        search = tb.Entry(header, width=40)
        search.insert(0, "Search entries, vault names, or tags")
        search.pack(side=RIGHT)

        metrics = tb.Frame(workspace)
        metrics.pack(fill=X, pady=(0, 14))

        for title, value, style in [
            ("Total Entries", "236", "info"),
            ("Weak Passwords", "12", "warning"),
            ("Compromised", "3", "danger"),
            ("2FA Coverage", "81%", "success"),
        ]:
            card = tb.Labelframe(metrics, text=title, bootstyle=style, padding=12)
            card.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
            tb.Label(card, text=value, font=("Segoe UI", 20, "bold")).pack(anchor="w")
            tb.Label(card, text="Placeholder metric", bootstyle="secondary").pack(anchor="w")

        split = tb.Panedwindow(workspace, orient=tk.HORIZONTAL)
        split.pack(fill=BOTH, expand=True)

        table_panel = tb.Labelframe(split, text="Recent Credentials", padding=10)
        split.add(table_panel, weight=3)

        columns = ("service", "username", "category", "updated", "status")
        tree = ttk.Treeview(table_panel, columns=columns, show="headings", height=14)
        tree.pack(fill=BOTH, expand=True)

        headings = {
            "service": "Service",
            "username": "Username",
            "category": "Category",
            "updated": "Last Updated",
            "status": "Status",
        }
        for key in columns:
            tree.heading(key, text=headings[key])
            tree.column(key, width=130, anchor="w")

        sample_rows = [
            ("GitHub", "admin@company.com", "Development", "Today", "Healthy"),
            ("AWS Console", "ops@company.com", "Infrastructure", "2 days ago", "Rotate Soon"),
            ("Office 365", "it-admin@company.com", "Productivity", "5 days ago", "Healthy"),
            ("Salesforce", "crm-owner@company.com", "Business", "1 week ago", "Weak"),
        ]
        for row in sample_rows:
            tree.insert("", "end", values=row)

        right_panel = tb.Frame(split, padding=(10, 0, 0, 0))
        split.add(right_panel, weight=2)

        activity = tb.Labelframe(right_panel, text="Security Activity", padding=10)
        activity.pack(fill=BOTH, expand=True)

        timeline = tk.Text(
            activity,
            wrap="word",
            height=10,
            relief="flat",
            borderwidth=0,
            cursor="arrow",
            background=ACTIVITY_DEFAULT_BG,
            foreground=ACTIVITY_DEFAULT_FG,
            insertbackground=ACTIVITY_DEFAULT_FG,
        )
        timeline.pack(fill=BOTH, expand=True)
        timeline.tag_configure(ACTIVITY_DEFAULT_TAG, background=ACTIVITY_DEFAULT_BG)
        timeline.tag_configure(ACTIVITY_HOVER_TAG, background=ACTIVITY_HOVER_BG)
        timeline.insert(
            "1.0",
            "• Password health scan completed\n"
            "• New vault template created\n"
            "• Policy reminder generated\n"
            "• 2FA enrollment campaign scheduled\n"
            "\n"
            "All entries are static placeholders for future integration.",
            ACTIVITY_DEFAULT_TAG,
        )
        timeline.bind("<Motion>", self._on_activity_hover)
        timeline.bind("<Leave>", self._on_activity_leave)
        timeline.configure(state="disabled")

        actions = tb.Labelframe(right_panel, text="Pending Actions", padding=10)
        actions.pack(fill=X, pady=(10, 0))
        for item in ["Run full security audit", "Export monthly report", "Review stale credentials"]:
            tb.Button(actions, text=item, bootstyle="outline-primary", cursor="hand2").pack(
                fill=X,
                pady=4,
            )

    def _build_statusbar(self) -> None:
        statusbar = tb.Frame(self, bootstyle="light")
        statusbar.pack(fill=X, side="bottom")

        tb.Label(
            statusbar,
            text="Status: UI preview mode (no data persistence or network calls)",
            bootstyle="secondary",
        ).pack(side=LEFT, padx=10, pady=6)
        tb.Label(statusbar, text="v0.1 Shell", bootstyle="secondary").pack(
            side=RIGHT,
            padx=10,
            pady=6,
        )

    def _on_activity_hover(self, event: tk.Event) -> None:
        timeline = event.widget
        timeline.configure(state="normal")
        timeline.tag_remove(ACTIVITY_HOVER_TAG, "1.0", "end")
        hovered_index = timeline.index(f"@{event.x},{event.y}")
        line_start = f"{hovered_index} linestart"
        line_end = f"{hovered_index} lineend+1c"
        if timeline.get(line_start, line_end).strip():
            timeline.tag_add(ACTIVITY_HOVER_TAG, line_start, line_end)
        timeline.configure(state="disabled")

    def _on_activity_leave(self, event: tk.Event) -> None:
        timeline = event.widget
        timeline.configure(state="normal")
        timeline.tag_remove(ACTIVITY_HOVER_TAG, "1.0", "end")
        timeline.configure(state="disabled")

    def _on_theme_change(self, _event: tk.Event) -> None:
        selected = self.theme_var.get()
        self.style.theme_use(selected)


def main() -> None:
    app = PasswordAppShell()
    app.mainloop()


if __name__ == "__main__":
    main()
