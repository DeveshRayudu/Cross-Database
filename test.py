import tkinter as tk
from tkinter import messagebox, ttk
import connection
import show_tables
import operation
from logger import setup_logger

t = tk.Tk()
t.title("Data Transfer Tool")
screen_width = t.winfo_screenwidth()
screen_height = t.winfo_screenheight()
t.geometry(f"{screen_width}x{screen_height}")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", font=("nunito", 10), padding=10, foreground="blue", background="white")

logger = setup_logger()

src_type1 = tk.StringVar()
dst_type1 = tk.StringVar()
oper1 = tk.StringVar()
selected_table1 = tk.StringVar()
destination_table1 = tk.StringVar()

for col in range(4):
    t.grid_columnconfigure(col, weight=1)

tk.Label(t, text="Data Transfer Tool", font=("nunito", 20), foreground="blue") .grid(row=0, column=1, columnspan=2, pady=20)

tk.Label(t, text="Source DB (oracle/mysql/postgresql):", font=("cambria", 12)) .grid(row=1, column=1, padx=(20, 10), sticky="s")  
tk.Entry(t, textvariable=src_type1, width=30) .grid(row=2, column=1, padx=(20, 10), pady=5)

tk.Label(t, text="Destination DB (oracle/mysql/postgresql):", font=("cambria", 12)) .grid(row=1, column=2, padx=(10, 20), sticky="s")  
tk.Entry(t, textvariable=dst_type1, width=30) .grid(row=2, column=2, padx=(10, 20), pady=5)

tk.Label(t, text="Operation (create or insert):", font=("cambria", 12)) .grid(row=3, column=1, columnspan=2, pady=(20, 5))
tk.Entry(t, textvariable=oper1, width=50) .grid(row=4, column=1, columnspan=2, pady=5)


table_frame = tk.Frame(t)
table_frame.grid(row=5, column=1, columnspan=2, pady=20)

tk.Label(table_frame, text="Select a table:",font=("cambria",12)).grid(row=0, column=0, sticky="s", pady=2)
tk.Entry(table_frame, textvariable=selected_table1, width=50).grid(row=1, column=0, pady=5)

tk.Label(table_frame, text="Destination table name:",font=("cambria",12)).grid(row=2, column=0, sticky="s", pady=2)
tk.Entry(table_frame, textvariable=destination_table1, width=50).grid(row=3, column=0, pady=5)
ttk.Button(table_frame, text="Submit Table Action", command=lambda: submit1()).grid(row=4, column=0, pady=10)

btn_frame = tk.Frame(t)
btn_frame.grid(row=6, column=1, columnspan=2, pady=10)

ttk.Button(btn_frame, text="Connect & Show Tables", command=lambda: submit()).pack(side="left", padx=10)
ttk.Button(btn_frame, text="Clear All", command=lambda: clear_inputs()).pack(side="left", padx=10)

list_label = tk.Label(t, text="", justify="left", font=("Courier", 10), fg="red")
list_label.grid(row=7, column=1, columnspan=2, pady=10)

def clear_inputs():
    src_type1.set('')
    dst_type1.set('')
    oper1.set('')
    selected_table1.set('')
    destination_table1.set('')
    list_label.config(text="")

def submit():
    try:
        global src_type, dst_type, oper
        src_type = src_type1.get()
        dst_type = dst_type1.get()
        oper = oper1.get()

        logger.info(f"Source DB: {src_type}, Destination DB: {dst_type}, Operation: {oper}")

        global src_conn, src_cursor, dst_conn, dst_cursor
        src_conn, src_cursor = connection.connect_database(src_type)
        dst_conn, dst_cursor = connection.connect_database(dst_type)
        logger.info("Connected to source and destination databases")

        tables = show_tables.get_tables(src_cursor, src_type)
        list_label.config(text="Available Tables:\n" + "\n".join(tables))
        logger.info(f"Available tables in {src_type}: {tables}")

    except Exception as e:
        logger.error("An unexpected error occurred in submit().", exc_info=True)
        messagebox.showerror("Error", str(e))

def submit1():
    try:
        selected_table = selected_table1.get()
        destination_table = destination_table1.get()

        logger.info(f"Selected table: {selected_table}")
        logger.info(f"Destination table name: {destination_table}")

        if oper == 'create':
            if show_tables.table_exists(dst_cursor, dst_type, destination_table):
                messagebox.showinfo("Info", f"Table {destination_table} already exists in {dst_type}.")
                logger.warning(f"Table {destination_table} already exists in {dst_type}.")
            else:
                schema = show_tables.get_table_schema(src_cursor, src_type, selected_table)
                operation.table_creation(destination_table, schema, dst_cursor, dst_type)
                dst_conn.commit()
                messagebox.showinfo("Success", f"Table {destination_table} created successfully.")
                logger.info(f"Table {destination_table} created successfully.")

        elif oper == 'insert':
            if show_tables.table_exists(dst_cursor, dst_type, destination_table):
                logger.warning(f"Table {destination_table} exists. Dropping and recreating.")
                dst_cursor.execute(f"DROP TABLE {destination_table}")

            schema = show_tables.get_table_schema(src_cursor, src_type, selected_table)
            operation.table_creation(destination_table, schema, dst_cursor, dst_type)
            dst_conn.commit()

            operation.transfer_data(src_cursor, dst_cursor, dst_conn, selected_table, destination_table, dst_type)
            logger.info(f"Data transferred from {selected_table} to {destination_table}")
            messagebox.showinfo("Success", f"Data transferred to {destination_table}")

        else:
            logger.error("Invalid operation specified.")
            messagebox.showerror("Error", "Invalid operation. Use 'create' or 'insert'.")

    except Exception as e:
        logger.error("Error in submit1()", exc_info=True)
        messagebox.showerror("Error", str(e))

    finally:
        if 'src_conn' in locals():
            src_conn.close()
        if 'dst_conn' in locals():
            dst_conn.close()
        logger.info("Database connections closed.")

t.mainloop()
