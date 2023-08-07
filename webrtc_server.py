import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

from aiohttp import web
from av import VideoFrame
import aiohttp_cors
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer,  MediaRelay