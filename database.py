## @file database.py
#  @author Mark Vecsernyes
#
#  @brief Ez a fájl kezeli az adatbázist
#  @{ 

## A szükséges könyvtárak importálása
import psycopg2
from config import config

## Database osztály az adatbázis kezeléséhez
class Database(object):
    ## Konstruktor: kapcsolódik az adatbázishoz
    def __init__(self):
        self.conn = None
        try:
            self.params = config()
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(**self.params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    ## Destruktor: lecsatlakozik az adatbázisról
    def __del__(self):
        self.conn.close()
        print('Database connection closed.')

    ## Táblák létrehozása ha nem létezik
    #  @return "OK" string
    def create_tables(self):

        commands = (
            """
                CREATE TABLE IF NOT EXISTS public.cycle
                (
                id serial NOT NULL,
                parent_id integer DEFAULT 0,
                sum_fitness integer NOT NULL DEFAULT 0,
                parameters text NOT NULL DEFAULT '',
                CONSTRAINT cycle_pkey PRIMARY KEY (id),
                CONSTRAINT cycle_parent_id_fkey FOREIGN KEY (parent_id)
                    REFERENCES public.cycle (id) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE CASCADE
                )
                WITH (
                OIDS=FALSE
                );
                ALTER TABLE public.cycle OWNER TO postgres;

                COMMENT ON TABLE public.cycle IS 'Stores the game cycle informations';
                COMMENT ON COLUMN public.cycle.id IS 'ID, generated by sequence';
                COMMENT ON COLUMN public.cycle.parent_id IS 'Foreign key to this table, stores the first cycle of the gouped generations';
                COMMENT ON COLUMN public.cycle.sum_fitness IS 'The sum fitness of the generation in this cycle';
                COMMENT ON COLUMN public.cycle.parameters IS 'The running parameters';

                CREATE UNIQUE INDEX IF NOT EXISTS cycle_cycle_parent_idx
                ON public.cycle
                USING btree
                (id, parent_id);

                INSERT INTO public.cycle (id, parent_id)
                SELECT 0, 0
                WHERE NOT EXISTS (SELECT 1 FROM public.cycle WHERE id = 0 AND parent_id = 0);
            """,
            """
                CREATE TABLE IF NOT EXISTS public.bird
                (
                id serial NOT NULL,
                cycle_id integer NOT NULL DEFAULT 0,
                neural_network bytea NOT NULL DEFAULT '',
                CONSTRAINT bird_pkey PRIMARY KEY (id),
                CONSTRAINT bird_cycle_id_fkey FOREIGN KEY (cycle_id)
                    REFERENCES public.cycle (id) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE CASCADE
                )
                WITH (
                OIDS=FALSE
                );
                ALTER TABLE public.bird OWNER TO postgres;

                COMMENT ON TABLE public.bird IS 'Stores the game cycle infomrations';
                COMMENT ON COLUMN public.bird.id IS 'ID, generated by sequence';
                COMMENT ON COLUMN public.bird.cycle_id IS 'Foreign key to the cycle table';
                COMMENT ON COLUMN public.bird.neural_network IS 'The neural network of the bird';
            """,
            """
                CREATE TABLE IF NOT EXISTS public.fitness
                (
                id serial NOT NULL,
                cycle_id integer NOT NULL DEFAULT 0,
                bird_id integer NOT NULL DEFAULT 0,
                fitness_score integer NOT NULL DEFAULT 0,
                CONSTRAINT fitness_pkey PRIMARY KEY (id),
                CONSTRAINT fitness_cycle_id_fkey FOREIGN KEY (cycle_id)
                    REFERENCES public.cycle (id) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE CASCADE,
                CONSTRAINT fitness_bird_id_fkey FOREIGN KEY (bird_id)
                    REFERENCES public.bird (id) MATCH SIMPLE
                    ON UPDATE NO ACTION ON DELETE CASCADE
                )
                WITH (
                OIDS=FALSE
                );
                ALTER TABLE public.fitness OWNER TO postgres;

                COMMENT ON TABLE public.fitness IS 'Stores the fitness infomrations';
                COMMENT ON COLUMN public.fitness.id IS 'ID, generated by sequence';
                COMMENT ON COLUMN public.fitness.cycle_id IS 'Foreign key to the cycle table';
                COMMENT ON COLUMN public.fitness.bird_id IS 'Foreign key to the bird table';
                COMMENT ON COLUMN public.fitness.fitness_score IS 'The fitness of the bird';
            """
            )
        cur = self.conn.cursor()
        for command in commands:
             cur.execute(command)
        cur.close()
        self.conn.commit()
        print("Database intialized")
        return "OK"

    ## Beszúrás és frissítés a "CYCLE" táblában
    #  @param parameters string
    def insert_cycle(self, parameters):
        sqlInsert = """INSERT INTO public.cycle(parameters)
                        VALUES(%s) RETURNING id;"""
        sqlUpdate = """UPDATE public.cycle
                        SET parent_id = %s
                        WHERE id = %s"""
        updated_rows = 0
        cycle_id = 0
        try:
            #print("insert_cycle")
            cur = self.conn.cursor()
            cur.execute(sqlInsert, (parameters,))
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

    ## Beszúrás és frissítés a "BIRD" táblában
    #  @param cycle_id string a ciklus száma
    #  @param neural_network object neurális hálók pickle dump-olva
    #  @return bird_id a madarak azonosítói
    def insert_bird(self, cycle_id, neural_network):
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

    ## Beszúrás és frissítés a "FITNESS" táblában
    #  @param brid_id string a madarak azonosítói
    #  @param fitness_score string a madár fitness értéke
    #  @return fitness_id string fitness értékek azonosítói
    def insert_fitness(self, bird_id, fitness_score):
        sqlInsert = """INSERT INTO public.fitness(cycle_id, bird_id)
                        VALUES((SELECT MAX(id) FROM public.cycle), %s) RETURNING id;"""
        sqlUpdate = """UPDATE public.fitness
                        SET fitness_score = %s
                        WHERE id = %s"""

        updated_rows = 0
        fitness_id = 0
        try:
            #print("insert_fitness")
            cur = self.conn.cursor()
            cur.execute(sqlInsert, (bird_id,))
            fitness_id = cur.fetchone()[0]
            self.conn.commit()
            #print("update_fitness")
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

    ## Lekérdezés a "BIRD" táblából az utolsó n db maradat
    #  @param population integer a populacio mérete
    #  @return bird ami az az azonosítót es a neurális hálókat tartalmazza
    def select_bird(self, population):
        sqlSelect = """SELECT id, neural_network FROM
                    (SELECT * FROM bird ORDER BY id DESC LIMIT %s) AS selectbird
                    ORDER BY id ASC;"""

        try:
            #print("select_bird")
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

    ## Lekérdezés a "FITNESS" táblából az utolsó n db erteket
    #  @param population integer a populacio mérete
    #  @return fitness ami a madár az azonosítóját es a fitness tartalmazza
    def select_fitness(self, population):
        sqlSelect = """SELECT bird_id, fitness_score FROM
                    (SELECT * FROM fitness ORDER BY id DESC LIMIT %s) AS selectbird
                    ORDER BY id ASC;"""

        try:
            #print("select_bird")
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

    ## Frissíti a neurális háló értékét a megadott id-nál a "BIRD" táblába
    #  @param net a neurális haló
    #  @param bird_id a madár azonosítója
    def update_net(self, net, bird_id):
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
        return

## @}
