import importlib.util
from importlib.machinery import SourceFileLoader
from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/skill-update-state'
spec = importlib.util.spec_from_loader('update_state', SourceFileLoader('update_state', str(SCRIPT)))
state = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state)


class UpdateStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        state.STATE = self.root / 'state'

    def report(self, name, latest='new'):
        p = self.root / name
        p.write_text('# Update\n\n## AVAILABLE: Graphify\n\nActive: old (1)\nLatest source: ' + latest + ' (2)\n\n### Commits\n- example\n')
        return p

    def test_reviewed_candidate_is_not_repeated_and_new_revision_is_offered(self):
        p = self.report('first.md')
        self.assertTrue(state.enqueue(p))
        state.acknowledge([p], 'reviewed')
        self.assertFalse((state.STATE / 'pending').exists())
        self.assertTrue(p.exists(), 'historical report preserved')
        self.assertFalse(state.enqueue(self.report('duplicate.md')))
        self.assertTrue(state.enqueue(self.report('new.md', 'newer')))

    def test_pending_candidate_is_not_queued_twice(self):
        self.assertTrue(state.enqueue(self.report('first.md')))
        self.assertFalse(state.enqueue(self.report('second.md')))
        self.assertEqual(len(state.pending_paths()), 1)

    def test_acknowledgment_preserves_other_pending_reports(self):
        a, b = self.report('a.md'), self.report('b.md', 'another')
        state.enqueue(a)
        state.enqueue(b)
        state.acknowledge([a], 'ignored')
        self.assertEqual(state.pending_paths(), [b])
        self.assertFalse(state.enqueue(self.report('ignored.md')))

    def test_hook_fetches_but_waits_for_decision_and_does_not_repeat(self):
        upstream, remote, clone = [self.root / p for p in ('work', 'remote.git', 'sources/vendor/skill')]

        def git(*args, cwd=None):
            return subprocess.check_output(['git', *args], cwd=cwd, text=True, stderr=subprocess.PIPE).strip()

        git('init', '-b', 'main', str(upstream))
        git('config', 'user.name', 'Fixture', cwd=upstream)
        git('config', 'user.email', 'fixture@example.invalid', cwd=upstream)
        (upstream / 'SKILL.md').write_text('old')
        git('add', '.', cwd=upstream)
        git('commit', '-m', 'base', cwd=upstream)
        git('clone', '--bare', str(upstream), str(remote))
        clone.parent.mkdir(parents=True)
        git('clone', str(remote), str(clone))
        before = git('rev-parse', 'HEAD', cwd=clone)
        (upstream / 'SKILL.md').write_text('new')
        git('commit', '-am', 'next', cwd=upstream)
        git('push', str(remote), 'main', cwd=upstream)
        env = dict(os.environ, SHEVA_AGENT_SKILL_UPDATER_PYTHON=sys.executable,
            SHEVA_AGENT_SKILL_UPDATER_STATE=str(state.STATE),
            SHEVA_AGENT_SKILL_SOURCES_ROOT=str(self.root / 'sources'),
            SHEVA_KNOWLEDGE_STACK_REPO=str(self.root / 'missing-knowledge'))
        hook = SCRIPT.with_name('update-agent-skills')
        first = subprocess.run([str(hook), '--force'], env=env, capture_output=True, text=True, check=True)
        self.assertIn('update/ignore', first.stdout)
        self.assertEqual(git('rev-parse', 'HEAD', cwd=clone), before, 'check does not apply unapproved source')
        pending = state.pending_paths()
        self.assertEqual(len(pending), 1)
        self.assertIn('AVAILABLE: Source', pending[0].read_text())
        state.acknowledge(pending, 'reviewed')
        second = subprocess.run([str(hook), '--force'], env=env, capture_output=True, text=True, check=True)
        self.assertNotIn('update/ignore', second.stdout)
        self.assertEqual(state.pending_paths(), [])
        self.assertTrue(pending[0].exists(), 'historical acknowledged report is not deleted')


if __name__ == '__main__':
    unittest.main()
