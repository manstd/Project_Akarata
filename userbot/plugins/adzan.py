# ported from uniborg
# https://github.com/muhammedfurkan/UniBorg/blob/master/stdplugins/ezanvakti.py
import json

import requests

from ..utils import admin_cmd, sudo_cmd
from . import CMD_HELP


@bot.on(admin_cmd(pattern="adzan (.*)", outgoing=True))
@bot.on(sudo_cmd(pattern="adzan (.*)", allow_sudo=True))
async def get_adzan(adzan):
    LOKASI = adzan.pattern_match.group(1)
    url = f"https://api.pray.zone/v2/times/today.json?city={LOKASI}"
    request = requests.get(url)
    if request.status_code != 200:
        await edit_delete(
            adzan, f"`Couldn't fetch any data about the city {LOKASI}`", 5
        )
        return
    result = json.loads(request.text)
    catresult = f"<b>Islamic prayer times </b>\
            \n\n<b>Kota     : </b><i>{result['results']['location']['city']}</i>\
            \n<b>Negara  : </b><i>{result['results']['location']['country']}</i>\
            \n<b>Tanggal     : </b><i>{result['results']['datetime'][0]['date']['gregorian']}</i>\
            \n<b>Hijriah    : </b><i>{result['results']['datetime'][0]['date']['hijri']}</i>\
            \n\n<b>Imsak    : </b><i>{result['results']['datetime'][0]['times']['Imsak']}</i>\
            \n<b>Matahari terbit  : </b><i>{result['results']['datetime'][0]['times']['Sunrise']}</i>\
            \n<b>Fajar     : </b><i>{result['results']['datetime'][0]['times']['Fajr']}</i>\
            \n<b>Dzuhur    : </b><i>{result['results']['datetime'][0]['times']['Dhuhr']}</i>\
            \n<b>Ashar      : </b><i>{result['results']['datetime'][0]['times']['Asr']}</i>\
            \n<b>Matahari terbenam   : </b><i>{result['results']['datetime'][0]['times']['Sunset']}</i>\
            \n<b>Maghrib  : </b><i>{result['results']['datetime'][0]['times']['Maghrib']}</i>\
            \n<b>Isha     : </b><i>{result['results']['datetime'][0]['times']['Isha']}</i>\
            \n<b>Tengah malam : </b><i>{result['results']['datetime'][0]['times']['Midnight']}</i>\
    "
    await edit_or_reply(adzan, catresult, "html")


CMD_HELP.update(
    {
        "adzan": "__**NAMA PLUGIN :** adzan__\
    \n\n✅** CMD ➥** `.adzan` <nama kota>\
    \n**Fungsi   ➥  **__Menunjukkan waktu sholat Islam dari nama kota yang diberikan__"
    }
)
