import mysql.connector

class MovieDAO:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def add_movie(self, movie_dto):
        cursor = self.db_connection.cursor()

        try:
            # Llamar al procedimiento almacenado para verificar si la película existe
            cursor.callproc('CheckMovieExists', [movie_dto.film_id, 0])
            result = cursor.stored_results().next().fetchone()
            exists = result[0] if result else 0

            if exists:
                return {"message": "La película ya existe."}

            # Llamar al procedimiento almacenado para agregar la película
            cursor.callproc('AddMovie', [movie_dto.film_id, movie_dto.title, movie_dto.description, movie_dto.language_id])
            self.db_connection.commit()
            return {"message": "Película agregada exitosamente"}

        except mysql.connector.Error as err:
            return {
                "message": "Error en la base de datos.",
                "error": str(err),
                "sqlstate": err.sqlstate if err.sqlstate else "No disponible",
                "errno": err.errno if err.errno else "No disponible"
            }
        finally:
            cursor.close()
