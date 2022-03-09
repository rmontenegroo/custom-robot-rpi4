import time
import pychromecast

ccs, browser = pychromecast.discovery.discover_chromecasts()
print(ccs)

cc = ccs[0]

# cc.wait()

# print(cc.device)

# pychromecast.discovery.stop_discovery(browser)
