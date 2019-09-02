#!/usr/bin/env bash
pytest umami tests/ --doctest-modules --cov=umami --cov-report term-missing -vvv
