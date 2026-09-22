import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("live_docs_smoke", ROOT / "scripts/live_docs_smoke.py")
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class LiveDocsSmokeTests(unittest.TestCase):
    def responses(self):
        annotations = dict(readOnlyHint=True, destructiveHint=False,
                           idempotentHint=True, openWorldHint=False)
        return [
            {"protocolVersion": smoke.PROTOCOL_VERSION, "serverInfo": {"name": "popscale-docs"}},
            {"tools": [{"name": name, "annotations": annotations} for name in
                       ("get_docs_overview", "search_docs", "get_pages")]},
            {"structuredContent": {"results": [{"path": smoke.CANONICAL_PATH}]}},
            {"structuredContent": {"pages": [{"path": smoke.CANONICAL_PATH,
                                             "status": "published", "markdown": "# Guide"}]}},
            {"resources": [{"uri": "docs://overview"}, {"uri": smoke.PAGE_RESOURCE_URI}]},
        ]

    def test_current_guide_is_searched_fetched_and_listed(self):
        with patch.object(smoke, "rpc", side_effect=self.responses()) as rpc, patch("builtins.print"):
            smoke.main()
        self.assertEqual(rpc.call_args_list[3].args[2]["arguments"],
                         {"paths": ["/integrations/connect-assistant/"]})

    def test_tool_error_cannot_pass_by_echoing_path_or_status(self):
        for index, name in ((2, "search_docs"), (3, "get_pages")):
            with self.subTest(tool=name):
                responses = self.responses()
                responses[index]["isError"] = True
                responses[index]["content"] = [{"type": "text", "text":
                    f'Unknown path: {smoke.CANONICAL_PATH}; "status": "published"'}]
                with patch.object(smoke, "rpc", side_effect=responses):
                    with self.assertRaisesRegex(AssertionError, f"{name} returned a tool error"):
                        smoke.main()

    def test_search_snippet_is_not_a_matching_result(self):
        responses = self.responses()
        responses[2] = {"structuredContent": {"results": [
            {"path": "/other/", "snippet": smoke.CANONICAL_PATH}]}}
        with patch.object(smoke, "rpc", side_effect=responses):
            with self.assertRaisesRegex(AssertionError, "search_docs missing"):
                smoke.main()

    def test_missing_unpublished_or_empty_page_fails(self):
        for pages in ([], [{"path": smoke.CANONICAL_PATH, "status": "draft", "markdown": "# Guide"}],
                      [{"path": smoke.CANONICAL_PATH, "status": "published", "markdown": " "}]):
            with self.subTest(pages=pages):
                responses = self.responses()
                responses[3] = {"structuredContent": {"pages": pages}}
                with patch.object(smoke, "rpc", side_effect=responses):
                    with self.assertRaises(AssertionError):
                        smoke.main()

    def test_missing_page_resource_fails(self):
        responses = self.responses()
        responses[4] = {"resources": [{"uri": "docs://overview"}]}
        with patch.object(smoke, "rpc", side_effect=responses):
            with self.assertRaisesRegex(AssertionError, "resources/list missing"):
                smoke.main()


if __name__ == "__main__":
    unittest.main()
