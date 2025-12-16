```mermaid
flowchart TB
    User["User Prompt"] --> Planning["PLANNING"]
    Planning --> Research["RESEARCH"]
    Research --> ST["search_sensor_tower - Market and App Intelligence"] & SA["analyze_sentiment - Social Media Data"] & RC["check_regulatory_compliance - Region-specific Legal Check"] & Validation{"VALIDATION<br>Is data sufficient and reliable?"}
    ST L_ST_Research_0@--> Research
    SA L_SA_Research_0@--> Research
    RC L_RC_Research_0@--> Research
    Validation -- Yes --> Synthesis["SYNTHESIS"]
    Validation -- Retry / Partial --> Research
    Validation -- High Risk --> Human["HUMAN REVIEW"]
    Validation -- Unrecoverable --> Failed["FAILED"]
    Human -- Approved --> Synthesis
    Human -- Rejected --> Failed
    Synthesis --> Completed["COMPLETED"]
    Completed --> MRD["MRD JSON Output"]


    L_ST_Research_0@{ animation: slow } 
    L_SA_Research_0@{ animation: slow } 
    L_RC_Research_0@{ animation: slow }