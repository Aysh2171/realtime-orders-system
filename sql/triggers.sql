CREATE OR REPLACE FUNCTION notify_order_change()
RETURNS TRIGGER AS $$
DECLARE
    payload JSON;
BEGIN

    IF (TG_OP = 'DELETE') THEN
        payload = json_build_object(
            'operation', TG_OP,
            'data', row_to_json(OLD)
        );

    ELSE
        payload = json_build_object(
            'operation', TG_OP,
            'data', row_to_json(NEW)
        );

    END IF;

    PERFORM pg_notify(
        'order_changes',
        payload::text
    );

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER orders_change_trigger
AFTER INSERT OR UPDATE OR DELETE
ON orders
FOR EACH ROW
EXECUTE FUNCTION notify_order_change();

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_orders_timestamp
BEFORE UPDATE
ON orders
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();