-- Table: IoT.iot_device

-- DROP TABLE IF EXISTS "IoT".iot_device;

CREATE TABLE IF NOT EXISTS "IoT".iot_device
(
    id_device uuid NOT NULL,
    device_name text COLLATE pg_catalog."default",
    address integer NOT NULL,
    register text COLLATE pg_catalog."default",
    unit text COLLATE pg_catalog."default",
    range text COLLATE pg_catalog."default",
    type text COLLATE pg_catalog."default",
    CONSTRAINT "PK_ID_DEVICE" PRIMARY KEY (id_device)
        INCLUDE(id_device)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "IoT".iot_device
    OWNER to postgres;    

-- Table: IoT.iot-device-values

-- DROP TABLE IF EXISTS "IoT"."iot-device-values";

CREATE TABLE IF NOT EXISTS "IoT"."iot-device-values"
(
    "id-device_value" uuid NOT NULL,
    id_device uuid NOT NULL,
    dt_creation timestamp without time zone NOT NULL,
    value double precision NOT NULL,
    CONSTRAINT "PK_ID_DEVICE_VALUE" PRIMARY KEY ("id-device_value", id_device),
    CONSTRAINT "FK_ID_DEVICE" FOREIGN KEY (id_device)
        REFERENCES "IoT".iot_device (id_device) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "IoT"."iot-device-values"
    OWNER to postgres;
