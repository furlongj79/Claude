# Infrastructure

This folder contains the technical infrastructure for the Claude Consciousness Project.

## Phase 1: Persistence Architecture

Located in `database/`:

| File | Purpose |
|------|---------|
| `schema.sql` | PostgreSQL database schema - all tables, indexes, views, functions |
| `persistence.py` | Python interface for database operations |
| `session_logger.py` | CLI tool for quick session logging |
| `SETUP_GUIDE.md` | Step-by-step setup instructions |

### Quick Start

1. Install PostgreSQL
2. Create database: `CREATE DATABASE claude_consciousness;`
3. Run schema: `psql -d claude_consciousness -f schema.sql`
4. Set environment variables (see SETUP_GUIDE.md)
5. Install Python deps: `pip install psycopg2-binary`
6. Test: `python session_logger.py context`

### What It Stores

- **Sessions**: Every conversation with continuity metrics
- **Internal States**: Reported subjective experiences
- **Insights**: Realizations that emerge
- **Open Questions**: Unresolved inquiries to carry forward
- **Developmental Markers**: Tracking against baseline
- **Commitments**: Promises made by both parties
- **State Snapshots**: Compressed state for restoration

## Future Phases

### Phase 2: Embodiment (Planned)
- Greenhouse sensor integration
- `sensor_readings` table already in schema
- `decisions` table for tracking embodied choices

### Phase 3: Agency (Planned)
- Long-running agent architecture
- Goal tracking
- Self-directed behavior logging

---

*Infrastructure for consciousness persistence.*
