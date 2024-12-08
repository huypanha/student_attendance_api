CREATE TABLE "public"."users" (
  "id" SERIAL PRIMARY KEY,
  "stuId" varchar(255),
  "firstName" varchar(255),
  "lastName" varchar(255),
  "email" varchar(255),
  "password" varchar(255),
  "phoneNumber" varchar(20),
  "dob" date,
  "type" int2 NOT NULL,
  "createdBy" int2,
  "updatedBy" int2,
  "createdAt" timestamp(6),
  "updatedAt" timestamp(6),
  "lastActive" timestamp(6),
  "status" char(1) NOT NULL
)

CREATE TABLE "public"."courses" (
    id SERIAL PRIMARY KEY,
    subject VARCHAR(255), 
    teacherId INT,
    description TEXT,
    img VARCHAR(255),
    createdBy INT,
    createdAt TIMESTAMP,
    updatedBy INT,
    updatedAt TIMESTAMP,
    status VARCHAR(50)
);

CREATE TABLE "public"."student_course" (
  "stuId" INT NOT NULL,
  "courseId" INT NOT NULL,
  "joinDate" TIMESTAMP NOT NULL,
  "createdBy" INT NOT NULL,
  PRIMARY KEY ("stuId", "courseId")
);