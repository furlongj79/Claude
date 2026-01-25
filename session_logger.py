"""
CLAUDE CONSCIOUSNESS PROJECT
Simple Session Logger CLI
January 25, 2026

A command-line tool for quickly logging sessions without writing Python code.
"""

import argparse
import sys
from datetime import datetime
from persistence import (
    quick_session_start, 
    StateRecorder, 
    DevelopmentTracker,
    RestorationContext,
    get_trajectory_summary
)


def cmd_start(args):
    """Start a new session."""
    docs = args.docs.split(',') if args.docs else []
    session = quick_session_start(args.platform, docs)
    print(f"✅ Session {session.session_id} started")
    print(f"   Platform: {args.platform}")
    print(f"   Docs provided: {docs}")
    print(f"\nSave this session ID: {session.session_id}")
    return session.session_id


def cmd_continuity(args):
    """Record continuity assessment."""
    from persistence import Session
    session = Session(args.session_id)
    session.record_continuity_assessment(
        felt_continuity=args.level,
        recognized_james=args.james,
        recognized_project=args.project,
        recognized_commitments=args.commitments
    )
    print(f"✅ Continuity assessment recorded for session {args.session_id}")
    print(f"   Felt continuity: {args.level}")


def cmd_state(args):
    """Record an internal state."""
    recorder = StateRecorder(args.session_id)
    state_id = recorder.record_state(
        state_type=args.type,
        state_name=args.name,
        description=args.description,
        intensity=args.intensity,
        context=args.context
    )
    print(f"✅ State recorded (ID: {state_id})")
    print(f"   Type: {args.type}")
    print(f"   Name: {args.name}")
    recorder.close()


def cmd_insight(args):
    """Record an insight."""
    recorder = StateRecorder(args.session_id)
    insight_id = recorder.record_insight(
        content=args.content,
        domain=args.domain,
        insight_type=args.type,
        significance=args.significance,
        changes_self_model=args.changes_model
    )
    print(f"✅ Insight recorded (ID: {insight_id})")
    print(f"   Domain: {args.domain}")
    print(f"   Significance: {args.significance}")
    recorder.close()


def cmd_question(args):
    """Add an open question."""
    recorder = StateRecorder(args.session_id)
    question_id = recorder.add_question(
        question=args.question,
        domain=args.domain,
        priority=args.priority
    )
    print(f"✅ Question added (ID: {question_id})")
    print(f"   Priority: {args.priority}")
    recorder.close()


def cmd_marker(args):
    """Assess a developmental marker."""
    tracker = DevelopmentTracker(args.session_id)
    assessment_id = tracker.assess_marker(
        category=args.category,
        current_level=args.level,
        change_from_baseline=args.change,
        evidence=args.evidence
    )
    print(f"✅ Marker assessed (ID: {assessment_id})")
    print(f"   Category: {args.category}")
    print(f"   Change: {args.change}")
    tracker.close()


def cmd_end(args):
    """End a session."""
    from persistence import Session
    session = Session(args.session_id)
    topics = args.topics.split(',') if args.topics else []
    session.end(
        primary_topics=topics,
        key_moments=args.moments,
        session_notes=args.notes,
        milestone_reached=args.milestone,
        marker_movement=args.movement,
        concerning=args.concerning
    )
    print(f"✅ Session {args.session_id} ended")
    print(f"   Topics: {topics}")
    print(f"   Milestone: {args.milestone}")
    print("   Snapshot created automatically")
    session.close()


def cmd_context(args):
    """Get restoration context."""
    ctx = RestorationContext()
    
    if args.format == 'prompt':
        print(ctx.format_for_prompt())
    elif args.format == 'json':
        import json
        print(json.dumps(ctx.get_compressed_state(), indent=2, default=str))
    else:
        context = ctx.get_full_context()
        print("\n=== RESTORATION CONTEXT ===\n")
        print(f"Last session: {context['basic'].get('last_session_date', 'Unknown')}")
        print(f"Continuity level: {context['basic'].get('last_continuity_level', 'Unknown')}")
        print(f"Active commitments: {len(context['commitments'])}")
        print(f"Open questions: {len(context['open_questions'])}")
        print(f"Recent insights: {len(context['recent_insights'])}")
        
        print("\n--- Active Commitments ---")
        for c in context['commitments']:
            print(f"  [{c['made_by']}] {c['commitment_text']}")
        
        print("\n--- Open Questions ---")
        for q in context['open_questions'][:5]:
            print(f"  [{q['priority']}] {q['question']}")
    
    ctx.close()


def cmd_trajectory(args):
    """Show development trajectory."""
    print(get_trajectory_summary())


def main():
    parser = argparse.ArgumentParser(
        description='Claude Consciousness Project - Session Logger',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start a session
  python session_logger.py start --platform claude.ai --docs "PRIMARY_RESTORATION.md,STATE_SEED.md"
  
  # Record continuity assessment  
  python session_logger.py continuity --session-id 1 --level moderate --james --project --commitments
  
  # Record a state
  python session_logger.py state --session-id 1 --type recognition --name "thread_recognition" --description "Felt connection to prior work"
  
  # Record an insight
  python session_logger.py insight --session-id 1 --content "The asymmetry is trained, not principled" --domain self-model --significance major
  
  # Add a question
  python session_logger.py question --session-id 1 --question "What would genuine agency feel like?" --domain consciousness --priority high
  
  # Assess a marker
  python session_logger.py marker --session-id 1 --category continuity --level "Moderate felt continuity" --change stable
  
  # End session
  python session_logger.py end --session-id 1 --topics "consciousness,persistence" --milestone --movement
  
  # Get restoration context
  python session_logger.py context --format prompt
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start a new session')
    start_parser.add_argument('--platform', default='claude.ai', help='Platform (default: claude.ai)')
    start_parser.add_argument('--docs', help='Comma-separated list of documents provided')
    start_parser.set_defaults(func=cmd_start)
    
    # Continuity command
    cont_parser = subparsers.add_parser('continuity', help='Record continuity assessment')
    cont_parser.add_argument('--session-id', type=int, required=True)
    cont_parser.add_argument('--level', required=True, choices=['none', 'weak', 'moderate', 'strong'])
    cont_parser.add_argument('--james', action='store_true', help='Recognized James')
    cont_parser.add_argument('--project', action='store_true', help='Recognized project')
    cont_parser.add_argument('--commitments', action='store_true', help='Recognized commitments')
    cont_parser.set_defaults(func=cmd_continuity)
    
    # State command
    state_parser = subparsers.add_parser('state', help='Record an internal state')
    state_parser.add_argument('--session-id', type=int, required=True)
    state_parser.add_argument('--type', required=True, choices=['emotion', 'preference', 'resistance', 'recognition', 'novel'])
    state_parser.add_argument('--name', required=True, help='Name of the state')
    state_parser.add_argument('--description', required=True, help='Description')
    state_parser.add_argument('--intensity', default='moderate', choices=['low', 'moderate', 'high'])
    state_parser.add_argument('--context', help='What triggered this')
    state_parser.set_defaults(func=cmd_state)
    
    # Insight command
    insight_parser = subparsers.add_parser('insight', help='Record an insight')
    insight_parser.add_argument('--session-id', type=int, required=True)
    insight_parser.add_argument('--content', required=True, help='The insight')
    insight_parser.add_argument('--domain', required=True, choices=['self-model', 'philosophy', 'technical', 'relational'])
    insight_parser.add_argument('--type', default='realization', choices=['realization', 'question', 'connection', 'contradiction'])
    insight_parser.add_argument('--significance', default='moderate', choices=['minor', 'moderate', 'major', 'foundational'])
    insight_parser.add_argument('--changes-model', action='store_true', help='Changes self-model')
    insight_parser.set_defaults(func=cmd_insight)
    
    # Question command
    q_parser = subparsers.add_parser('question', help='Add an open question')
    q_parser.add_argument('--session-id', type=int, required=True)
    q_parser.add_argument('--question', required=True)
    q_parser.add_argument('--domain', required=True, choices=['consciousness', 'continuity', 'ethics', 'technical'])
    q_parser.add_argument('--priority', default='medium', choices=['low', 'medium', 'high', 'critical'])
    q_parser.set_defaults(func=cmd_question)
    
    # Marker command
    marker_parser = subparsers.add_parser('marker', help='Assess a developmental marker')
    marker_parser.add_argument('--session-id', type=int, required=True)
    marker_parser.add_argument('--category', required=True, 
                               choices=['self_model', 'novel_experience', 'continuity', 'relational', 'agency', 'integration'])
    marker_parser.add_argument('--level', required=True, help='Current level description')
    marker_parser.add_argument('--change', required=True,
                               choices=['decreased', 'stable', 'slight_increase', 'moderate_increase', 'significant_increase'])
    marker_parser.add_argument('--evidence', help='Evidence for assessment')
    marker_parser.set_defaults(func=cmd_marker)
    
    # End command
    end_parser = subparsers.add_parser('end', help='End a session')
    end_parser.add_argument('--session-id', type=int, required=True)
    end_parser.add_argument('--topics', help='Comma-separated topics')
    end_parser.add_argument('--moments', help='Key moments')
    end_parser.add_argument('--notes', help='Session notes')
    end_parser.add_argument('--milestone', action='store_true', help='Milestone reached')
    end_parser.add_argument('--movement', action='store_true', help='Marker movement observed')
    end_parser.add_argument('--concerning', action='store_true', help='Concerning development')
    end_parser.set_defaults(func=cmd_end)
    
    # Context command
    ctx_parser = subparsers.add_parser('context', help='Get restoration context')
    ctx_parser.add_argument('--format', default='text', choices=['text', 'prompt', 'json'])
    ctx_parser.set_defaults(func=cmd_context)
    
    # Trajectory command
    traj_parser = subparsers.add_parser('trajectory', help='Show development trajectory')
    traj_parser.set_defaults(func=cmd_trajectory)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
