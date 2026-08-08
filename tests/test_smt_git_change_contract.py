from __future__ import annotations

import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'scripts'/'smt_git_change_contract.py'
S=importlib.util.spec_from_file_location('git_contract',P);assert S and S.loader
g=importlib.util.module_from_spec(S);S.loader.exec_module(g)

class GitContractTests(unittest.TestCase):
    def repo(self):
        r=Path(tempfile.mkdtemp());subprocess.run(['git','init','-q'],cwd=r,check=True)
        subprocess.run(['git','config','user.name','T'],cwd=r,check=True);subprocess.run(['git','config','user.email','t@example.invalid'],cwd=r,check=True)
        return r
    def commit(self,r,msg):
        subprocess.run(['git','add','-A'],cwd=r,check=True);subprocess.run(['git','commit','-qm',msg],cwd=r,check=True)
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip()
    def deltas(self,r,b): return g.commit_deltas(r,b)[1]
    def test_add_regular_A(self):
        r=self.repo();(r/'base').write_text('x');b=self.commit(r,'base');(r/'a').write_text('a');self.commit(r,'add')
        d=self.deltas(r,b);self.assertEqual([('A','a','000000','100644')],[(x.status,x.path,x.old_mode,x.new_mode) for x in d])
    def test_modify_regular_M(self):
        r=self.repo();p=r/'a';p.write_text('x');b=self.commit(r,'base');p.write_text('y');self.commit(r,'m');d=self.deltas(r,b);self.assertEqual('M',d[0].status)
    def test_delete_D(self):
        r=self.repo();p=r/'a';p.write_text('x');b=self.commit(r,'base');p.unlink();self.commit(r,'d');d=self.deltas(r,b);self.assertEqual(('D','100644','000000'),(d[0].status,d[0].old_mode,d[0].new_mode))
    def test_regular_to_symlink_T(self):
        r=self.repo();p=r/'a';p.write_text('x');b=self.commit(r,'base');p.unlink();p.symlink_to('target');self.commit(r,'t');d=self.deltas(r,b);self.assertEqual(('T','100644','120000'),(d[0].status,d[0].old_mode,d[0].new_mode))
    def test_symlink_to_regular_T(self):
        r=self.repo();p=r/'a';p.symlink_to('target');b=self.commit(r,'base');p.unlink();p.write_text('x');self.commit(r,'t');d=self.deltas(r,b);self.assertEqual(('T','120000','100644'),(d[0].status,d[0].old_mode,d[0].new_mode))
    def test_mode_only_is_M_with_modes(self):
        r=self.repo();p=r/'a';p.write_text('x');b=self.commit(r,'base');p.chmod(0o755);self.commit(r,'mode');d=self.deltas(r,b);self.assertEqual(('M','100644','100755'),(d[0].status,d[0].old_mode,d[0].new_mode))
    def test_rename_is_D_plus_A(self):
        r=self.repo();p=r/'old';p.write_text('x');b=self.commit(r,'base');p.rename(r/'new');self.commit(r,'rename');d=self.deltas(r,b);self.assertEqual([('A','new'),('D','old')],sorted((x.status,x.path) for x in d))
    def test_case_rename_is_D_plus_A(self):
        r=self.repo();p=r/'old';p.write_text('x');b=self.commit(r,'base');p.rename(r/'OLD');self.commit(r,'rename');d=self.deltas(r,b);self.assertEqual([('A','OLD'),('D','old')],sorted((x.status,x.path) for x in d))
    def test_file_to_tree_is_D_plus_A_child(self):
        r=self.repo();p=r/'x';p.write_text('x');b=self.commit(r,'base');p.unlink();p.mkdir();(p/'a').write_text('a');self.commit(r,'replace');d=self.deltas(r,b);self.assertEqual([('A','x/a'),('D','x')],sorted((x.status,x.path) for x in d))
    def test_tree_to_file_is_D_child_plus_A_file(self):
        r=self.repo();p=r/'x';p.mkdir();(p/'a').write_text('a');b=self.commit(r,'base');(p/'a').unlink();p.rmdir();p.write_text('x');self.commit(r,'replace');d=self.deltas(r,b);self.assertEqual([('A','x'),('D','x/a')],sorted((x.status,x.path) for x in d))
    def test_gitlink_add_and_modify(self):
        # Build a local sub-repository and add it as a gitlink without network access.
        sub=self.repo();(sub/'f').write_text('1');s1=self.commit(sub,'s1')
        r=self.repo();(r/'base').write_text('x');b=self.commit(r,'base')
        subprocess.run(['git','-c','protocol.file.allow=always','submodule','add','-q',str(sub),'mod'],cwd=r,check=True);self.commit(r,'add sub')
        d=self.deltas(r,b);mod=next(x for x in d if x.path=='mod');self.assertEqual(('A','160000'),(mod.status,mod.new_mode))
        (sub/'f').write_text('2');s2=self.commit(sub,'s2');subprocess.run(['git','fetch','-q'],cwd=r/'mod',check=True);subprocess.run(['git','checkout','-q',s2],cwd=r/'mod',check=True);b2=subprocess.check_output(['git','rev-parse','HEAD'],cwd=r,text=True).strip();self.commit(r,'move sub')
        d2=self.deltas(r,b2);mod2=next(x for x in d2 if x.path=='mod');self.assertEqual(('M','160000','160000'),(mod2.status,mod2.old_mode,mod2.new_mode))
    def test_regular_to_gitlink_T(self):
        sub=self.repo();(sub/'f').write_text('1');self.commit(sub,'s')
        r=self.repo();p=r/'mod';p.write_text('x');b=self.commit(r,'base');subprocess.run(['git','rm','-q','mod'],cwd=r,check=True)
        subprocess.run(['git','-c','protocol.file.allow=always','submodule','add','-q',str(sub),'mod'],cwd=r,check=True);self.commit(r,'t')
        d=self.deltas(r,b);mod=next(x for x in d if x.path=='mod');self.assertEqual(('T','100644','160000'),(mod.status,mod.old_mode,mod.new_mode))
    def test_prohibited_control_character_path_fails_closed(self):
        r=self.repo();(r/'base').write_text('x');b=self.commit(r,'base');(r/'bad\nname').write_text('x');self.commit(r,'bad')
        with self.assertRaises(g.GitContractError): g.commit_deltas(r,b)

    def test_printable_unicode_path_is_supported(self):
        r=self.repo();(r/'base').write_text('x');b=self.commit(r,'base');name='snowman-\u2603';(r/name).write_text('x');self.commit(r,'unicode')
        d=self.deltas(r,b);self.assertEqual([('A',name)],[(x.status,x.path) for x in d if x.path==name])

    def test_invalid_utf8_raw_path_fails_closed(self):
        raw=b':000000 100644 '+b'0'*64+b' '+b'a'*64+b' A\x00'+b'bad-\xff-name'+b'\x00'
        with self.assertRaises(g.GitContractError):g.parse_raw_diff_z(raw)

    def test_parse_rejects_unsupported_status(self):
        raw=b':100644 100644 '+b'a'*40+b' '+b'b'*40+b' U\x00x\x00'
        with self.assertRaises(g.GitContractError):g.parse_raw_diff_z(raw)
    def test_parse_rejects_malformed_output(self):
        with self.assertRaises(g.GitContractError):g.parse_raw_diff_z(b'bad\x00x\x00')
    def test_head_regular_blob(self):
        r=self.repo();p=r/'a';p.write_text('x');self.commit(r,'c');e=g.require_head_regular_blob(r,'a');self.assertEqual('100644',e.mode)
    def test_head_symlink_rejected(self):
        r=self.repo();p=r/'a';p.symlink_to('x');self.commit(r,'c')
        with self.assertRaises(g.GitContractError):g.require_head_regular_blob(r,'a')
    def test_bad_base_fails_closed(self):
        r=self.repo();(r/'a').write_text('x');self.commit(r,'c')
        with self.assertRaises(g.GitContractError):g.commit_deltas(r,'not-a-ref')

if __name__=='__main__':unittest.main()

class GitIdentityContractTests(unittest.TestCase):
    def repo(self):
        r=Path(tempfile.mkdtemp());subprocess.run(['git','init','-q'],cwd=r,check=True)
        subprocess.run(['git','config','user.name','T'],cwd=r,check=True);subprocess.run(['git','config','user.email','t@example.invalid'],cwd=r,check=True)
        (r/'a').write_text('x');subprocess.run(['git','add','-A'],cwd=r,check=True);subprocess.run(['git','commit','-qm','base'],cwd=r,check=True)
        return r
    def test_resolve_commit_and_head_tree(self):
        repo = self.repo()
        head = g.resolve_commit(repo, "HEAD")
        observed_head, tree = g.head_commit_and_tree(repo)
        self.assertEqual(head, observed_head)
        self.assertRegex(head, r"^[0-9a-f]{40,64}$")
        self.assertRegex(tree, r"^[0-9a-f]{40,64}$")
    def test_resolve_commit_bad_ref_fails_closed(self):
        repo = self.repo()
        with self.assertRaises(g.GitContractError):
            g.resolve_commit(repo, "refs/heads/__missing__")
