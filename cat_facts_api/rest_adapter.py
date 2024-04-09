import json
import requests
import requests.packages
from typing import List, Dict
from json import JSONDecodeError
import logging
from cat_facts_api.exceptions import CatApiException
from cat_facts_api.result import Result


class RestAdapter:
    def __init__(self, hostname: str, logger: logging.Logger = None):
        self.url = "https://{}/".format(hostname)
        self._logger = logger or logging.getLogger(__name__)

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        full_url = self.url + endpoint
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        try:
            self._logger.debug(msg=log_line_pre)
            response = requests.request(method=http_method, url=full_url, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise CatApiException("Request failed") from e
        
        try:
            data_out = response.json()
        except (ValueError, JSONDecodeError) as e:
            raise CatApiException("Bad JSON in response") from e

        is_success = 299 >= response.status_code >= 200
        # log_line = log_line_post.format(is_success, response.status_code, response.reason)
        if is_success:
            # self._logger.debug(msg=log_line)
            return Result(response.status_code, message=response.reason, data=data_out)
        # self._logger.error(msg=log_line)
        raise CatApiException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> List[Dict]:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None):
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)
    
    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None):
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)