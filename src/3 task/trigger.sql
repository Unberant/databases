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

