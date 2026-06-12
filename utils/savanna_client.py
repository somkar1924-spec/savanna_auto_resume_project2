import os
import json
import hmac
import hashlib
from datetime import datetime, timezone
from urllib.parse import urlparse, quote

import requests
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)


class SavannaClient:
    def __init__(
        self,
        base_url=None,
        key_id=None,
        api_key=None,
        wg_id=None,
        ws_id=None,
        region=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_session_token=None,
    ):
        self.base_url = base_url or os.getenv("BASE_URL")
        self.key_id = key_id or os.getenv("KEY_ID")
        self.api_key = api_key or os.getenv("API_KEY")
        self.aws_access_key_id = aws_access_key_id or os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = aws_secret_access_key or os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_session_token = aws_session_token or os.getenv("AWS_SESSION_TOKEN")
        self.wg_id = wg_id or os.getenv("WORKGROUP_ID")
        self.ws_id = ws_id or os.getenv("WORKSPACE_ID")
        self.restpp_url = os.getenv("RESTPP_URL")
        self.restpp_token = os.getenv("RESTPP_TOKEN") or os.getenv("RESTPP")
        self.restpp_token_method = os.getenv("RESTPP_TOKEN_METHOD", "header").strip().lower()
        self.region = region or os.getenv("AWS_REGION", "us-west-1")
        self.service = "execute-api"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.graph_name = os.getenv("GRAPH_NAME")
        self.query_name = os.getenv("QUERY_NAME")

    def _get_url(self, path="", workspace_id=None):
        workspace_id = workspace_id or self.ws_id
        return f"{self.base_url}/workgroups/{self.wg_id}/workspaces/{workspace_id}{path}"

    def _sign(self, key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    def _get_signature_key(self, key, date_stamp, region_name, service_name):
        k_date = self._sign(("AWS4" + key).encode("utf-8"), date_stamp)
        k_region = self._sign(k_date, region_name)
        k_service = self._sign(k_region, service_name)
        return self._sign(k_service, "aws4_request")

    def _get_canonical_query_string(self, query_string):
        if not query_string:
            return ""

        query_params = []
        for pair in query_string.split("&"):
            if not pair:
                continue
            key, sep, value = pair.partition("=")
            query_params.append((quote(key, safe="~-._"), quote(value, safe="~-._")))

        query_params.sort()
        return "&".join(f"{k}={v}" for k, v in query_params)

    def _get_headers(self, method, url, payload="", api_key=None, key_id=None):
        explicit_api_key = api_key is not None
        explicit_key_id = key_id is not None
        api_key = api_key or self.api_key
        key_id = key_id or self.key_id

        use_aws_creds = self.aws_access_key_id and self.aws_secret_access_key and not (explicit_api_key or explicit_key_id)
        if use_aws_creds:
            signing_key = self.aws_secret_access_key
            signing_id = self.aws_access_key_id
        elif api_key:
            signing_key = None
            signing_id = None
        else:
            raise ValueError(
                "AWS credentials are required for API request signing, or provide a valid API key. "
                "Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, or set API_KEY in the environment."
            )

        parsed = urlparse(url)
        host = parsed.netloc
        canonical_uri = parsed.path or "/"
        canonical_querystring = self._get_canonical_query_string(parsed.query)

        headers = {
            "content-type": "application/json",
            "host": host,
        }

        if use_aws_creds:
            payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            now = datetime.now(timezone.utc)
            amz_date = now.strftime("%Y%m%dT%H%M%SZ")
            date_stamp = now.strftime("%Y%m%d")

            headers.update({
                "x-amz-date": amz_date,
                "x-amz-content-sha256": payload_hash,
            })
            if self.aws_session_token:
                headers["x-amz-security-token"] = self.aws_session_token

            canonical_headers = "".join(f"{k}:{headers[k]}\n" for k in sorted(headers))
            signed_headers = ";".join(sorted(headers))
            canonical_request = "\n".join([
                method,
                canonical_uri,
                canonical_querystring,
                canonical_headers,
                signed_headers,
                payload_hash,
            ])

            credential_scope = f"{date_stamp}/{self.region}/{self.service}/aws4_request"
            string_to_sign = "\n".join([
                "AWS4-HMAC-SHA256",
                amz_date,
                credential_scope,
                hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
            ])

            signing_key = self._get_signature_key(signing_key, date_stamp, self.region, self.service)
            signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

            headers["Authorization"] = (
                f"AWS4-HMAC-SHA256 Credential={signing_id}/{credential_scope}, "
                f"SignedHeaders={signed_headers}, Signature={signature}"
            )
        else:
            headers["x-api-key"] = api_key

        return headers

    def _make_request(self, method, url, payload=None, api_key=None, key_id=None):
        body = ""
        if payload is not None:
            if isinstance(payload, str):
                body = payload
            else:
                body = json.dumps(payload, separators=(",", ":"), sort_keys=True)

        headers = self._get_headers(method, url, body, api_key=api_key, key_id=key_id)
        if key_id:
            headers["X-TG-Key-ID"] = key_id
        elif self.key_id:
            headers["X-TG-Key-ID"] = self.key_id
        try:
            return self.session.request(method, url, headers=headers, data=body, timeout=30)
        except requests.RequestException as exc:
            response = requests.Response()
            response.status_code = 503
            response._content = str(exc).encode("utf-8")
            response.reason = "Service Unavailable"
            response.url = url
            return response

    def get_workspace_status(self):
        return self._make_request("GET", self._get_url())

    def suspend_workspace(self):
        return self._make_request("POST", self._get_url("/pause"))

    def resume_workspace(self):
        return self._make_request("POST", self._get_url("/resume"))

    def enable_auto_resume(self, enabled=True):
        payload = {"auto_resume": enabled}
        return self._make_request("PUT", self._get_url(), payload=payload)

    def set_auto_suspend_time(self, minutes):
        payload = {"auto_suspend_time": minutes}
        return self._make_request("PUT", self._get_url(), payload=payload)

    def _get_restpp_query_url(self):
        graph_name = self.graph_name
        query_name = self.query_name
        if not graph_name or not query_name:
            raise ValueError("GRAPH_NAME and QUERY_NAME must be defined for RESTPP query execution.")

        if not self.restpp_url:
            return f"{self.base_url}/workgroups/{self.wg_id}/workspaces/{self.ws_id}/query/{graph_name}/{query_name}"

        base_url = self.restpp_url.rstrip("/")
        if "/restpp/query/" in base_url:
            if base_url.lower().endswith(f"/{query_name.lower()}"):
                return base_url
            return f"{base_url}/{graph_name}/{query_name}"
        if base_url.lower().endswith("/restpp"):
            return f"{base_url}/query/{graph_name}/{query_name}"
        if base_url.lower().endswith("/query"):
            return f"{base_url}/{graph_name}/{query_name}"
        return f"{base_url}/restpp/query/{graph_name}/{query_name}"

    def _get_restpp_token_headers(self):
        if not self.restpp_token:
            return None

        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.restpp_token}",
        }

    def _get_restpp_token_url(self, query_url):
        if not self.restpp_token or self.restpp_token_method != "query":
            return query_url

        delimiter = "?" if "?" not in query_url else "&"
        return f"{query_url}{delimiter}token={quote(self.restpp_token, safe='')}"

    def run_query(self, query_payload):
        query_url = self._get_restpp_query_url()

        print(f"\nQUERY URL = {query_url}")
        print(f"GRAPH_NAME = {self.graph_name}")
        print(f"QUERY_NAME = {self.query_name}\n")

        if query_payload is not None and not isinstance(query_payload, str):
           payload = json.dumps(query_payload, separators=(",", ":"), sort_keys=True)
        else:
           payload = query_payload or ""

        if self.restpp_token:
            if self.restpp_token_method == "query":
                query_url = self._get_restpp_token_url(query_url)
                headers = {"Content-Type": "application/json"}
            else:
                headers = self._get_restpp_token_headers()
                if self.key_id:
                    headers["X-TG-Key-ID"] = self.key_id

            try:
                return self.session.request("POST", query_url, headers=headers, data=payload, timeout=30)
            except requests.RequestException as exc:
                response = requests.Response()
                response.status_code = 503
                response._content = str(exc).encode("utf-8")
                response.reason = "Service Unavailable"
                response.url = query_url
                return response

        if self.restpp_url and not self.restpp_token:
            raise ValueError(
                "RESTPP_URL is configured but RESTPP_TOKEN is missing. "
                "Set RESTPP_TOKEN in environment or .env for TigerGraph Cloud RESTPP query execution."
            )

        return self._make_request("POST", query_url, payload=query_payload)

    def invalid_api_key_request(self):
        return self._make_request("GET", self._get_url(), api_key="invalid-key")

    def invalid_workspace_request(self):
        return self._make_request("GET", self._get_url(workspace_id="invalid"))

    def get_status_value(self):
        response = self.get_workspace_status()
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                result = data.get("Result")
                if isinstance(result, dict):
                    return result.get("status")
                return data.get("status")
        return None