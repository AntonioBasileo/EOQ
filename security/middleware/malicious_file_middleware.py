from django.http import HttpResponseForbidden
import os

class FileScanError(Exception):
    pass

class MaliciousFileUploadMiddleware:

    FORBIDDEN_EXTENSIONS = {'.exe', '.bat', '.sh', '.js', '.php', '.scr', '.dll'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    MALICIOUS_PATTERNS = [
        b'<script',  # script HTML/JS
        b'<?php',    # codice PHP
        b'#!/bin/bash',  # script bash
        b'PowerShell',   # script PowerShell
        b'eval(',    # uso sospetto di eval
        b'base64_decode',
        b'cmd.exe',
        b'@echo off',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for file in request.FILES.values():
            ext = os.path.splitext(file.name)[1].lower()
            if ext in self.FORBIDDEN_EXTENSIONS:
                return HttpResponseForbidden("File con estensione non consentita.")
            if file.size > self.MAX_FILE_SIZE:
                return HttpResponseForbidden("File troppo grande.")

            try:
                file.seek(0)
                content = file.read(10 * 1024 * 1024)
                file.seek(0)

                for pattern in self.MALICIOUS_PATTERNS:
                    if pattern in content:
                        return HttpResponseForbidden("File con contenuto potenzialmente malevolo.")
            except FileScanError:
                return HttpResponseForbidden("Errore durante la scansione del file.")
        return self.get_response(request)
