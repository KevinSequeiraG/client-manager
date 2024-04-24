from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title('CRM')

conn = sqlite3.connect('crm.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS client (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT NOT NULL, company TEXT NOT NULL)')

def renderClients():
    rows = c.execute('SELECT * FROM client').fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', END, row[0], values=(row[1], row[2], row[3]))

def insert(client):
    c.execute('INSERT INTO client (name, phone, company) VALUES (?, ?, ?)', (client['name'], client['phone'], client['company']))
    conn.commit()
    renderClients()

def newClient():
    def save():
        if not name.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return
        if not phone.get():
            messagebox.showerror('Error', 'El teléfono es obligatorio')
            return
        if not company.get():
            messagebox.showerror('Error', 'La empresa es obligatoria')
            return
        
        client = {
            'name': name.get(),
            'phone': phone.get(),
            'company': company.get()
        }
        insert(client)
        top.destroy()
    
    top = Toplevel()
    top.title('Nuevo cliente')
    
    lName = Label(top, text='Nombre')
    name = Entry(top, width=40)
    lName.grid(row=0, column=0)
    name.grid(row=0, column=1)
    
    lPhone = Label(top, text='Teléfono')
    phone = Entry(top, width=40)
    lPhone.grid(row=1, column=0)
    phone.grid(row=1, column=1)
    
    lCompany = Label(top, text='Empresa')
    company = Entry(top, width=40)
    lCompany.grid(row=2, column=0)
    company.grid(row=2, column=1)
    
    saveBtn = Button(top, text='Guardar', command=save)
    saveBtn.grid(row=3, column=1)
    
    name.focus()
    top.bind('<Return>', lambda x:save())
    top.mainloop()

def deleteClient():
    id = tree.selection()[0]
    client = c.execute('SELECT * FROM client WHERE id = ? ', (id,)).fetchone()
    ask = messagebox.askokcancel('SEGURO?', 'Estás seguro de querer eliminar el cliente:' + client[1])
    if ask:
        c.execute('DELETE FROM client WHERE ID = ?', (id,))
        conn.commit()
        renderClients()
    else:
        pass

addClientBtn = Button(root, text='Nuevo cliente', command=newClient)
addClientBtn.grid(row=0, column=0)

deleteClientbtn = Button(root, text='Eliminar cliente', command=deleteClient)
deleteClientbtn.grid(row=0, column=1)

tree = ttk.Treeview(root)
tree['columns'] = ('name', 'phone', 'company')

tree.column('#0', width=0, stretch=NO)
tree.column('name')
tree.column('phone')
tree.column('company')

tree.heading('name', text='Nombre')
tree.heading('phone', text='Teléfono')
tree.heading('company', text='Empresa')
tree.grid(column=0, row=1, columnspan=2)

tree.grid()

renderClients()
root.mainloop()