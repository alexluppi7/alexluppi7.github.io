import os
import requests
from urllib.parse import parse_qsl
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def main(args):

    # 1) Get method and headers
    method = args.get("__ow_method", "GET").upper()
    incoming_headers = args.get("__ow_headers", {})

    # 2) Identify the original host from the 'Host' header
    #    E.g., "api.example.com" (the user might have pointed that DNS to the function endpoint).
    host = incoming_headers.get("host", None)

    # 3) Identify scheme (http or https).
    #    In many serverless contexts, the request might be behind a DO load balancer with HTTPS.
    #    Sometimes 'x-forwarded-proto' might be "https".
    scheme = incoming_headers.get("x-forwarded-proto", "http")

    # 4) Get the path from __ow_path
    path = args.get("__ow_path", "")  # e.g. "/users/info"
    # We do not need to strip a leading slash here, because we handle it below.
   
    # If host is empty or not provided, you might want to default to something, or error out.
    if not host:
        return {
            "statusCode": 400,
            "body": "Missing 'Host' header in the incoming request, cannot bypass to original host."
        }

    # 5) Construct the target URL = scheme://host + path
    #    Example: "https://api.example.com/users/info"
    #    If the host includes a port, e.g. "api.example.com:8080", keep it as is.
    target_url = f"{scheme}://{host}{path}"

    # 6) Parse the query string into a dict
    #    e.g. "foo=1&bar=2" -> {"foo": "1", "bar": "2"}
    raw_query = args.get("__ow_query", "")
    query_params = dict(parse_qsl(raw_query))  # parse_qsl handles URL-encoded query strings


    # 7) Build headers to forward, excluding some that might conflict
    excluded_headers = {
        "host",
        "content-length",
        "transfer-encoding",
        "connection",
        "accept-encoding"
    }
    forward_headers = {}
    for h_name, h_value in incoming_headers.items():
        if h_name.lower() not in excluded_headers:
            forward_headers[h_name] = h_value

    # 8) Body (for POST, PUT, PATCH). In DO Functions, it's usually in args["body"] as a string or None
    body = args.get("body", None)

    logging.info(f"Passou aqui! {target_url}")
    print(f"Passou aqui! {target_url}")

    if "ondigitalocean.app" in host:
        logging.warning("Detected a request to the same domain (potential loop). Not forwarding.")
        return {
            "statusCode": 400,
            "body": "Cannot proxy to the same domain as the function (would cause loop)."
        }

    # 9) Make the request to the original host/path
    # try:
    #     resp = requests.request(
    #         method=method,
    #         url=target_url,
    #         headers=forward_headers,
    #         params=query_params,
    #         data=body,
    #         allow_redirects=False,
    #         timeout=10  # segundos
    #     )
    # except Exception as e:
    #     return {
    #         "statusCode": 502,
    #         "body": { "value": "Request Error" }
    #     }

    # # 10) Build the response back to the caller
    # #     Include status code, body, and (most) headers from the upstream.
    # exclude_resp_hdrs = {"content-encoding", "transfer-encoding", "connection"}
    # returned_headers = {}
    # for r_name, r_value in resp.headers.items():
    #     if r_name.lower() not in exclude_resp_hdrs:
    #         returned_head

    # return {
    #     "statusCode": resp.status_code,
    #     "headers": returned_headers,
    #     "body": resp.text  # or use resp.content if binary, but then you need base64 encoding, etc.
    # }
    return { "statusCode": 200, "body": { "value": "Hello Folks" }}

# def main(args):
#     """
#     Example of a "bypass" proxy using DigitalOcean Functions:
#       - Receives an HTTP request (converted by DO Functions into the 'args' dict).
#       - Forwards the request to the same Host + Path that originally came in.
#       - Returns the upstream response back to the caller.

#     Caveats:
#       - No fixed outbound IP on DO Functions.
#       - Host-based or SNI-based HTTPS might not be fully transparent.
#       - Typically used for rewriting or short-living proxy tasks.

#     'args' keys of interest:
#       - __ow_method:  The HTTP method (GET, POST, etc.).
#       - __ow_headers: A dict of headers from the incoming request.
#       - __ow_path:    The path portion after the function's base URL.
#       - __ow_query:   The raw query string (e.g., "foo=1&bar=2").
#       - body:         The request body if present (for POST, PUT, etc.).
#     """

    # # 1) Get method and headers
    # method = args.get("__ow_method", "GET").upper()
    # incoming_headers = args.get("__ow_headers", {})

    # # 2) Identify the original host from the 'Host' header
    # #    E.g., "api.example.com" (the user might have pointed that DNS to the function endpoint).
    # host = incoming_headers.get("host", None)

    # # 3) Identify scheme (http or https).
    # #    In many serverless contexts, the request might be behind a DO load balancer with HTTPS.
    # #    Sometimes 'x-forwarded-proto' might be "https".
    # scheme = incoming_headers.get("x-forwarded-proto", "http")

    # # 4) Get the path from __ow_path
    # path = args.get("__ow_path", "")  # e.g. "/users/info"
    # # We do not need to strip a leading slash here, because we handle it below.

    # # If host is empty or not provided, you might want to default to something, or error out.
    # if not host:
    #     return {
    #         "statusCode": 400,
    #         "body": "Missing 'Host' header in the incoming request, cannot bypass to original host."
    #     }

    # # 5) Construct the target URL = scheme://host + path
    # #    Example: "https://api.example.com/users/info"
    # #    If the host includes a port, e.g. "api.example.com:8080", keep it as is.
    # target_url = f"{scheme}://{host}{path}"

    # # 6) Parse the query string into a dict
    # #    e.g. "foo=1&bar=2" -> {"foo": "1", "bar": "2"}
    # raw_query = args.get("__ow_query", "")
    # query_params = dict(parse_qsl(raw_query))  # parse_qsl handles URL-encoded query strings

    # # 7) Build headers to forward, excluding some that might conflict
    # excluded_headers = {
    #     "host",
    #     "content-length",
    #     "transfer-encoding",
    #     "connection",
    #     "accept-encoding"
    # }
    # forward_headers = {}
    # for h_name, h_value in incoming_headers.items():
    #     if h_name.lower() not in excluded_headers:
    #         forward_headers[h_name] = h_value

    # # 8) Body (for POST, PUT, PATCH). In DO Functions, it's usually in args["body"] as a string or None
    # body = args.get("body", None)

    # # 9) Make the request to the original host/path
    # try:
    #     resp = requests.request(
    #         method=method,
    #         url=target_url,
    #         headers=forward_headers,
    #         params=query_params,
    #         data=body,
    #         allow_redirects=False
    #     )
    # except Exception as e:
    #     return {
    #         "statusCode": 502,
    #         "body": f"Proxy error when forwarding to {target_url}: {str(e)}"
    #     }

    # # 10) Build the response back to the caller
    # #     Include status code, body, and (most) headers from the upstream.
    # exclude_resp_hdrs = {"content-encoding", "transfer-encoding", "connection"}
    # returned_headers = {}
    # for r_name, r_value in resp.headers.items():
    #     if r_name.lower() not in exclude_resp_hdrs:
    #         returned_headers[r_name] = r_value

    # return {
    #     "statusCode": resp.status_code,
    #     "headers": returned_headers,
    #     "body": resp.text  # or use resp.content if binary, but then you need base64 encoding, etc.
    # }
