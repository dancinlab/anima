"""anima_client.py — minimal Python client for anima daemon (CHAT.md Phase 4).

Connects to anima live daemon over TCP, parses JSONL frames, exposes
async iterator for spontaneous + response messages.

Usage:
    import anima_client
    c = anima_client.connect("localhost", 7878)
    c.speak("alice", "안녕 모두?")
    for msg in c.stream():
        if msg["type"] == "message":
            print(f"[{msg['speaker']}] {msg['text']}",
                  "🎙" if msg.get("spontaneous") else "")

Or CLI:
    python3 anima_client.py --host localhost --port 7878 --as alice

Frame protocol (line-delimited JSON):
    daemon → client:   {"type":"hello","msg":"anima live"}
                       {"type":"message","speaker":"<id>","text":"<text>",
                        "spontaneous":bool}
    client → daemon:   {"type":"speak","speaker":"<name>","text":"<text>"}
                       (currently treated as raw stdin line by daemon)

See CHAT.md Phase 4 for full protocol spec.
"""
import json
import socket
import sys
import threading
import time
import argparse


class AnimaClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None
        self.recv_buf = b""
        self._closed = False

    def connect(self) -> "AnimaClient":
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        return self

    def speak(self, speaker: str, text: str) -> None:
        frame = json.dumps({"type": "speak", "speaker": speaker, "text": text})
        self.sock.sendall((frame + "\n").encode("utf-8"))

    def send_raw(self, line: str) -> None:
        self.sock.sendall((line.rstrip("\n") + "\n").encode("utf-8"))

    def stream(self):
        """Yield parsed JSONL frames from the daemon."""
        while not self._closed:
            try:
                chunk = self.sock.recv(4096)
            except (ConnectionResetError, OSError):
                break
            if not chunk:
                break
            self.recv_buf += chunk
            while b"\n" in self.recv_buf:
                line, self.recv_buf = self.recv_buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line.decode("utf-8"))
                except json.JSONDecodeError:
                    yield {"type": "raw", "data": line.decode("utf-8", errors="replace")}

    def close(self) -> None:
        self._closed = True
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass


def connect(host: str = "localhost", port: int = 7878) -> AnimaClient:
    return AnimaClient(host, port).connect()


def _cli_main() -> int:
    p = argparse.ArgumentParser(description="anima live daemon CLI client")
    p.add_argument("--host", default="localhost")
    p.add_argument("--port", type=int, default=7878)
    p.add_argument("--as", dest="speaker", default="me",
                   help="speaker name for outgoing messages")
    p.add_argument("--once", default=None,
                   help="send a single message then drain responses and exit")
    args = p.parse_args()

    try:
        c = connect(args.host, args.port)
    except OSError as e:
        sys.stderr.write(f"[anima-client] connect failed: {e}\n")
        return 1

    print(f"[anima-client] connected to {args.host}:{args.port} as '{args.speaker}'")

    # Reader thread
    def _reader():
        for msg in c.stream():
            t = msg.get("type")
            if t == "hello":
                print(f"[server] {msg.get('msg', '')}")
            elif t == "message":
                spk = msg.get("speaker", "?")
                txt = msg.get("text", "")
                mark = " 🎙" if msg.get("spontaneous") else ""
                print(f"[{spk}]{mark} {txt}")
            else:
                print(f"[{t or 'raw'}] {msg}")
        print("[anima-client] disconnected")

    t = threading.Thread(target=_reader, daemon=True)
    t.start()

    if args.once is not None:
        c.speak(args.speaker, args.once)
        time.sleep(2.0)  # let response arrive
        c.close()
        return 0

    # Interactive stdin → speak
    print("[anima-client] type messages (or /exit to quit)")
    try:
        for line in sys.stdin:
            line = line.rstrip("\n")
            if line == "/exit" or line == "/quit":
                break
            if not line:
                continue
            c.speak(args.speaker, line)
    except KeyboardInterrupt:
        pass

    c.close()
    return 0


if __name__ == "__main__":
    sys.exit(_cli_main())
