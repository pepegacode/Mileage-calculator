import csv
import tkinter as tk
from tkinter import messagebox

class CarPartDatabase:
    def __init__(self, filename):
        self.filename = filename
        self.karts = {}
        self.parts = []
        self.tracks = {}
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r', newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['type']=='kart':
                        kart_id = row['kart_id']
                        if kart_id not in self.karts:
                            self.karts[kart_id] = {
                                'name': row['name'],
                                'type':'kart',
                                'mileage': float(row['mileage']),
                                'kart_id':row['kart_id']
                            }
                    
                    #elif row['kart_id']:
                    #    pass
                        #kart_parts = self.karts[kart_id]['parts']
                        #kart_parts[row['id']] = {'name': row['name'], 'mileage': row['mileage']}
                    elif row['type']=='part':
                        part_details = row.get('details', '')  # Handle missing details field
                        self.parts.append({
                            'id': row['id'],
                            'name': row['name'],
                            'type': 'part',
                            'details': part_details,
                            'mileage': row['mileage'],
                            'kart_id': row['kart_id']
                        })

                    elif row['type']=='track':
                        id = row['id']
                        if id not in self.tracks:
                            self.tracks[id] = {
                                'name': row['name'],
                                'type':'track',
                                'mileage': row['mileage']
                            }
        except FileNotFoundError:
            pass

    def save_data(self):
        with open(self.filename, 'w', newline='') as file:
            fieldnames = ['id', 'name','type', 'details', 'mileage', 'kart_id']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for part in self.parts:
                writer.writerow(part)
            for kart_id, kart_data in self.karts.items():
                writer.writerow({  # Save kart as well
                    'id': kart_id,
                    'name': kart_data['name'],
                    'type':'kart',
                    'details': '',  # Kart details are empty
                    'mileage': kart_data['mileage'],
                    'kart_id': kart_data['kart_id']
                })
            for id, track_data in self.tracks.items():
                writer.writerow({  # Save track
                    'id': id,
                    'name': track_data['name'],
                    'type':'track',
                    'details': '',  # Track details are empty
                    'mileage': track_data['mileage'],
                    'kart_id': ''   #no kart id
                })

    def add_kart(self, kart_name):
        new_id = str(len(self.karts) + 1)
        self.karts[new_id] = {'id':new_id,'name': kart_name,'type':'kart', 'mileage': 0, 'kart_id': new_id}
        self.save_data()

    def add_track(self, track_name, length):
        new_id = str(len(self.tracks) + 1)
        self.tracks[new_id] = {'name': track_name,'type':'track', 'mileage': length}
        self.save_data()

    def remove_kart(self, kart_id):
        if kart_id in self.karts:
            del self.karts[kart_id]
            self.save_data()

    def remove_track(self, track_id):
        if track_id in self.tracks:
            del self.tracks[track_id]
            self.save_data()

    def add_part_to_kart(self, kart_id, part_id):
        if kart_id in self.karts:
            for i in self.parts:
                if str(i['id']) == str(part_id):
                    
                    i['kart_id'] = kart_id

            self.save_data()

    def remove_part_from_kart(self, kart_id, part_id):
        for i in self.parts:
            if str(i['id'])==str(part_id):
                i['kart_id']=0
        self.save_data()

    def add_part(self, part_name, part_details):
        new_id = str(len(self.parts) + 1)
        self.parts.append({'id': new_id,'type':'part', 'name': part_name, 'details': part_details, 'mileage': 0, 'kart_id': 0})
        self.save_data()

    def remove_part(self, part_id):
        part = next((part for part in self.parts if part['id'] == part_id), None)
        if part:
            self.parts.remove(part)
            self.save_data()

    def update_kart_mileage(self, kart_id, mileage):
        if kart_id in self.karts:
            self.karts[kart_id]['mileage'] += mileage
            self.update_parts_mileage(kart_id, mileage)
            self.save_data()

    def update_part_mileage(self, part_id, mileage):
        for part in self.parts:
            if str(part['id'])==str(part_id):
                part['mileage'] += mileage
            self.save_data()

    def update_parts_mileage(self, kart_id, mileage):
        for part in self.parts:
            if str(part['kart_id'])==str(kart_id):
                part['mileage'] += mileage

    def get_parts_without_kart(self):
        all_parts = set()
        for kart_data in self.karts.values():
            all_parts.update(part['name'] for part in kart_data['parts'].values())
        return [part for part in self.parts if part['name'] not in all_parts]

class CarPartGUI:
    def __init__(self, root, database):
        self.root = root
        self.root.title("Car Part Database")

        self.database = database
        self.selected_kart = None  # Store the selected kart
        self.selected_part = None  # Store the selected part

        self.kart_frame = tk.Frame(root)
        self.kart_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.parts_frame = tk.Frame(root)
        self.parts_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.track_frame = tk.Frame(root)
        self.track_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.init_kart_ui()
        self.init_parts_ui()
        self.init_kart_part_ui()
        self.init_track_ui()


    def init_kart_ui(self):
        self.kart_name_label = tk.Label(self.kart_frame, text="Kart Name:")
        self.kart_name_label.pack()

        self.kart_name_entry = tk.Entry(self.kart_frame)
        self.kart_name_entry.pack()

        self.add_kart_button = tk.Button(self.kart_frame, text="Add Kart", command=self.add_kart)
        self.add_kart_button.pack()

        self.kart_listbox = tk.Listbox(self.kart_frame, selectmode=tk.SINGLE,width=30)
        self.kart_listbox.pack()

        # Display selected kart's name
        self.selected_kart_label = tk.Label(self.kart_frame, text="Selected Kart:")
        self.selected_kart_label.pack()

        self.kart_listbox.bind("<<ListboxSelect>>", self.on_kart_selected)  # Bind selection event

        #self.kart_parts_label = tk.Label(self.kart_frame, text="Parts on Kart:")
        #self.kart_parts_label.pack()

        #self.kart_parts_listbox = tk.Listbox(self.kart_frame)
        #self.kart_parts_listbox.pack()



        self.remove_kart_button = tk.Button(self.kart_frame, text="Remove Kart", command=self.remove_kart)
        self.remove_kart_button.pack()
        


        self.refresh_karts()

    def init_kart_part_ui(self):

        self.kart_parts_label = tk.Label(self.kart_frame, text="Parts on Kart:")
        self.kart_parts_label.pack()

        self.kart_parts_listbox = tk.Listbox(self.kart_frame,width=30)
        self.kart_parts_listbox.pack()

        self.kart_parts_listbox.bind("<<ListboxSelect>>", self.on_kart_part_selected)  # Bind selection event
        
        self.kart_mileage_label = tk.Label(self.kart_frame, text="Kart Mileage:")
        self.kart_mileage_label.pack()

        self.kart_mileage_entry = tk.Entry(self.kart_frame)
        self.kart_mileage_entry.pack()

        self.update_kart_mileage_button = tk.Button(self.kart_frame, text="Update Kart Mileage", command=self.update_kart_mileage)
        self.update_kart_mileage_button.pack()

        self.refresh_parts()
        self.refresh_karts()

    def on_kart_selected(self, event):
        selected_kart = self.kart_listbox.curselection()
        if selected_kart:
            self.selected_kart = list(self.database.karts.keys())[selected_kart[0]]
            selected_kart_name = self.database.karts[self.selected_kart]['name']
            self.selected_kart_label.config(text=f"Selected Kart: {selected_kart_name}")
            self.refresh_kart_parts(self.selected_kart)
        else:
            pass
    
    def on_track_selected(self, event):
        selected_track = self.track_listbox.curselection()
        if selected_track:
            self.selected_track = list(self.database.karts.keys())[selected_track[0]]
            selected_track_name = self.database.tracks[self.selected_track]['name']
            self.selected_track_label.config(text=f"Selected Track: {selected_track_name}")
        else:
            pass
        

    def on_part_selected(self, event):
        selected_part = self.parts_listbox.curselection()
        if selected_part:
            self.selected_part = self.database.parts[selected_part[0]]
            self.selected_part_label.config(text=f"Selected Part: {self.selected_part['name']}")
            self.selected_part_details.config(text=f"Part Details: {self.selected_part['details']}")
        else:
            pass

    def on_kart_part_selected(self, event):
        selected_part = self.kart_parts_listbox.curselection()
        kplist=[]
        for part in self.database.parts:
            if str(part['kart_id'])==str(self.selected_kart): 
                kplist.append(part)
        if selected_part:
            self.selected_part = kplist[selected_part[0]]
            self.selected_part_label.config(text=f"Selected Part: {self.selected_part['name']}")
            self.selected_part_details.config(text=f"Part Details: {self.selected_part['details']}")
        else:
            pass

    def init_parts_ui(self):
        self.parts_label = tk.Label(self.parts_frame, text="Parts Database:")
        self.parts_label.pack()

        self.parts_listbox = tk.Listbox(self.parts_frame,width=30)
        self.parts_listbox.pack()

        self.selected_part_label = tk.Label(self.parts_frame, text="Selected Part:")
        self.selected_part_label.pack()

        self.selected_part_details = tk.Label(self.parts_frame)
        self.selected_part_details.pack()

        self.part_mileage_entry = tk.Entry(self.parts_frame)
        self.part_mileage_entry.pack()

        self.update_part_mileage_button = tk.Button(self.parts_frame, text="Update Part Mileage", command=self.update_part_mileage)
        self.update_part_mileage_button.pack()

        self.add_part_to_kart_button = tk.Button(self.parts_frame, text="Add Part to Kart", command=self.add_part_to_kart)
        self.add_part_to_kart_button.pack()

        self.remove_part_from_kart_button = tk.Button(self.parts_frame, text="Remove Part from Kart", command=self.remove_part_from_kart)
        self.remove_part_from_kart_button.pack()

        self.part_name_label = tk.Label(self.parts_frame, text="Part Name:")
        self.part_name_label.pack()

        self.part_name_entry = tk.Entry(self.parts_frame)
        self.part_name_entry.pack()

        self.part_details_label = tk.Label(self.parts_frame, text="Part Details:")
        self.part_details_label.pack()

        self.part_details_entry = tk.Text(self.parts_frame, height=4, width=30)
        self.part_details_entry.pack()

        self.add_part_button = tk.Button(self.parts_frame, text="Add Part", command=self.add_part)
        self.add_part_button.pack()

        self.remove_part_button = tk.Button(self.parts_frame, text="Remove Part", command=self.remove_part)
        self.remove_part_button.pack()

        self.parts_listbox.bind("<<ListboxSelect>>", self.on_part_selected)  # Bind selection event


        self.refresh_parts()

    def init_track_ui(self):
        
        self.track_label = tk.Label(self.track_frame, text="Track Database:")
        self.track_label.pack()

        self.track_listbox = tk.Listbox(self.track_frame,width=30)
        self.track_listbox.pack()

        self.selected_track_label = tk.Label(self.track_frame, text="Selected Track:")
        self.selected_track_label.pack()


        self.track_name_label = tk.Label(self.track_frame, text="Track Name:")
        self.track_name_label.pack()

        self.track_name_entry = tk.Entry(self.track_frame)
        self.track_name_entry.pack()

        self.track_length_label = tk.Label(self.track_frame, text="Track Length:")
        self.track_length_label.pack()

        self.track_length_entry = tk.Entry(self.track_frame)
        self.track_length_entry.pack()

        self.add_track_button = tk.Button(self.track_frame, text="Add Track", command=self.add_track)
        self.add_track_button.pack()

        self.remove_track_button = tk.Button(self.track_frame, text="Remove Track", command=self.remove_track)
        self.remove_track_button.pack()

        self.track_laps_entry = tk.Entry(self.track_frame)
        self.track_laps_entry.pack()

        self.remove_track_button = tk.Button(self.track_frame, text="Add laps to kart", command=self.update_kart_mileage)
        self.remove_track_button.pack()

        self.track_listbox.bind("<<ListboxSelect>>", self.on_track_selected)  # Bind selection event

        self.refresh_tracks()

    def refresh_karts(self):
        self.kart_listbox.delete(0, tk.END)
        for kart_id, kart_data in self.database.karts.items():
            kart_name = f"{kart_data['name']} - Mileage: {kart_data['mileage']}"
            self.kart_listbox.insert(tk.END, kart_name)

    def refresh_tracks(self):
        self.track_listbox.delete(0, tk.END)
        for track_id,track_data in self.database.tracks.items():
            track_name = f"{track_data['name']} - Length: {track_data['mileage']}"
            self.track_listbox.insert(tk.END, track_name)

    def refresh_kart_parts(self, kart_id):
        self.kart_parts_listbox.delete(0, tk.END)
        if kart_id in self.database.karts:
            for part in self.database.parts:
                if str(part['kart_id']) == str(kart_id):
                    part_name = f"{part['name']} - Mileage: {part['mileage']}"
                    self.kart_parts_listbox.insert(tk.END, part_name)

            # Display selected kart's name
            selected_kart_name = self.database.karts[kart_id]['name']
            self.selected_kart_label.config(text=f"Selected Kart: {selected_kart_name}")
        else:
            self.selected_kart_label.config(text="Selected Kart:")

    def refresh_parts(self):
        self.parts_listbox.delete(0, tk.END)
        for part in self.database.parts:
            part_name = f"{part['name']} - Mileage: {part['mileage']}"
            self.parts_listbox.insert(tk.END, part_name)

    def add_kart(self):
        kart_name = self.kart_name_entry.get()
        if kart_name:
            self.database.add_kart(kart_name)
            self.kart_name_entry.delete(0, tk.END)
            self.refresh_karts()

    def add_track(self):
        track_name = self.track_name_entry.get()
        length = self.track_length_entry.get()
        if track_name:
            self.database.add_track(track_name,length)
            self.track_name_entry.delete(0, tk.END)
            self.track_length_entry.delete(0, tk.END)
            self.refresh_tracks()

    def remove_kart(self):
        selected_kart = self.kart_listbox.curselection()
        if selected_kart:
            kart_id = list(self.database.karts.keys())[selected_kart[0]]
            self.database.remove_kart(kart_id)
            self.refresh_karts()
            self.kart_parts_listbox.delete(0, tk.END)

    def remove_track(self):
        selected_track = self.track_listbox.curselection()
        if selected_track:
            track_id = list(self.database.karts.keys())[selected_track[0]]
            self.database.remove_track(track_id)
            self.refresh_tracks()
            self.kart_parts_listbox.delete(0, tk.END)

    def add_part_to_kart(self):
        if self.selected_part and self.selected_kart:
            part_id = self.selected_part['id']
            self.database.add_part_to_kart(self.selected_kart, part_id)  # Use selected kart
            self.refresh_kart_parts(self.selected_kart)  # Refresh parts of selected kart
            self.refresh_parts()

    def remove_part_from_kart(self):
        if self.selected_part and self.selected_kart:
            part_id = self.selected_part['id']
            self.database.remove_part_from_kart(self.selected_kart, part_id)
            self.refresh_kart_parts(self.selected_kart)
            self.refresh_parts()

    def add_part(self):
        part_name = self.part_name_entry.get()
        part_details = self.part_details_entry.get("1.0", tk.END).strip()
        if part_details=='':
            part_details="None"
        if part_name:
            self.database.add_part(part_name, part_details)
            self.part_name_entry.delete(0, tk.END)
            self.part_details_entry.delete("1.0", tk.END)
            self.refresh_parts()


    def remove_part(self):
        selected_part = self.parts_listbox.curselection()
        if selected_part:
            part_id = self.database.parts[selected_part[0]]['id']
            self.database.remove_part(part_id)
            self.refresh_kart_parts(self.selected_kart)
            self.refresh_parts()

    def update_kart_mileage(self):
        manual = 0
        auto = 0
        
        
        if self.kart_mileage_entry.get() != '':
            manual = int(self.kart_mileage_entry.get())
        if self.track_laps_entry.get() != '':
            auto = int(self.track_laps_entry.get())*float(self.database.tracks[self.selected_track[0]]['mileage'])
            
        

        if auto > 0:
            mileage = auto
        else:
            mileage = manual

        if mileage >= 0:
            kart_id = self.selected_kart
            self.database.update_kart_mileage(kart_id, mileage)
            self.refresh_karts()
            self.refresh_kart_parts(kart_id)
            self.refresh_parts()
            self.kart_mileage_entry.delete(0, tk.END)
            self.track_laps_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid kart selection or mileage value.")

    def update_part_mileage(self):
        mileage = int(self.part_mileage_entry.get())
        
        if mileage >= 0:
            kart_id = self.selected_kart
            part_id = self.selected_part['id']
            print(mileage,part_id)
            self.database.update_part_mileage(part_id, mileage)
            self.refresh_karts()
            self.refresh_kart_parts(kart_id)
            self.refresh_parts()
            self.part_mileage_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid kart selection or mileage value.")

if __name__ == "__main__":
    db = CarPartDatabase("car_parts.csv")

    root = tk.Tk()
    gui = CarPartGUI(root, db)
    root.mainloop()