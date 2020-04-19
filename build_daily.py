#!/usr/bin/env python3
import requests
import re
import subprocess
from xml.etree import ElementTree

lastBuildID = requests.get('https://jenkins.darlinghq.org/job/darling-ubuntu-latest/lastSuccessfulBuild/buildNumber').text

areq = requests.get('http://darling-daily.s3.eu-central-1.amazonaws.com/?delimiter=/&prefix=jobs/darling-ubuntu-latest/' + lastBuildID + '/')
artifactsListing = ElementTree.fromstring(areq.content)

namespaces = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
keys = artifactsListing.findall('./s3:Contents/s3:Key', namespaces)

for key in keys:
    text = key.text
    if "/darling_" in text:
        artifactUrl = 'http://darling-daily.s3.eu-central-1.amazonaws.com/' + text
        break

if not artifactUrl:
    print("Artifact not found")
    sys.exit(1)

print("Artifact URL: " + artifactUrl)
reVersion = re.compile('/darling_([^_]+)')
match = reVersion.search(artifactUrl)

if not match:
    print("Artifact version cannot be parsed")
    sys.exit(1)

version = match.group(1)

# tag = "darlinghq/darling:v" + version
# Until we have a script that deletes old images
# E.g. from here https://gist.github.com/transcranial/be0f8f0d80e464f4032e
tag = "docker.pkg.github.com/darlinghq/darling/darling:latest"

subprocess.run(["docker", "build", "--build-arg", "DARLING_DEB=" + artifactUrl, "-t", tag, "."], check=True)
#subprocess.run(["docker", "tag", tag, "darlinghq/darling:latest"], check=True)
subprocess.run(["docker", "push", tag])
#subprocess.run(["docker", "push", "darlinghq/darling:latest"])

