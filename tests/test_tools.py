import unittest
from unittest.mock import patch
from careerpilot.tools import (
    skill_gap_analysis,
    create_study_plan,
    find_learning_resources,
    execute_tool,
)

class ToolTests(unittest.TestCase):
    def test_skill_gap_identifies_data_analyst(self):
        result = skill_gap_analysis("Data Analyst internship", "Python, SQL")
        self.assertEqual(result["career"], "data analyst")
        self.assertIn("Python", result["skills_identified"])
        self.assertIn("Power BI or Tableau", result["skills_to_build"])

    def test_plan_has_requested_number_of_weeks(self):
        result = create_study_plan("Data Analyst", 3, "Python")
        self.assertEqual(len(result["plan"]), 3)
        self.assertEqual(result["plan"][0]["week"], 1)

    def test_weeks_are_bounded(self):
        self.assertEqual(len(create_study_plan("Software developer", 50)["plan"]), 12)
        self.assertEqual(len(create_study_plan("Software developer", 0)["plan"]), 1)

    def test_resources_return_links(self):
        result = find_learning_resources("SQL")
        self.assertTrue(result["resources"])
        self.assertTrue(all(item["url"].startswith("https://") for item in result["resources"]))

    def test_unapproved_tool_is_rejected(self):
        with self.assertRaises(ValueError):
            execute_tool("run_shell_command", {})

if __name__ == "__main__":
    unittest.main()
