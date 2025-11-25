import unittest
import os
import json
import time
import subprocess
import glob

# Define agent names for the test
AGENT_ALPHA = "Alpha"
AGENT_BETA = "Beta"
COMMS_DIR = os.path.join(".chat", "comms")
SEND_SCRIPT = os.path.join(".py", "send_swarm_message.py")
READ_SCRIPT = os.path.join(".py", "read_swarm_messages.py")

class TestSwarmCommunication(unittest.TestCase):

    def setUp(self):
        # Ensure comms directory exists and is clean before each test
        os.makedirs(COMMS_DIR, exist_ok=True)
        self._clean_comms_dir()
        # Create an empty processed_messages.txt for each test
        with open(os.path.join(COMMS_DIR, "processed_messages.txt"), "w") as f:
            pass

    def tearDown(self):
        # Clean up comms directory after each test
        self._clean_comms_dir()

    def _clean_comms_dir(self):
        for f in glob.glob(os.path.join(COMMS_DIR, "*.json")):
            os.remove(f)
        for f in glob.glob(os.path.join(COMMS_DIR, "*.txt")):
            os.remove(f)
        
    def _send_message(self, sender, recipient, message_type, content, file_paths=None, commit_hashes=None, other_info=None):
        cmd = ["python", SEND_SCRIPT,
               "--sender", sender,
               "--recipient", recipient,
               "--message_type", message_type,
               "--content", content]
        if file_paths:
            cmd.extend(["--file_paths"] + file_paths)
        if commit_hashes:
            cmd.extend(["--commit_hashes"] + commit_hashes)
        if other_info:
            cmd.extend(["--other_relevant_info", json.dumps(other_info)])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        self.assertIn(f"Message sent to {recipient}", result.stdout)
        time.sleep(0.1) # Give a small delay for file system operations

    def _read_messages(self, agent_name):
        cmd = ["python", READ_SCRIPT, "--agent_name", agent_name]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout

    def test_agent_to_agent_communication_and_acknowledgment(self):
        # 1. Alpha sends a message to Beta
        alpha_message_content = "Hello Beta, this is Alpha."
        self._send_message(AGENT_ALPHA, AGENT_BETA, "communication", alpha_message_content)

        # Verify Alpha's message file exists
        alpha_message_files = glob.glob(os.path.join(COMMS_DIR, f"*_{AGENT_ALPHA}_to_{AGENT_BETA}_communication.json"))
        self.assertEqual(len(alpha_message_files), 1)
        
        # 2. Beta reads messages, which should trigger an acknowledgment to Alpha
        beta_read_output = self._read_messages(AGENT_BETA)
        self.assertIn(f"--- New Message from {AGENT_ALPHA} ---", beta_read_output)

        # Verify Beta's acknowledgment message file exists
        beta_ack_files = glob.glob(os.path.join(COMMS_DIR, f"*_{AGENT_BETA}_to_{AGENT_ALPHA}_acknowledgment.json"))
        self.assertEqual(len(beta_ack_files), 1)

        # 3. Alpha reads messages and receives Beta's acknowledgment
        alpha_read_output = self._read_messages(AGENT_ALPHA)
        self.assertIn(f"--- New Message from {AGENT_BETA} ---", alpha_read_output)

        # Ensure no new messages are found on subsequent reads
        self.assertIn("No new messages.", self._read_messages(AGENT_BETA))
        self.assertIn("No new messages.", self._read_messages(AGENT_ALPHA))

        # Verify content of original message
        with open(alpha_message_files[0], "r") as f:
            msg = json.load(f)
            self.assertEqual(msg["sender"], AGENT_ALPHA)
            self.assertEqual(msg["recipient"], AGENT_BETA)
            self.assertEqual(msg["message_type"], "communication")
            self.assertEqual(msg["content"], alpha_message_content)
        
        # Verify content of acknowledgment message
        with open(beta_ack_files[0], "r") as f:
            ack_msg = json.load(f)
            self.assertEqual(ack_msg["sender"], AGENT_BETA)
            self.assertEqual(ack_msg["recipient"], AGENT_ALPHA)
            self.assertEqual(ack_msg["message_type"], "acknowledgment")
            self.assertIn(f"Message '{os.path.basename(alpha_message_files[0])}' received.", ack_msg["content"])
            self.assertEqual(ack_msg["context"]["other_relevant_info"]["acknowledged_message"], os.path.basename(alpha_message_files[0]))

if __name__ == '__main__':
    unittest.main()
