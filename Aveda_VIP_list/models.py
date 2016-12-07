class Client:
    def __init__(self, client_id, first_name, last_name):
        self.id = client_id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)


class Appointment:
    def __init__(self, appointment_id, name, professional):
        self.id = appointment_id
        self.name = name
        self.professional = professional


class Professional:
    def __init__(self, professional_id, first_name, last_name):
        self.id = professional_id
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
