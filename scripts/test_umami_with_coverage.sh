#!/usr/bin/env bash
pytest umami --doctest-modules --cov=umami tests/ --cov-report term-missing
