# copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import datetime

from imp import reload
reload(logging)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")


def time_zone(sec, fmt):
    real_time = datetime.datetime.now() + datetime.timedelta(hours=8)
    return real_time.timetuple()


logging.Formatter.converter = time_zone
_logger = logging.getLogger(__name__)

Color = {
    'RED': '\033[31m',
    'HEADER': '\033[35m',  # deep purple
    'PURPLE': '\033[95m',  # purple
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m'
}


def coloring(message, color="OKGREEN"):
    assert color in Color.keys()
    if os.environ.get('PADDLECLAS_COLORING', False):
        return Color[color] + str(message) + Color["ENDC"]
    else:
        return message


def anti_fleet(log):
    """
    logs will print multi-times when calling Fleet API.
    Only display single log and ignore the others.
    """

    def wrapper(fmt, *args):
        if int(os.getenv("PADDLE_TRAINER_ID", 0)) == 0:
            log(fmt, *args)

    return wrapper


@anti_fleet
def info(fmt, *args):
    _logger.info(fmt, *args)


@anti_fleet
def warning(fmt, *args):
    _logger.warning(coloring(fmt, "RED"), *args)


@anti_fleet
def error(fmt, *args):
    _logger.error(coloring(fmt, "FAIL"), *args)


def scaler(name, value, step, writer):
    writer.add_scalar(name, value, step)


def advertise():
    """
    Show the advertising message like the following:

    ===========================================================
    ==        PaddleClas is powered by PaddlePaddle !        ==
    ===========================================================
    ==                                                       ==
    ==   For more info please go to the following website.   ==
    ==                                                       ==
    ==       https://github.com/PaddlePaddle/PaddleClas      ==
    ===========================================================

    """
    copyright = "PaddleClas is powered by PaddlePaddle !"
    ad = "For more info please go to the following website."
    website = "https://github.com/PaddlePaddle/PaddleClas"
    AD_LEN = 6 + len(max([copyright, ad, website], key=len))

    info(
        coloring("\n{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n".format(
            "=" * (AD_LEN + 4),
            "=={}==".format(copyright.center(AD_LEN)),
            "=" * (AD_LEN + 4),
            "=={}==".format(' ' * AD_LEN),
            "=={}==".format(ad.center(AD_LEN)),
            "=={}==".format(' ' * AD_LEN),
            "=={}==".format(website.center(AD_LEN)),
            "=" * (AD_LEN + 4), ), "RED"))
