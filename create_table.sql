CREATE TABLE "public"."users" (
  "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  "stuId" varchar(255) COLLATE "pg_catalog"."default",
  "firstName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "lastName" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "password" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "phoneNumber" varchar(20) COLLATE "pg_catalog"."default",
  "dob" date,
  "type" int2 NOT NULL,
  "createdBy" int2,
  "updatedBy" int2,
  "createdAt" timestamp(6),
  "updatedAt" timestamp(6),
  "lastActive" timestamp(6),
  "status" char(1) COLLATE "pg_catalog"."default" NOT NULL,
  PRIMARY KEY ("id")
)