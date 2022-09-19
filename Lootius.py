import webview
import threading


def	customLogic(window):
	window.toggle_fullscreen()
	window.evaluate_js('alert("Nice one brother")')

window = webview.create_window("Lootius", "./views/index.html")
webview.start(customLogic, window, gui="cef", http_server=True, debug=True)