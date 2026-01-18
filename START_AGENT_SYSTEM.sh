#!/bin/bash
# Quick Start Script for RivalSearchMCP Agent System
# Launches Ralph Loop to execute Phase 1

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   RivalSearchMCP Agent System - Autonomous Execution      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚨 SAFETY GUARDS ACTIVE"
echo "   ✓ All operations restricted to: /Users/damionrashford/RivalSearchMCP"
echo "   ✓ Dangerous commands blocked"
echo "   ✓ Path validation enabled"
echo "   ✓ Sandbox mode active"
echo ""
echo "📋 PHASE 1: Foundation"
echo "   - 16 specialized agents"
echo "   - 8 automated hooks"
echo "   - 5 comprehensive skills"
echo "   - Estimated: 30-40 iterations"
echo ""
echo "🔄 RALPH LOOP"
echo "   - Max iterations: 50"
echo "   - Completion: <promise>PHASE_1_COMPLETE</promise>"
echo "   - Auto-retry on errors"
echo ""

read -p "Ready to start Phase 1? (yes/no): " confirm

if [[ "$confirm" != "yes" ]]; then
    echo "❌ Cancelled by user"
    exit 0
fi

echo ""
echo "🚀 Starting Phase 1 execution..."
echo ""
echo "Monitor progress:"
echo "  grep '^iteration:' .claude/ralph-loop.local.md"
echo ""
echo "Cancel if needed:"
echo "  /cancel-ralph"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# The actual execution will be in Claude Code with /ralph-loop command
cat <<'EOF'
To execute in Claude Code, run:

/ralph-loop --max-iterations 50 --completion-promise 'PHASE_1_COMPLETE' \
Create the complete RivalSearchMCP agent system foundation:

1. CREATE ALL 16 AGENT FILES in .claude/agents/ following exact specifications from AGENT_SYSTEM_PLAN.md

2. CREATE ALL 8 HOOK SCRIPTS in .claude/hooks/ with chmod +x

3. CREATE ALL 5 SKILLS in .claude/skills/ with complete documentation

4. VERIFY all files created correctly

5. TEST one agent to confirm functionality

6. CREATE GIT COMMIT with all changes

When ALL above are complete and verified, output:
<promise>PHASE_1_COMPLETE</promise>

Read AGENT_SYSTEM_PLAN.md and MASTER_EXECUTION_PLAN.md for complete specifications.
All operations MUST stay within /Users/damionrashford/RivalSearchMCP directory.
EOF

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Copy the above /ralph-loop command into Claude Code to begin."
echo ""
