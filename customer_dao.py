import mysql.connector

class CustomerDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_customer(self, customer_dto):
        cursor = self.db_connection.cursor()

        try:
            args = [customer_dto.customer_id, 0]  
            result_args = cursor.callproc('CheckCustomerExists', args)
            exists = result_args[1]  
            if exists:
                return {"message": "El cliente ya existe."}

            cursor.callproc('AddCustomer', [customer_dto.customer_id, customer_dto.name, customer_dto.contact_name])
            self.db_connection.commit()
            return {"message": "Cliente agregado exitosamente"}

        except mysql.connector.Error as err:
            return {"message": "Error en la base de datos.", "error": str(err)}

