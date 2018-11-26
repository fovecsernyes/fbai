## @file database.py
#  @author Mark Vecsernyes
#
#  @brief This file handles the database
#  @{ 

## Import modules
import psycopg2
from config import config


## Database class
class Database(object):
    ## Constructor connects to db
    def __init__(self):
        #print(TEST: Database __init__ called)
        self.conn = None
        try:
            self.params = config()
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**self.params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    # Destructor disconnects from db
    def __del__(self):
        #print(TEST: Database __del__ called)
       self.conn.close()
       print('Database connection closed.')


    ## Initializunk tables if not exist
    #  @return "OK" string
    def create_tables(self):
        #print(TEST: Database create_tables called)

        try:
            cycle = open('static/sql/cycle.sql','r')
            bird = open('static/sql/bird.sql','r')
            fitness = open('static/sql/fitness.sql','r')

            cur = self.conn.cursor()
            for i in [cycle, bird, fitness]:
                cur.execute(i.read())
                self.conn.commit()
            cur.close()

            return "OK"
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
            return "NOK"


    ## Inserting and updating in cycle table
    #  @param parameters string
    #  @return cycle id
    def insert_cycle(self, parameters, game_id):
        #print(TEST: Database insert_cycle( ) called)
        sqlInsert = """INSERT INTO public.cycle(parameters, game_id)
                        VALUES(%s, %s) RETURNING id;"""
        sqlUpdate = """UPDATE public.cycle
                        SET parent_id = %s
                        WHERE id = %s"""
        updated_rows = 0
        cycle_id = 0
        try:
            #print("insert_cycle")
            cur = self.conn.cursor()
            cur.execute(sqlInsert, (parameters,game_id,))
            cycle_id = cur.fetchone()[0]
            self.conn.commit()
            #print("update_cycle")
            cur.execute(sqlUpdate, (cycle_id, cycle_id))
            updated_rows = cur.rowcount
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()
        
        if updated_rows is None or updated_rows == 0:
            cycle_id = -1
        return cycle_id


    ## Inserting and updating in bird table
    #  @param cycle_id string 
    #  @param neural_network string
    #  @return bird_id string
    def insert_bird(self, cycle_id, neural_network):
        #print(TEST: Database insert_bird( ) called)
        sqlInsert = """INSERT INTO public.bird(cycle_id)
                   VALUES(%s) RETURNING id;"""
        sqlUpdate = """UPDATE public.bird
                        SET neural_network = %s
                        WHERE id = %s"""
        updated_rows = 0
        bird_id = 0
        try:
            cur = self.conn.cursor()
            #print("insert_bird")
            cur.execute(sqlInsert, (cycle_id,))
            bird_id = cur.fetchone()[0]
            self.conn.commit()
            #print("update_bird")
            cur.execute(sqlUpdate, (neural_network, bird_id))
            updated_rows = cur.rowcount
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()
        
        if updated_rows is None or updated_rows == 0:
            bird_id = -1
        return bird_id


    ## Inserting and updating in fitness table
    #  @param brid_id string
    #  @param fitness_score string
    #  @return fitness_id string
    def insert_fitness(self, bird_id, fitness_score):
        #print(TEST: Database insert_fitness( ) called)
        sqlInsert = """INSERT INTO public.fitness(cycle_id, bird_id)
                        VALUES((SELECT MAX(id) FROM public.cycle), %s) RETURNING id;"""
        sqlUpdate = """UPDATE public.fitness
                        SET fitness_score = %s
                        WHERE id = %s"""

        updated_rows = 0
        fitness_id = 0
        try:
            cur = self.conn.cursor()
            cur.execute(sqlInsert, (bird_id,))
            fitness_id = cur.fetchone()[0]
            self.conn.commit()
            cur.execute(sqlUpdate, (fitness_score, fitness_id))
            updated_rows = cur.rowcount
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()
        
        if updated_rows is None or updated_rows == 0:
            fitness_id = -1
        return fitness_id


    ## Select from bird table
    #  @param population integer
    #  @return ids and neural networks
    def select_bird(self, population):
        #print(TEST: Database select_bird( ) called)
        sqlSelect = """SELECT id, neural_network FROM
                    (SELECT * FROM bird ORDER BY id DESC LIMIT %s) AS selectbird
                    ORDER BY id ASC;"""

        try:
            cur = self.conn.cursor()
            cur.execute(sqlSelect, (population,))
            bird = cur.fetchall()
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()
            return bird


    ## Select from fitness table
    #  @param population integer
    #  @return fitness
    def select_fitness(self, population):
        #print(TEST: Database select_fitness( ) called)
        sqlSelect = """SELECT bird_id, fitness_score FROM
                    (SELECT * FROM fitness ORDER BY id DESC LIMIT %s) AS selectbird
                    ORDER BY id ASC;"""

        try:
            cur = self.conn.cursor()
            cur.execute(sqlSelect, (population,))
            fitness = cur.fetchall()
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()
        return fitness
        

    ## Updates the fitness value at given id
    #  @param net neural network
    #  @param bird_id string
    def update_net(self, net, bird_id):
        #print(TEST: Database update_net( ) called)
        sqlUpdate = """UPDATE "bird" 
                     SET neural_network = %s
                     WHERE id = %s;"""

        try:
            cur = self.conn.cursor()
            cur.execute(sqlUpdate, (net, bird_id))
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()

       ## Select from fitness table
    #  @param population integer
    #  @return fitness
    def select_game_id(self):
        #print(TEST: Database select_game_id( ) called)
        sqlSelect = """SELECT game_id FROM cycle ORDER BY game_id DESC LIMIT 1"""

        try:
            cur = self.conn.cursor()
            cur.execute(sqlSelect)
            game_id = cur.fetchone()
            self.conn.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is None:
                self.conn.close()
            return game_id


## @}
