import unittest
import os
import json
import subprocess
from unittest.mock import patch, MagicMock, mock_open
from generate_clean_project_structure import get_git_files, build_tree

class TestGenerateCleanProjectStructure(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_git_files(self, mock_subprocess_run):
        mock_subprocess_run.return_value = MagicMock(
            stdout="file1.txt\ndir1/file2.txt\ndir1/subdir/file3.txt\n",
            stderr="",
            returncode=0
        )
        expected_files = ["file1.txt", "dir1/file2.txt", "dir1/subdir/file3.txt"]
        self.assertEqual(get_git_files("/mock/project/path"), expected_files) # Pass a mock path
        mock_subprocess_run.assert_called_once_with(['git', 'ls-files'], cwd="/mock/project/path", capture_output=True, text=True, check=True)

    @patch('subprocess.run')
    def test_get_git_files_error(self, mock_subprocess_run):
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'git ls-files', stderr='error')
        self.assertEqual(get_git_files("/mock/project/path"), []) # Pass a mock path
        mock_subprocess_run.assert_called_once_with(['git', 'ls-files'], cwd="/mock/project/path", capture_output=True, text=True, check=True)

    def test_build_tree_simple(self):
        files = ["file1.txt", "dir1/file2.txt"]
        expected_tree = {
            "file1.txt": "file",
            "dir1/": {
                "file2.txt": "file"
            }
        }
        self.assertEqual(build_tree(files), expected_tree)

    def test_build_tree_nested(self):
        files = ["dir1/subdir1/file1.txt", "dir1/subdir2/file2.txt"]
        expected_tree = {
            "dir1/": {
                "subdir1/": {
                    "file1.txt": "file"
                },
                "subdir2/": {
                    "file2.txt": "file"
                }
            }
        }
        self.assertEqual(build_tree(files), expected_tree)

    def test_build_tree_empty(self):
        self.assertEqual(build_tree([]), {})

        @patch('generate_clean_project_structure.get_git_files') # Mock the function itself
        @patch('subprocess.run')
        def test_full_script_execution(self, mock_subprocess_run, mock_get_git_files):
            # Configure mock_subprocess_run for git rev-parse
            mock_subprocess_run.return_value = MagicMock(
                stdout="mock_project_root\n",
                stderr="",
                returncode=0
            )
            mock_get_git_files.return_value = ["fileA.txt", "folderB/fileC.txt"]
    
            with patch('os.path.join', side_effect=lambda *args: '/'.join(args)) as mock_os_path_join:
                mock_open_func = mock_open()
                with patch('builtins.open', mock_open_func):
                    with patch('sys.argv', ['generate_clean_project_structure.py']):
                        import importlib
                        import generate_clean_project_structure
                        importlib.reload(generate_clean_project_structure)
                        
                        mock_subprocess_run.assert_called_once_with(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True)
                        mock_get_git_files.assert_called_once_with("mock_project_root")
                        mock_os_path_join.assert_any_call('mock_project_root', '.memory', 'project_structure.json')
                        written_content = mock_open_func().write.call_args[0][0]
                        parsed_content = json.loads(written_content)
                        expected_structure = {
                            "project_structure": {
                                "fileA.txt": "file",
                                "folderB/": {
                                    "fileC.txt": "file"
                                }
                            }
                        }
                        self.assertEqual(parsed_content, expected_structure)


if __name__ == '__main__':
    unittest.main()
