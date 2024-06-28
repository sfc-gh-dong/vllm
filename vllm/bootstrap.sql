USE ROLE SYSADMIN;
CREATE DATABASE IF NOT EXISTS LLM;
USE DATABASE LLM;

CREATE COMPUTE POOL GPU_NV_M
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = GPU_NV_M;

CREATE OR REPLACE IMAGE REPOSITORY images;

-- Stage to store LLM models
CREATE OR REPLACE STAGE models
 DIRECTORY = (ENABLE = TRUE)
 ENCRYPTION = (TYPE='SNOWFLAKE_SSE');

-- Stage to store yaml specs
CREATE OR REPLACE STAGE specs
 DIRECTORY = (ENABLE = TRUE)
 ENCRYPTION = (TYPE='SNOWFLAKE_SSE');

CREATE OR REPLACE NETWORK RULE hugging_face_network
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('0.0.0.0');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION hugging_face_integration
  ALLOWED_NETWORK_RULES = (hugging_face_network)
  ENABLED = TRUE;