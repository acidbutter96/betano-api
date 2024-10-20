import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--ignore-certificate-errors",
            "--disable-gpu",
            "--disable-software-rasterizer",
        ],
    )
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "sticky_sb=95f840234d38be31ef1cba76f5eabba5; sb_landing=true; _fs_sample=undefined; _lr_uf_-7hhr6m=58bff094-85d5-4ccb-9496-c89116b4418a; siteid=undefined; cf_clearance=qAkEjOKhhi4vRLf1kKZpY9Q2xpZYXdLibquTs2UlWq8-1729190890-1.2.1.1-xP4jHBhuetQG9cgiKyDMuL_cV___5LtBroM_MQicsTLd.iSj2P8J7ciRBkyQ0kFWhLMIcYOBygpgZzHbeSi64ZuahGuqUbTlqqSLSrGVqYqMXtFOow6.Bb7Dkdm3bTYqmcsLd7kY197ZLmWQXJdur1usNPvazT6UteFPNaiNxpylUOldqD0nibe9cnNb1lu1wsWnJddjlt2u2SOLyT7PlOwRqgYyq1efp6ocw73jeu6LQCD4GLiHIMBrzNkgZkdS7uNgyw4WqFLRcsabdpO.DwG7QdM6lMKygfDpHL0fFE1VUijLoKVSLaoZBdU7qsdvEJfTBqdDZeatcpsu5ejSySWghFe_duwOUHdm2RjZpTg.XcLLhygtsMJbHj0hMOpL; _gcl_au=1.1.1373718309.1729190892; _ga=GA1.1.1573955611.1729190892; cntps_id=e6101b950e846fd5451b33f1bbebee2a; __cf_bm=Y_Dsq4nJ0QupurkmJfSsP8FEZzPSzlpcqivRN.hSAOk-1729190897-1.0.1.1-mkKOblUZJ6KrMejbQ_9sEL71MKLNax635OAobKYkZ1IENbS9_ZmIxvw6pVWL2f3owmshZvBxZoElWoBUdn5A7g; _cfuvid=ulHUMPj8T4uOvs6Ntj.f0D053fFGLi9wg_k_kDYxqH0-1729190897006-0.0.1.1-604800000; datadome=0nI7df0IkWTOO_jOrwJ~rzrbPaTx_Qo5IYhbhzSOr8N0H8HvS5sbMmC9q3WI8hrYwW44gVEgD~0qM~xXSOeMrm~T5McT67EiinTHVLYLwNIilKlH90DafZr5GSmW~Tz8; DV360=fired; _lr_hb_-7hhr6m%2Fstoiximangr={%22heartbeat%22:1729191772078}; _lr_tabs_-7hhr6m%2Fstoiximangr={%22sessionID%22:0%2C%22recordingID%22:%225-b75791d0-8000-4a53-a340-d6d6080ad757%22%2C%22lastActivity%22:1729191797205%2C%22hasActivity%22:true%2C%22recordingConditionThreshold%22:89.46370249593411}; _ga_CHR7RP8E7T=GS1.1.1729190891.1.0.1729191803.60.0.0; _ga_SJLCV23YJW=GS1.1.1729190891.1.0.1729191803.60.0.990834388",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Linux\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    context = browser.new_context(ignore_https_errors=True, extra_http_headers=headers)
    page = context.new_page()
    page.goto("https://br.betano.com/")
    time.sleep(1)
    page.click('xpath=//button[@data-qa="login-button"]')
    # time.sleep(2)
    page.screenshot(path="example.png")
    print(page.title())
    browser.close()
