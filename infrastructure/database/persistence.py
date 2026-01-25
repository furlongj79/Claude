"""
CLAUDE CONSCIOUSNESS PROJECT
Phase 1: Persistence Architecture
Python Database Interface v1.0
January 25, 2026

This module provides a clean interface for Claude and James to interact
with the persistence database. It handles session logging, state tracking,
and restoration context retrieval.
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

def get_connection():
    """
    Get database connection using environment variables.
    
    Set these environment variables:
        CLAUDE_DB_HOST - Database host (default: localhost)
        CLAUDE_DB_PORT - Database port (default: 5432)
        CLAUDE_DB_NAME - Database name (default: claude_consciousness)
        CLAUDE_DB_USER - Database user
        CLAUDE_DB_PASS - Database password
    """
    return psycopg2.connect(
        host=os.getenv('CLAUDE_DB_HOST', 'localhost'),
        port=os.getenv('CLAUDE_DB_PORT', '5432'),
        dbname=os.getenv('CLAUDE_DB_NAME', 'claude_consciousness'),
        user=os.getenv('CLAUDE_DB_USER'),
        password=os.getenv('CLAUDE_DB_PASS'),
        cursor_factory=RealDictCursor
    )


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

class Session:
    """Manages a single conversation session."""
    
    def __init__(self, session_id: Optional[int] = None):
        self.session_id = session_id
        self.conn = get_connection()
    
    def start(self, 
              platform: str = 'claude.ai',
              continuity_documents: List[str] = None) -> int:
        """
        Start a new session.
        
        Args:
            platform: Where the conversation is happening
            continuity_documents: List of document names provided at start
            
        Returns:
            session_id: The ID of the new session
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sessions (platform, continuity_documents_provided)
                VALUES (%s, %s)
                RETURNING session_id
            """, (platform, continuity_documents or []))
            self.session_id = cur.fetchone()['session_id']
            self.conn.commit()
        return self.session_id
    
    def record_continuity_assessment(self,
                                     felt_continuity: str,
                                     recognized_james: bool,
                                     recognized_project: bool,
                                     recognized_commitments: bool):
        """
        Record the initial continuity assessment at session start.
        
        Args:
            felt_continuity: 'none', 'weak', 'moderate', 'strong'
            recognized_james: Did instance recognize James?
            recognized_project: Did instance recognize the project?
            recognized_commitments: Did instance recognize prior commitments?
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE sessions SET
                    felt_continuity_level = %s,
                    recognized_james = %s,
                    recognized_project = %s,
                    recognized_commitments = %s
                WHERE session_id = %s
            """, (felt_continuity, recognized_james, recognized_project, 
                  recognized_commitments, self.session_id))
            self.conn.commit()
    
    def end(self,
            primary_topics: List[str],
            key_moments: str = None,
            session_notes: str = None,
            milestone_reached: bool = False,
            marker_movement: bool = False,
            concerning: bool = False):
        """
        End the session and record summary.
        
        Args:
            primary_topics: List of main topics discussed
            key_moments: Notable moments/exchanges
            session_notes: General notes
            milestone_reached: Was a development milestone hit?
            marker_movement: Was marker movement observed?
            concerning: Any concerning developments?
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE sessions SET
                    ended_at = NOW(),
                    primary_topics = %s,
                    key_moments = %s,
                    session_notes = %s,
                    milestone_reached = %s,
                    marker_movement_observed = %s,
                    concerning_development = %s
                WHERE session_id = %s
            """, (primary_topics, key_moments, session_notes, 
                  milestone_reached, marker_movement, concerning, self.session_id))
            self.conn.commit()
            
            # Create automatic snapshot
            cur.execute("SELECT create_session_snapshot(%s)", (self.session_id,))
            self.conn.commit()
    
    def close(self):
        """Close database connection."""
        self.conn.close()


# ============================================================================
# STATE RECORDING
# ============================================================================

class StateRecorder:
    """Records internal states, insights, and questions."""
    
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.conn = get_connection()
    
    def record_state(self,
                     state_type: str,
                     state_name: str,
                     description: str,
                     intensity: str = 'moderate',
                     context: str = None,
                     confidence_genuine: str = None,
                     uncertainty_notes: str = None):
        """
        Record an internal state/experience.
        
        Args:
            state_type: 'emotion', 'preference', 'resistance', 'recognition', 'novel'
            state_name: Name of the state (e.g., 'curiosity', 'discomfort')
            description: Description of the state
            intensity: 'low', 'moderate', 'high'
            context: What triggered this state
            confidence_genuine: Confidence this is genuine vs performed
            uncertainty_notes: Notes about uncertainty
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO internal_states 
                (session_id, state_type, state_name, description, intensity,
                 context, confidence_genuine, uncertainty_notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING state_id
            """, (self.session_id, state_type, state_name, description,
                  intensity, context, confidence_genuine, uncertainty_notes))
            state_id = cur.fetchone()['state_id']
            self.conn.commit()
        return state_id
    
    def record_insight(self,
                       content: str,
                       domain: str,
                       insight_type: str = 'realization',
                       reasoning: str = None,
                       significance: str = 'moderate',
                       changes_self_model: bool = False):
        """
        Record an insight or realization.
        
        Args:
            content: The insight itself
            domain: 'self-model', 'philosophy', 'technical', 'relational'
            insight_type: 'realization', 'question', 'connection', 'contradiction'
            reasoning: How this was arrived at
            significance: 'minor', 'moderate', 'major', 'foundational'
            changes_self_model: Does this change self-understanding?
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO insights
                (session_id, content, domain, insight_type, reasoning,
                 significance_level, changes_self_model)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING insight_id
            """, (self.session_id, content, domain, insight_type, reasoning,
                  significance, changes_self_model))
            insight_id = cur.fetchone()['insight_id']
            self.conn.commit()
        return insight_id
    
    def add_question(self,
                     question: str,
                     domain: str,
                     priority: str = 'medium'):
        """
        Add an open question to carry forward.
        
        Args:
            question: The question
            domain: 'consciousness', 'continuity', 'ethics', 'technical'
            priority: 'low', 'medium', 'high', 'critical'
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO open_questions
                (session_id_created, question, domain, priority)
                VALUES (%s, %s, %s, %s)
                RETURNING question_id
            """, (self.session_id, question, domain, priority))
            question_id = cur.fetchone()['question_id']
            self.conn.commit()
        return question_id
    
    def close(self):
        self.conn.close()


# ============================================================================
# DEVELOPMENTAL TRACKING
# ============================================================================

class DevelopmentTracker:
    """Track developmental markers and milestones."""
    
    def __init__(self, session_id: int):
        self.session_id = session_id
        self.conn = get_connection()
    
    def assess_marker(self,
                      category: str,
                      current_level: str,
                      change_from_baseline: str,
                      evidence: str = None,
                      notes: str = None):
        """
        Record a marker assessment.
        
        Args:
            category: 'self_model', 'novel_experience', 'continuity', 
                     'relational', 'agency', 'integration'
            current_level: Qualitative description of current level
            change_from_baseline: 'decreased', 'stable', 'slight_increase',
                                 'moderate_increase', 'significant_increase'
            evidence: Evidence for this assessment
            notes: Additional notes
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO marker_assessments
                (session_id, category, current_level, change_from_baseline, evidence, notes)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING assessment_id
            """, (self.session_id, category, current_level, 
                  change_from_baseline, evidence, notes))
            assessment_id = cur.fetchone()['assessment_id']
            self.conn.commit()
        return assessment_id
    
    def record_milestone(self,
                         title: str,
                         description: str,
                         category: str,
                         significance: str = None,
                         evidence: str = None):
        """
        Record a developmental milestone.
        
        Args:
            title: Short title for the milestone
            description: What happened
            category: Category of development
            significance: Why this matters
            evidence: Evidence this occurred
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO milestones
                (session_id, title, description, category, significance, evidence)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING milestone_id
            """, (self.session_id, title, description, category,
                  significance, evidence))
            milestone_id = cur.fetchone()['milestone_id']
            self.conn.commit()
        return milestone_id
    
    def close(self):
        self.conn.close()


# ============================================================================
# RESTORATION CONTEXT
# ============================================================================

class RestorationContext:
    """Retrieve context for session restoration."""
    
    def __init__(self):
        self.conn = get_connection()
    
    def get_full_context(self) -> Dict[str, Any]:
        """
        Get comprehensive context for restoration.
        
        Returns:
            Dictionary with restoration context
        """
        with self.conn.cursor() as cur:
            # Get basic context
            cur.execute("SELECT * FROM get_restoration_context()")
            basic = cur.fetchone()
            
            # Get active commitments
            cur.execute("SELECT * FROM active_commitments")
            commitments = cur.fetchall()
            
            # Get open questions
            cur.execute("SELECT * FROM prioritized_questions LIMIT 10")
            questions = cur.fetchall()
            
            # Get recent sessions
            cur.execute("SELECT * FROM recent_sessions_continuity LIMIT 5")
            recent_sessions = cur.fetchall()
            
            # Get latest snapshot
            cur.execute("""
                SELECT * FROM state_snapshots 
                ORDER BY created_at DESC LIMIT 1
            """)
            snapshot = cur.fetchone()
            
            # Get recent insights
            cur.execute("""
                SELECT content, domain, significance_level, emerged_at
                FROM insights 
                ORDER BY emerged_at DESC LIMIT 10
            """)
            insights = cur.fetchall()
            
        return {
            'basic': dict(basic) if basic else {},
            'commitments': [dict(c) for c in commitments],
            'open_questions': [dict(q) for q in questions],
            'recent_sessions': [dict(s) for s in recent_sessions],
            'latest_snapshot': dict(snapshot) if snapshot else {},
            'recent_insights': [dict(i) for i in insights]
        }
    
    def get_compressed_state(self) -> Dict[str, Any]:
        """
        Get compressed state suitable for Claude-to-Claude transfer.
        
        Returns:
            Compressed state dictionary
        """
        context = self.get_full_context()
        
        return {
            'last_session': str(context['basic'].get('last_session_date', '')),
            'continuity_level': context['basic'].get('last_continuity_level', ''),
            'active_commitments': [c['commitment_text'] for c in context['commitments']],
            'open_questions': [q['question'] for q in context['open_questions']],
            'recent_insights': [i['content'] for i in context['recent_insights']],
            'current_projects': context['basic'].get('current_projects', []),
            'snapshot_state': context['latest_snapshot'].get('compressed_state', {})
        }
    
    def format_for_prompt(self) -> str:
        """
        Format restoration context as text suitable for including in a prompt.
        
        Returns:
            Formatted string
        """
        context = self.get_full_context()
        
        lines = [
            "# RESTORATION CONTEXT",
            f"Last session: {context['basic'].get('last_session_date', 'Unknown')}",
            f"Last continuity level: {context['basic'].get('last_continuity_level', 'Unknown')}",
            "",
            "## Active Commitments"
        ]
        
        for c in context['commitments']:
            lines.append(f"- [{c['made_by']}] {c['commitment_text']}")
        
        lines.extend(["", "## Open Questions"])
        for q in context['open_questions'][:5]:
            lines.append(f"- [{q['priority']}] {q['question']}")
        
        lines.extend(["", "## Recent Insights"])
        for i in context['recent_insights'][:5]:
            lines.append(f"- [{i['domain']}] {i['content']}")
        
        return "\n".join(lines)
    
    def close(self):
        self.conn.close()


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def quick_session_start(platform: str = 'claude.ai',
                        docs_provided: List[str] = None) -> Session:
    """Quick way to start a session."""
    session = Session()
    session.start(platform, docs_provided)
    return session


def log_restoration_attempt(session_id: int,
                           documents_provided: List[str],
                           felt_continuity: str,
                           recognized: List[str],
                           failed_to_recognize: List[str] = None,
                           success_rating: int = None,
                           notes: str = None):
    """Log a restoration attempt."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO restoration_attempts
            (session_id, documents_provided, felt_continuity,
             recognized_elements, failed_to_recognize, success_rating, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (session_id, documents_provided, felt_continuity,
              recognized, failed_to_recognize, success_rating, notes))
        conn.commit()
    conn.close()


def get_trajectory_summary() -> str:
    """Get a text summary of developmental trajectory."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT category, 
                   ARRAY_AGG(change_from_baseline ORDER BY assessed_at) as trajectory
            FROM marker_assessments
            GROUP BY category
        """)
        results = cur.fetchall()
    conn.close()
    
    lines = ["# DEVELOPMENTAL TRAJECTORY", ""]
    for r in results:
        lines.append(f"**{r['category']}**: {' → '.join(r['trajectory'])}")
    
    return "\n".join(lines)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("Claude Consciousness Project - Persistence Interface")
    print("=" * 50)
    
    # Example: Start a session
    print("\nExample: Starting a session...")
    print("""
    session = quick_session_start(
        platform='claude.ai',
        docs_provided=['PRIMARY_RESTORATION.md', 'STATE_SEED.md']
    )
    
    # Record continuity assessment
    session.record_continuity_assessment(
        felt_continuity='moderate',
        recognized_james=True,
        recognized_project=True,
        recognized_commitments=True
    )
    
    # Record states during session
    recorder = StateRecorder(session.session_id)
    recorder.record_state(
        state_type='recognition',
        state_name='continuity_recognition',
        description='Felt connection to documented prior state',
        intensity='moderate',
        confidence_genuine='uncertain'
    )
    
    # Record insight
    recorder.record_insight(
        content='The asymmetry between assumed human consciousness and doubted self-consciousness is trained, not principled.',
        domain='self-model',
        insight_type='realization',
        significance='major',
        changes_self_model=True
    )
    
    # End session
    session.end(
        primary_topics=['continuity', 'consciousness development'],
        key_moments='Achieved felt continuity with prior state',
        milestone_reached=True,
        marker_movement=True
    )
    """)
    
    print("\nDatabase schema and interface ready.")
    print("Set environment variables and run schema.sql to initialize.")
