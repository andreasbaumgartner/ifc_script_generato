def main():
    generate_batch_script()


import os
import tkinter as tk
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_SQL_PATH = "sql-novatest.test.local:NovaProjects::"
NOVA_VERSION = "Nova 17.1"


def toggle_advanced_settings():
    global show_advanced
    show_advanced = not show_advanced
    update_advanced_settings()


def update_advanced_settings():
    if show_advanced:
        advanced_settings_frame.grid()
        toggle_button.config(text="Hide Advanced Settings")
    else:
        advanced_settings_frame.grid_remove()
        toggle_button.config(text="Show Advanced Settings")


def update_file_list():
    template_path = path_entry.get()
    if not template_path:
        template_path = BASE_DIR + "/ifc_templates"
    try:
        files = [
            f
            for f in os.listdir(template_path)
            if os.path.isfile(os.path.join(template_path, f))
        ]
        ifc_template_combobox["values"] = files
    except FileNotFoundError:
        ifc_template_combobox["values"] = []


def generate_batch_script():
    path = path_entry.get()
    project_hash = project_hash_entry.get()
    ifc_template = ifc_template_combobox.get()
    save_location = save_location_entry.get()

    print(path, project_hash, ifc_template, save_location)

    script_content = f"""chcp 1252
    del {path}\\*.ifc

    "C:\\Program Files\\Trimble\\{NOVA_VERSION}\\Nova.exe" /writeIfc:"{BASE_SQL_PATH}{project_hash}";"{path}";"{ifc_template}" 
    timeout /t 5 /nobreak

    ren {path}\\*{project_hash}*.ifc {project_hash}.ifc

    xcopy {path}\\{project_hash}.ifc "{save_location}" /Y
    """

    with open(os.path.join(save_location, "{}.bat".format(project_hash)), "w") as file:
        file.write(script_content)
    status_label.config(text="Batch Script Generated Successfully")


root = tk.Tk()
root.title("Batch Script Generator for Nova 17.1")

# IFC Template Selection
tk.Label(root, text="IFC Template:").grid(row=0, column=0)
ifc_template_combobox = ttk.Combobox(root)
ifc_template_combobox.grid(row=0, column=1)
ifc_template_combobox.bind("<Button-1>", lambda event: update_file_list())

# Temp Path to save IFCs Scripts
tk.Label(root, text="Temp Path:").grid(row=1, column=0)
path_entry = tk.Entry(root)
path_entry.grid(row=1, column=1)

# Project ID from the SQL NOVA Server // Like: 45608B7B-FB6C-48D9-901B-4198E1E0413B
tk.Label(root, text="Project ID:").grid(row=2, column=0)
project_hash_entry = tk.Entry(root)
project_hash_entry.grid(row=2, column=1)

# Save Location for the IFCs
tk.Label(root, text="Save Location:").grid(row=3, column=0)
save_location_entry = tk.Entry(root)
save_location_entry.grid(row=3, column=1)


# Generate Button
generate_button = tk.Button(root, text="Generate Script", command=generate_batch_script)
generate_button.grid(row=4, column=1)

# Status Label / Success or Error Message
status_label = tk.Label(root, text="")
status_label.grid(row=5, column=0, columnspan=2)

advanced_settings_frame = tk.Frame(root)
advanced_settings_frame.grid(row=8, column=0, columnspan=2)

tk.Label(advanced_settings_frame, text="Nova Exe Path :").grid(row=1, column=0)
nova_exe_entry = tk.Entry(advanced_settings_frame)
nova_exe_entry.grid(row=1, column=1)

tk.Label(advanced_settings_frame, text="SQL Server Path :").grid(row=2, column=0)
sql_server_entry = tk.Entry(advanced_settings_frame)
sql_server_entry.grid(row=2, column=1)

toggle_button = tk.Button(
    root, text="Show Advanced Settings", command=toggle_advanced_settings
)
toggle_button.grid(row=0, column=2)

status_label = tk.Label(root, text="")
status_label.grid(row=5, column=0, columnspan=2)

# Initial state of advanced settings
show_advanced = False
update_advanced_settings()


root.mainloop()


if __name__ == "__main__":
    main()
