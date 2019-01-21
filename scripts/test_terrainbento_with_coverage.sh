#!/usr/bin/env bash
py.test umami --doctest-modules --cov=umami tests/ --cov-report term-missing
