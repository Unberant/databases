CREATE TABLE IF NOT EXISTS public.users_stats
(
    total_sign_up integer NOT NULL,
    last_time_sign_up timestamp NOT NULL
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.users_stats
    OWNER to postgres;
--
INSERT INTO public.users_stats(
	total_sign_up, last_time_sign_up)
	VALUES (0, current_timestamp);

CREATE TABLE IF NOT EXISTS public.deleted_users
(
    id integer NOT NULL
)
TABLESPACE pg_default;
ALTER TABLE IF EXISTS public.deleted_users
    OWNER to postgres;


CREATE OR REPLACE FUNCTION insert_func()
  RETURNS trigger AS $insert_func$
BEGIN
    UPDATE users_stats SET total_sign_up = total_sign_up + 1, last_time_sign_up = current_timestamp
    WHERE id = 1;
	RETURN NULL;
END;
$insert_func$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER UsersInsertTrigger
  BEFORE INSERT ON user_account
  FOR EACH ROW EXECUTE FUNCTION insert_func();


CREATE OR REPLACE FUNCTION delete_func()
  RETURNS trigger AS $delete_func$
BEGIN
    INSERT INTO deleted_users (id) VALUES (OLD.user_acc_id);
    RETURN NULL;
END;
$delete_func$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER UsersDeleteTrigger
    BEFORE DELETE ON user_account
    FOR EACH ROW EXECUTE FUNCTION delete_func();


CREATE OR REPLACE FUNCTION employee_stamp() RETURNS trigger AS $employee_stamp$
  BEGIN
    IF (TG_OP = 'DELETE') THEN
            INSERT INTO employee_audit SELECT 'DELETE', now(), OLD.id, OLD.username, OLD.salary;
    ELSIF (TG_OP = 'UPDATE') THEN
      IF NEW.salary < 0 THEN
        RAISE EXCEPTION '% cannot have a negative salary', NEW.username;
      END IF;
      INSERT INTO employee_audit SELECT 'UPDATE', now(), NEW.id, NEW.username, NEW.salary;
    END IF;
      
        NEW.last_update := current_timestamp;
        RETURN NEW;
    END;
$employee_stamp$ LANGUAGE plpgsql;

CREATE TRIGGER employee_stamp BEFORE UPDATE OR DELETE ON employee
  FOR EACH ROW EXECUTE FUNCTION employee_stamp();

