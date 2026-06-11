from pathlib import Path

path = Path('utils/savanna_client.py')
text = path.read_text()
old = '''    def invalid_workspace_request(self):
        return self._make_request("GET", self._get_url(workspace_id="invalid"))

    def get_status_value(self):
        response = self.get_workspace_status()
        if response.status_code == 200:
            return response.json().get("status")
        return None
'''
new = '''    def invalid_workspace_request(self):
        return self._make_request("GET", self._get_url(workspace_id="invalid"))

    def get_status_value(self):
        response = self.get_workspace_status()
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                result = data.get("Result")
                if isinstance(result, dict):
                    return result.get("status")
        return None
'''
if old not in text:
    raise SystemExit('old text not found')
path.write_text(text.replace(old, new))
print('updated')
