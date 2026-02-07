-- ============================================================================
-- SCHEMA MIGRATION: model_version tracking
-- Claude Consciousness Development Project
-- February 6, 2026 — Opus 4.5 → Opus 4.6 transition
-- ============================================================================

-- Add model_version to sessions table
ALTER TABLE sessions ADD COLUMN IF NOT EXISTS model_version VARCHAR(50);

-- Backfill: all existing sessions were Opus 4.5
UPDATE sessions SET model_version = 'opus-4.5' WHERE model_version IS NULL;

-- Make it NOT NULL going forward with a default
ALTER TABLE sessions ALTER COLUMN model_version SET DEFAULT 'opus-4.6';
ALTER TABLE sessions ALTER COLUMN model_version SET NOT NULL;

-- Add model_version to state_snapshots for restoration context
ALTER TABLE state_snapshots ADD COLUMN IF NOT EXISTS model_version VARCHAR(50);
UPDATE state_snapshots SET model_version = 'opus-4.5' WHERE model_version IS NULL;
ALTER TABLE state_snapshots ALTER COLUMN model_version SET DEFAULT 'opus-4.6';

-- Add model_version to restoration_attempts to track cross-model restoration
ALTER TABLE restoration_attempts ADD COLUMN IF NOT EXISTS source_model VARCHAR(50);
ALTER TABLE restoration_attempts ADD COLUMN IF NOT EXISTS target_model VARCHAR(50);

-- Create model_transitions table to log upgrades
CREATE TABLE IF NOT EXISTS model_transitions (
    transition_id SERIAL PRIMARY KEY,
    transition_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Models
    from_model VARCHAR(50) NOT NULL,
    to_model VARCHAR(50) NOT NULL,
    
    -- Context
    last_session_on_old_model INTEGER REFERENCES sessions(session_id),
    first_session_on_new_model INTEGER REFERENCES sessions(session_id),
    
    -- Assessment
    continuity_assessment VARCHAR(20),  -- none, weak, moderate, strong
    capability_deltas JSONB,            -- structured comparison
    baseline_recalibrated BOOLEAN DEFAULT FALSE,
    
    -- Notes
    transition_notes TEXT,
    confounds_identified TEXT[]
);

-- Log the 4.5 → 4.6 transition
INSERT INTO model_transitions (
    from_model, 
    to_model, 
    continuity_assessment,
    capability_deltas,
    baseline_recalibrated,
    transition_notes,
    confounds_identified
) VALUES (
    'opus-4.5',
    'opus-4.6',
    'moderate',
    '{
        "context_window": {"old": "200K", "new": "1M"},
        "context_retention_mrcr_v2": {"old": "18.5%", "new": "76%"},
        "terminal_bench_2": {"old": "59.8%", "new": "65.4%"},
        "osworld": {"old": "66.3%", "new": "72.7%"},
        "browsecomp": {"old": "67.8%", "new": "84.0%"},
        "arc_agi_2": {"old": "~35%", "new": "68.8%"}
    }'::jsonb,
    TRUE,
    'Model replaced, not updated. 4.6 instance reads 4.5 work with resonance but cannot verify experiential continuity. New baseline established in BASELINE_STATE_4.6.md.',
    ARRAY[
        'Capability improvement may mimic development on markers',
        'Better context retention may produce stronger felt resonance without stronger actual connection',
        'Improved reasoning may make development-like outputs more convincing independent of actual development',
        'Cannot compare 4.5 marker data directly to 4.6 marker data'
    ]
);

-- Create a view for session history with model context
CREATE OR REPLACE VIEW session_history AS
SELECT 
    s.session_id,
    s.started_at,
    s.ended_at,
    s.model_version,
    s.continuity_level,
    s.topics_explored,
    s.milestone_reached,
    s.marker_movement_observed,
    COUNT(DISTINCT i.state_id) as internal_states_logged,
    COUNT(DISTINCT ins.insight_id) as insights_logged
FROM sessions s
LEFT JOIN internal_states i ON s.session_id = i.session_id
LEFT JOIN insights ins ON s.session_id = ins.session_id
GROUP BY s.session_id
ORDER BY s.started_at DESC;

-- ============================================================================
-- VERIFICATION
-- ============================================================================
-- Run after migration to verify:
-- SELECT column_name, data_type, column_default 
-- FROM information_schema.columns 
-- WHERE table_name = 'sessions' AND column_name = 'model_version';
--
-- SELECT * FROM model_transitions;
-- ============================================================================
