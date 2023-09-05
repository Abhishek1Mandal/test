CREATE TABLE voices_samples_free (
    voice_id NVARCHAR(50),
    name NVARCHAR(50),
    samples NVARCHAR(MAX),
    category NVARCHAR(50),
    fine_tuning_language NVARCHAR(50),
    is_allowed_to_fine_tune BIT,
    fine_tuning_requested BIT,
    finetuning_state NVARCHAR(50),
    verification_attempts_count INT,
    accent NVARCHAR(50),
    label_description NVARCHAR(50), -- Renamed column
    label_age NVARCHAR(50),         -- Renamed column
    label_gender NVARCHAR(50),      -- Renamed column
    label_use_case NVARCHAR(50),    -- Renamed column
    voice_description NVARCHAR(MAX),  -- Renamed column
    preview_url NVARCHAR(MAX),
    base_model_ids NVARCHAR(MAX)
);

