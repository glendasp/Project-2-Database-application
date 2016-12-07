import sqlite3
from models import Client, Appointment, Professional


class DatabaseManager:
    """Manages connecting and getting information from the database."""

    def __init__(self, filename):
        """Set up the connection to the database."""
        self.conn = sqlite3.connect(filename)

    def setup_db(self):
        sql_script = '''
            CREATE TABLE Client (
              ClientNum INT PRIMARY KEY,
              FirstName TEXT NOT NULL,
              LastName TEXT NOT NULL
            );

            CREATE TABLE Appointment (
              AppointmentNum INT PRIMARY KEY,
              Name TEXT NOT NULL,
              ProfessionalNum INT,
              FOREIGN KEY (ProfessionalNum) REFERENCES Professional
            );

            CREATE TABLE Professional (
              ProfessionalNum INT PRIMARY KEY,
              FirstName TEXT NOT NULL,
              LastName TEXT NOT NULL
            );

            CREATE TABLE Client_Appointment (
              ClientNum INT NOT NULL,
              AppointmentNum INT NOT NULL,
              PRIMARY KEY (ClientNum , AppointmentNum),
              FOREIGN KEY (ClientNum) REFERENCES Client,
              FOREIGN KEY (AppointmentNum) REFERENCES Appointment
            );

            INSERT INTO Client VALUES (1, 'Allison', 'Siehr');
            INSERT INTO Client VALUES (2, 'Alejandra', 'Ochoa');
            INSERT INTO Client VALUES (3, 'Denise', 'Wong');
            INSERT INTO Client VALUES (4, 'Prsicla', 'Pinho');
            INSERT INTO Client VALUES (5, 'Glenda', 'Pinho');
            INSERT INTO Client VALUES (6, 'Eva', 'Mendes');
            INSERT INTO Client VALUES (7, 'Julian', 'Preciado');
            INSERT INTO Client VALUES (8, 'Jessica', 'Oak');
            INSERT INTO Client VALUES (9, 'Amy', 'Borst');
            INSERT INTO Client VALUES (10, 'Heather', 'Barber');

            INSERT INTO Appointment VALUES (1, 'Makeup Application', 1);
            INSERT INTO Appointment VALUES (2, 'Massage',2);
            INSERT INTO Appointment VALUES (3, 'Shampoo Blow-dry & Style', 3);
            INSERT INTO Appointment VALUES (4, 'Haircut', 4);
            INSERT INTO Appointment VALUES (5, 'Manicure', 1);
            INSERT INTO Appointment VALUES (6, 'Pedcure', 1);
            INSERT INTO Appointment VALUES (7, 'Lightening and Toning', 5);

            INSERT INTO Professional VALUES (1, 'Sarah', 'Phill');
            INSERT INTO Professional VALUES (2, 'Amy', 'Clinton');
            INSERT INTO Professional VALUES (3, 'Mike', 'Rowe');
            INSERT INTO Professional VALUES (4, 'Sandy', 'Banks');
            INSERT INTO Professional VALUES (5, 'Ruth', 'Warren');
            INSERT INTO Professional VALUES (6, 'Lorena', 'Christensen');

            INSERT INTO Client_Appointment VALUES (4, 5);
            INSERT INTO Client_Appointment VALUES (4, 6);
            INSERT INTO Client_Appointment VALUES (5, 5);
            INSERT INTO Client_Appointment VALUES (5, 6);
            INSERT INTO Client_Appointment VALUES (8, 6);
            INSERT INTO Client_Appointment VALUES (8, 7);
            INSERT INTO Client_Appointment VALUES (7, 6);
            INSERT INTO Client_Appointment VALUES (7, 8);
        '''

        try:
            print('Creating tables...')
            self.conn.executescript(sql_script)
            print("Table successfully created")
        except sqlite3.OperationalError as oe:
            print('Error:', oe)

    # Return a client object from existing ID
    def get_client(self, client_id):
        try:
            cur = self.conn.cursor()
            query = 'SELECT * FROM Client WHERE ClientNum = ?'
            cur.execute(query, (client_id, ))

            row = cur.fetchone()
            if row:
                client_id, first_name, last_name = (row[0], row[1], row[2])
                return Client(client_id, first_name, last_name)

        except sqlite3.OperationalError as oe:
            print('Sql execution error', oe)
        except sqlite3.Error as e:
            print("Connection error ", e)

    # Returns a appointment object from existing ID
    def get_appointment(self, appointment_id):
        try:
            cur = self.conn.cursor()
            query = (
                'SELECT AppointmentNum, Name, Appointment.ProfessionalNum, FirstName, LastName '
                'FROM Appointment '
                'JOIN Professional ON Appointment.ProfessionalNum = Professional.ProfessionalNum '
                'WHERE AppointmentNum = ?'
            )
            cur.execute(query, (appointment_id, ))

            row = cur.fetchone()
            if row:
                appointment_id, appointment_name = (row[0], row[1])
                professional_id, first_name, last_name = (row[2], row[3], row[4])
                professional = Professional(professional_id, first_name, last_name)
                return Appointment(appointment_id, appointment_name, professional)

        except sqlite3.OperationalError as oe:
            print('Sql execution error', oe)
        except sqlite3.Error as e:
            print("Connection error ", e)

    # Returns a list of appointment that matches with appointment_name
    def get_appointment_by_name(self, appointment_name):
        try:
            cur = self.conn.cursor()
            # TODO: Query parameter might need some wildcards added.
            query = (
                'SELECT AppointmentNum, Name, Appointment.ProfessionalNum, FirstName, LastName '
                'FROM Appointment '
                'JOIN Professional ON Appointment.ProfessionalNum = Professional.ProfessionalNum '
                'WHERE UPPER(Name) LIKE ?'
            )
            cur.execute(query, ('%{}%'.format(appointment_name.upper()), ))

            appointment = []
            for row in cur:
                appointment_id, appointment_name = (row[0], row[1])
                professional_id, first_name, last_name = (row[2], row[3], row[4])
                professional = Professional(professional_id, first_name, last_name)
                appointment.append(Appointment(appointment_id, appointment_name, professional))
            return appointment

        except sqlite3.OperationalError as oe:
            print('Sql execution error', oe)
        except sqlite3.Error as e:
            print("Connection error ", e)

    # Return a client's list of appointments
    def get_appointment_by_client_id(self, appointment_id):
        cur = self.conn.cursor()
        query = 'SELECT * FROM Client_Appointment WHERE ClientNum LIKE ?'
        cur.execute(query, (appointment_id, ))
        appointments_list = []
        for row in cur.fetchall():
            appointment_id = row[1]
            appointments_list.append(self.get_appointment(appointment_id))
        return appointments_list

    # Add the Client to an appointment
    def register_appointment(self, client, appointment):
        try:
            cur = self.conn.cursor()
            query = 'INSERT INTO Client_Appointment VALUES (?, ?)'
            cur.execute(query, (client.id, appointment.id))
            self.conn.commit()

        except sqlite3.OperationalError as oe:
            print('Sql execution error', oe)
        except sqlite3.Error as e:
            print("Connection error ", e)

    # Drop appointment from the ppointment list for the client
    def drop_appointment(self, clientid, appointmentid):
        try:
            cur = self.conn.cursor()
            query = ('DELETE FROM Client_Appointment '
                     '  WHERE AppointmentNum = ? '
                     '  AND  ClientNum = ?')
            cur.execute(query, (appointmentid, clientid))
            self.conn.commit()

        except sqlite3.OperationalError as oe:
            print('Sql execution error', oe)
        except sqlite3.Error as e:
            print("Connection error ", e)
