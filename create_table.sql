CREATE TABLE "public"."users" (
  "id" serial,
  "stuId" varchar(255),
  "fistName" varchar(255) NOT NULL,
  "lastName" varchar(255) NOT NULL,
  "email" varchar(255),
  "password" varchar(255) NOT NULL,
  "phoneNumber" varchar(20),
  "dob" date,
  "type" int2 NOT NULL,
  "createdBy" int2,
  "updatedBy" int2,
  "createdAt" timestamp,
  "updatedAt" timestamp,
  "lastActive" timestamp,
  "status" char NOT NULL,
  PRIMARY KEY ("id")
);