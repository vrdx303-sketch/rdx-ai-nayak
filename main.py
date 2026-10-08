from pathlib import Path
from threading import Thread
from urllib.parse import urlparse
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

KV='''<RDXRoot>:\n    orientation: "vertical"\n    padding: dp(18)\n    spacing: dp(12)\n    Label:\n        text: "RDX AI STUDIO"\n        font_size: "28sp"\n        bold: True\n        size_hint_y: None\n        height: dp(48)\n    Label:\n        text: "Android AI Studio • Downloader"\n        size_hint_y: None\n        height: dp(28)\n    TextInput:\n        id: url_input\n        hint_text: "Paste a direct download URL"\n        multiline: False\n        size_hint_y: None\n        height: dp(48)\n    Button:\n        text: "DOWNLOAD"\n        size_hint_y: None\n        height: dp(50)\n        on_release: root.start_download(url_input.text)\n    Label:\n        text: root.status\n        text_size: self.width, None\n    Label:\n        text: root.location\n        text_size: self.width, None\n    Widget:\n'''

class RDXRoot(BoxLayout):
    status=StringProperty("Ready.")
    location=StringProperty("Files are saved in the app's private storage.")
    def start_download(self,url):
        url=url.strip(); p=urlparse(url)
        if p.scheme not in ("http","https") or not p.netloc:
            self.status="Please enter a valid http:// or https:// URL."; return
        self.status="Downloading..."
        Thread(target=self._download,args=(url,),daemon=True).start()
    def _download(self,url):
        try:
            d=Path(App.get_running_app().user_data_dir)/"downloads"; d.mkdir(parents=True,exist_ok=True)
            name=Path(urlparse(url).path).name or "download.bin"
            name="".join(c for c in name if c.isalnum() or c in "._-")[:180] or "download.bin"
            target=d/name
            with requests.get(url,stream=True,timeout=60,headers={"User-Agent":"RDX-AI-Studio/1.0"}) as r:
                r.raise_for_status()
                with target.open("wb") as out:
                    for chunk in r.iter_content(chunk_size=131072):
                        if chunk: out.write(chunk)
            Clock.schedule_once(lambda dt:self._success(str(target)),0)
        except Exception as e:
            msg=str(e); Clock.schedule_once(lambda dt:self._error(msg),0)
    def _success(self,path): self.status="Download complete."; self.location=path
    def _error(self,msg): self.status="Download failed: "+msg; self.location="Check the URL and connection."

class RDXAIStudioApp(App):
    title="RDX AI Studio"
    def build(self): Builder.load_string(KV); return RDXRoot()

if __name__=="__main__": RDXAIStudioApp().run()
