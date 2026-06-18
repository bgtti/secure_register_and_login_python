"""
Docstring for Backend.app.constants.xss_vectors

XSS vectors, also log injection vectors 
"""

# there are a number of events in js that could be part of the list bellow... checkout http://help.dottoro.com/ljfvvdnm.php for more.
COMMON_XSS_VECTORS = [
    "\n",
    "\r",
    "$env",
    "&#x3c", # <
    "&#x3e", # >
    "&gt", # >
    "&lt", # <
    "&quot", # "
    "%3c", # <
    "%3e", # >
    ".js",
    "<?php",
    "<script",
    "<style",
    "alert",
    "cmd",
    "confirm",
    "data:",
    "data:text",
    "decodeuri",
    "document.cookie",
    "document.write",
    "dynsrc",
    "eval",
    "expression",
    "fromcharcode",
    "href",
    "iframe",
    "input type",
    "isindex",
    "javascript",
    "location.hash",
    "object data",
    "onchange",
    "onclick",
    "onerror",
    "onfocus",
    "onload",
    "onmouseover",
    "print(",
    "prompt(",
    "src=",
    "svg",
    "textarea",
    "tostring",
    "u003", # < for \u003C, \u003E, %u003C, and %u003E
    "unescape",
    "url(",
    "window",
    "with(document)",
]
"""`COMMON_XSS_VECTORS` is a black list of words that may indicate an injection attempt."""