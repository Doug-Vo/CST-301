DROP TABLE IF EXISTS api_function_specific;
DROP TABLE IF EXISTS functions_api;

CREATE TABLE functions_api(
    function_name TEXT,
    api_name TEXT, 
    PRIMARY KEY(function_name),
    CONSTRAINT fk_api_name
        FOREIGN KEY (api_name) 
        REFERENCES "API" (api_name)
        ON DELETE SET NULL
);

CREATE TABLE api_function_specific(
    function_name_fk TEXT, 
    api_name_fk TEXT, 
    api_context TEXT, 
    api_topic TEXT, 
    function_context TEXT, 
    function_topic TEXT, 
    llm_expert_API TEXT, 
    sim_expert_API TEXT, 
    llm_expert_function TEXT,
    sim_expert_function TEXT, 
    PRIMARY KEY (function_name_fk, api_name_fk),
    CONSTRAINT function_name_fk
        FOREIGN KEY (function_name_fk) 
        REFERENCES functions_api (function_name)
        ON DELETE SET NULL
);